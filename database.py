from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()


class SentimentRecord(Base):
    __tablename__ = "sentiment_records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    title = Column(String)
    summary = Column(String)
    source = Column(String)
    url = Column(String)
    title_score = Column(Float)
    summary_score = Column(Float)
    title_positive = Column(Integer)
    title_negative = Column(Integer)
    summary_positive = Column(Integer)
    summary_negative = Column(Integer)


# Database setup
engine = create_engine('sqlite:///./sentiment.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()