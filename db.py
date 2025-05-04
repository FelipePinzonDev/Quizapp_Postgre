from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:password@192.168.32.1:5432/QuizApp'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# To give access from POSTGRESQL to connect between POSTGRESQL WINDOWS and Code on WSL

# U need to paste this code in WSL to find the ip from conetion and use on the line 5: ip route show | grep -i default | awk '{ print $3}'

# Then U need to go and look the firewall and and a new rule that allow the port to connect like 5432

# Then U need to go to the file named pg_hba inside os Postgresql folder and data : host    all             all             192.168.42.5/32         md5