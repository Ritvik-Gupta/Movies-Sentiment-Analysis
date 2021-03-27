from datetime import datetime

from sqlalchemy import select

from customFns import normalizeMovieName
from dbModel import Connection, Movie, Review
from extractMovieReviews import extractMovieReviews


def debounceMovieInfo(movieName: str) -> list[str]:
    normalizedName = normalizeMovieName(movieName)

    storedReviews: list[tuple[str]] = Connection.execute(
        select([Review.c.content]).where(Review.c.movie_name == normalizedName)
    ).fetchall()

    if len(storedReviews) == 0:
        movieReviews = extractMovieReviews(normalizedName)

        Connection.execute(
            Movie.insert(),
            [{"name": normalizedName, "last_read_date": datetime.now()}],
        )
        Connection.execute(
            Review.insert(),
            [
                {"movie_name": normalizedName, "content": content}
                for content in movieReviews
            ],
        )
    else:
        storedMovie: tuple[datetime] = Connection.execute(
            select([Movie.c.last_read_date]).where(Movie.c.name == normalizedName)
        ).fetchone()
        lastReadDate = storedMovie[0]

        if (datetime.now() - lastReadDate).days > 2:
            movieReviews = extractMovieReviews(normalizedName)

            Connection.execute(
                Movie.update()
                .where(Movie.c.name == normalizedName)
                .values(last_read_date=datetime.now())
            )
            Connection.execute(
                Review.delete().where(Review.c.movie_name == normalizedName)
            )
            Connection.execute(
                Review.insert(),
                [
                    {"movie_name": normalizedName, "content": content}
                    for content in movieReviews
                ],
            )

        else:
            movieReviews = [review[0] for review in storedReviews]

    return movieReviews
