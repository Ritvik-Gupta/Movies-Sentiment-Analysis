from datetime import datetime
from typing import Optional

from sqlalchemy import select, insert, update

from customFns import normalizeMovieName
from dbModel import Connection, Movie
from extractMovieReviews import extractMovieReviews


def debounceMovieInfo(movieName: str) -> tuple[list[str], bool]:
    normalizedMovieName = normalizeMovieName(movieName)
    isDebounced = False

    storedMovie: Optional[tuple[datetime, list[str]]] = Connection.execute(
        select([Movie.update_date, Movie.reviews]).where(
            Movie.name == normalizedMovieName
        )
    ).fetchone()

    if storedMovie == None:
        movieReviews = extractMovieReviews(normalizedMovieName)

        Connection.execute(
            insert(Movie).values(
                name=normalizedMovieName,
                update_date=datetime.now(),
                reviews=movieReviews,
            )
        )
    elif (datetime.now() - storedMovie[0]).seconds > 120:
        movieReviews = extractMovieReviews(normalizedMovieName)

        Connection.execute(
            update(Movie)
            .where(Movie.name == normalizedMovieName)
            .values(update_date=datetime.now(), reviews=movieReviews)
        )
    else:
        movieReviews = storedMovie[1]
        isDebounced = True

    return movieReviews, isDebounced
