from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine) #Create tables and Columns in the database

class ChoiceBase(BaseModel):
    choice: str
    is_correct: bool


class QuestionBase(BaseModel):
    question: str
    choices: List[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependecy):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.post("/questions/")
async def create_question(questions: QuestionBase, db: db_dependecy):
    db_question = models.Questions(question=questions.question)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in questions.choices:
        db_choice = models.Choices(choice=choice.choice, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)

    db.commit()
    return {"message": "Question and choices created successfully"}

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependecy):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result