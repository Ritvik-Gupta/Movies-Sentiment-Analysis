from services.customEnv import EnvConfig
from sqlalchemy import ARRAY, Column, DateTime, String
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine(EnvConfig.DATABASE_CONFIG_URL, echo=True)
BaseEntity = declarative_base()


class Movie(BaseEntity):
    __tablename__ = "movie"
    name = Column(String(), primary_key=True)
    update_date = Column(DateTime(timezone=False), nullable=False)
    reviews = Column(ARRAY(String), nullable=False)


Connection = Engine.connect()
