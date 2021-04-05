from datetime import datetime

from services.customEnv import EnvConfig
from services.customFns import normalizeMovieName
from services.customTypes import (
    debouncedMovieStateInfo,
    fetchStateInfo,
    storedMovieInfo,
)
from sqlalchemy import insert, select, update

from .dbModel import Connection, Movie
from .extractMovieReviews import extractMovieReviews


async def debounceMovieInfo(movieName: str) -> debouncedMovieStateInfo:
    normalizedMovieName = normalizeMovieName(movieName)
    storedMovie: storedMovieInfo = Connection.execute(
        select([Movie]).where(Movie.name == normalizedMovieName)
    ).fetchone()
    fetchState: fetchStateInfo

    if storedMovie == None:
        movieReviews = await extractMovieReviews(normalizedMovieName)
        fetchState = "Scraped from Web"
        mutation = insert(Movie).values(
            name=normalizedMovieName,
            update_date=datetime.now(),
            reviews=movieReviews,
        )
    elif EnvConfig.SESSION_TIMEOUT <= (datetime.now() - storedMovie[1]).total_seconds():
        movieReviews = await extractMovieReviews(normalizedMovieName)
        fetchState = "Refectched and Cached"
        mutation = (
            update(Movie)
            .where(Movie.name == normalizedMovieName)
            .values(update_date=datetime.now(), reviews=movieReviews)
        )
    else:
        movieReviews = storedMovie[2]
        fetchState = "Read from Cache"
        mutation = None
        isDebounced = True

    if mutation != None:
        Connection.execute(mutation)

    return movieReviews, fetchState
