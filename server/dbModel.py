from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy import create_engine as createEngine, MetaData

meta = MetaData()

Engine = createEngine(
    "postgresql://postgres:Ageofempire0207@localhost/movies-sentiment-analysis",
    echo=True,
)

Movie = Table(
    "movie",
    meta,
    Column("name", String(), primary_key=True),
    Column("last_read_date", DateTime(timezone=False), nullable=False),
)

Review = Table(
    "review",
    meta,
    Column("movie_name", String(), ForeignKey("movie.name"), primary_key=True),
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("content", String, nullable=False),
)

Connection = Engine.connect()

meta.create_all(Engine)
