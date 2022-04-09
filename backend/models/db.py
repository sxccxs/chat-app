from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING, future=True, echo=True)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
