from services.customEnv import EnvConfig
from .customEnv import EnvConfig

import joblib
from nltk.classify.naivebayes import NaiveBayesClassifier


def imdbFindUrl(movieSearchUrlRef: str) -> str:
    return EnvConfig.IMDB_FIND_PATH + movieSearchUrlRef


def imdbMainUrl(href: str) -> str:
    return EnvConfig.IMDB_MAIN_PATH + href


def normalizeMovieName(movieName: str) -> str:
    return movieName.lower()


def storeClassifier(classifier: NaiveBayesClassifier) -> None:
    joblib.dump(classifier, EnvConfig.CLASSIFIER_STORAGE)


async def loadClassifier() -> NaiveBayesClassifier:
    return joblib.load(EnvConfig.CLASSIFIER_STORAGE)
