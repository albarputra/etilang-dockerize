from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(
    os.getenv('SQLALCHEMY_DATABASE_URL'),
    echo=True
)


Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
