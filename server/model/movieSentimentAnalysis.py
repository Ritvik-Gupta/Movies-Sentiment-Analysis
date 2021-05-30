# import nltk

# nltk.download("punkt")
# nltk.download("movie_reviews")
# nltk.download("stopwords")

import asyncio
from random import shuffle
from string import punctuation as stringPunctuations

from nltk import NaiveBayesClassifier, classify
from nltk import word_tokenize as tokenizeWord
from nltk.corpus import movie_reviews as movieReviewsCorpus
from nltk.corpus import stopwords
from services.customFns import ClassifierStorage
from services.customTypes import (
    classificationBagWords,
    classifierPrediction,
    classifierTrainingSet,
    movieReviewType,
)

from .debounceMovieInfo import debounceMovieInfo

englishStopwords = stopwords.words("english")


def classifierBagWords(words: list[str]) -> classificationBagWords:
    classificationBag: classificationBagWords = {}
    for word in words:
        if not (word in englishStopwords or word in stringPunctuations):
            classificationBag[word] = True
    return classificationBag


def classifierTrainingTesting() -> tuple[NaiveBayesClassifier, float]:
    positiveReviewSet: classifierTrainingSet = []
    negativeReviewSet: classifierTrainingSet = []

    for fileid in movieReviewsCorpus.fileids("pos"):
        positiveReview = movieReviewsCorpus.words(fileid)
        positiveReviewSet.append((classifierBagWords(positiveReview), "pos"))
    shuffle(positiveReviewSet)

    for fileid in movieReviewsCorpus.fileids("neg"):
        negativeReview = movieReviewsCorpus.words(fileid)
        negativeReviewSet.append((classifierBagWords(negativeReview), "neg"))
    shuffle(negativeReviewSet)

    trainSet = positiveReviewSet[200:] + negativeReviewSet[200:]
    testSet = positiveReviewSet[:200] + negativeReviewSet[:200]

    classifier = NaiveBayesClassifier.train(trainSet)
    classifierAccuracy = classify.accuracy(classifier, testSet)

    return classifier, classifierAccuracy


async def classifierPredict(movieName: str) -> classifierPrediction:
    (movieReviews, fetchState), classifier = await asyncio.gather(
        debounceMovieInfo(movieName), ClassifierStorage.load()
    )

    tokens: list[list[str]] = []
    for review in movieReviews:
        tokens.append(tokenizeWord(review))

    classifiedBagWords: list[classificationBagWords] = []
    for review in tokens:
        classifiedBagWords.append(classifierBagWords(review))

    classification: list[movieReviewType] = []
    for review in classifiedBagWords:
        classification.append(classifier.classify(review))

    totalPositiveReviews = classification.count("pos")
    positiveReviewPercentage = 100 * totalPositiveReviews / len(classification)

    return movieReviews, positiveReviewPercentage, fetchState
