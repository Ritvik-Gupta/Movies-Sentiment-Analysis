from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, Column, DateTime, String
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import select

Engine = create_engine(
    "postgresql://postgres:Ageofempire0207@localhost/movies-sentiment-analysis",
    echo=True,
)

BaseEntity = declarative_base()


class Movie(BaseEntity):
    __tablename__ = "movie"
    name = Column(String(), primary_key=True)
    update_date = Column(DateTime(timezone=False), nullable=False)
    reviews = Column(ARRAY(String), nullable=False)


Connection = Engine.connect()
BaseEntity.metadata.create_all(bind=Engine)
