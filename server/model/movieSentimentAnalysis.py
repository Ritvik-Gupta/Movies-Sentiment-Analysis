# import nltk

# nltk.download("punkt")
# nltk.download("movie_reviews")
# nltk.download("stopwords")

import asyncio
from random import shuffle
from services.customFns import loadClassifier
from string import punctuation as stringPunctuations

import joblib
from nltk import NaiveBayesClassifier, classify
from nltk import word_tokenize as tokenizeWord
from nltk.corpus import movie_reviews as movieReviewsCorpus
from nltk.corpus import stopwords
from services.customTypes import *

from .debounceMovieInfo import debounceMovieInfo

from services.customEnv import EnvConfig


def classifierBagWords(words: list[str]) -> classificationBagWords:
    global stop_words
    stop_words = stopwords.words("english")
    classificationBag: classificationBagWords = {}
    for word in words:
        if not (word in stop_words or word in stringPunctuations):
            classificationBag[word] = True
    return classificationBag


def classifierTrainingTesting() -> None:
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

    test_set = positiveReviewSet[:200] + negativeReviewSet[:200]
    train_set = positiveReviewSet[200:] + negativeReviewSet[200:]

    classifier = NaiveBayesClassifier.train(train_set)
    classifierAccuracy = classify.accuracy(classifier, test_set)
    print("Classifier Accuracy :\t", classifierAccuracy)
    joblib.dump(classifier, EnvConfig.CLASSIFIER_STORAGE)


async def classifierPredict(movieName: str) -> classifierPrediction:
    gatherRequest = asyncio.gather(debounceMovieInfo(movieName), loadClassifier())
    (movieReviews, isDebounced), classifier = await gatherRequest

    tokens: list[list[str]] = []
    for review in movieReviews:
        tokens.append(tokenizeWord(review))

    set_testing: list[classificationBagWords] = []
    for review in tokens:
        set_testing.append(classifierBagWords(review))

    classification: list[movieReviewType] = []
    for review in set_testing:
        classification.append(classifier.classify(review))

    totalPositiveReviews = classification.count("pos")
    positiveReviewPercentage = 100 * totalPositiveReviews / len(classification)

    return movieReviews, positiveReviewPercentage, isDebounced


# classifierTrainingTesting()

# movieName = input("Enter name of movie:")
# filmReviews, positiveReviewPercentage = classifierPredict(movieName)
# print(
#     "The film {} has got {} percent positive reviews".format(
#         movieName, positiveReviewPercentage
#     )
# )
# if positive_per > 60:
#     print("overall impression of movie is good")
# else:
#     print("overall impression of movie is bad")
