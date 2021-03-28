from datetime import datetime
from typing import Optional
import asyncio

from services.customEnv import EnvConfig
from services.customFns import normalizeMovieName
from sqlalchemy import insert, select, update

from .dbModel import Connection, Movie
from .extractMovieReviews import extractMovieReviews
from services.customTypes import storedMovieInfo


async def debounceMovieInfo(movieName: str) -> tuple[list[str], bool]:
    normalizedMovieName = normalizeMovieName(movieName)
    storedMovie: storedMovieInfo = Connection.execute(
        select([Movie]).where(Movie.name == normalizedMovieName)
    ).fetchone()
    isDebounced = False

    if storedMovie == None:
        movieReviews = await extractMovieReviews(normalizedMovieName)
        mutation = insert(Movie).values(
            name=normalizedMovieName,
            update_date=datetime.now(),
            reviews=movieReviews,
        )
    elif (datetime.now() - storedMovie[1]).seconds > EnvConfig.MOVIE_SESSION_TIMEOUT:
        movieReviews = await extractMovieReviews(normalizedMovieName)
        mutation = (
            update(Movie)
            .where(Movie.name == normalizedMovieName)
            .values(update_date=datetime.now(), reviews=movieReviews)
        )
    else:
        movieReviews = storedMovie[2]
        mutation = None
        isDebounced = True

    if mutation != None:
        Connection.execute(mutation)

    return movieReviews, isDebounced
