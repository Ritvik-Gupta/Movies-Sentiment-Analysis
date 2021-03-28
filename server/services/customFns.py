from typing import Optional

import joblib
from nltk.classify.naivebayes import NaiveBayesClassifier

from .customEnv import EnvConfig, castNonOptional


def imdbFindUrl(movieSearchUrlRef: str) -> str:
    return EnvConfig.IMDB_FIND_PATH + movieSearchUrlRef


def imdbMainUrl(href: str) -> str:
    return EnvConfig.IMDB_MAIN_PATH + href


def normalizeMovieName(movieName: str) -> str:
    return movieName.lower()


class ClassifierStorage:
    stored: Optional[NaiveBayesClassifier] = None

    @staticmethod
    def store(classifier: NaiveBayesClassifier) -> None:
        joblib.dump(classifier, EnvConfig.CLASSIFIER_STORAGE)

    @staticmethod
    async def load() -> NaiveBayesClassifier:
        if ClassifierStorage.stored == None:
            try:
                ClassifierStorage.stored = joblib.load(EnvConfig.CLASSIFIER_STORAGE)
            except Exception as err:
                raise Exception("Naive Bayes Model PKL file not Found", *err.args)
        return castNonOptional(ClassifierStorage.stored)
