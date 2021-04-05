from typing import Optional, TypeVar

from dotenv import dotenv_values

config = dotenv_values(".env")
T = TypeVar("T")


def castNonOptional(arg: Optional[T]) -> T:
    assert arg is not None
    return arg


class EnvConfig:
    CLASSIFIER_STORAGE = castNonOptional(config["CLASSIFIER_STORAGE"])
    SESSION_TIMEOUT = int(castNonOptional(config["MOVIE_SESSION_TIMEOUT"]))
    IMDB_FIND_PATH = castNonOptional(config["IMDB_FIND_PATH"])
    IMDB_MAIN_PATH = castNonOptional(config["IMDB_MAIN_PATH"])
    DATABASE_CONFIG_URL = castNonOptional(config["DATABASE_CONFIG_URL"])
