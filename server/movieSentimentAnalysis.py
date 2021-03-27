# import nltk

# nltk.download("punkt")
# nltk.download("movie_reviews")
# nltk.download("stopwords")

from random import shuffle
from string import punctuation as stringPunctuations

import joblib
from nltk import NaiveBayesClassifier, classify
from nltk import word_tokenize as tokenizeWord
from nltk.corpus import movie_reviews as movieReviews
from nltk.corpus import stopwords

from debounceMovieInfo import debounceMovieInfo
from customTypes import *


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

    for fileid in movieReviews.fileids("pos"):
        positiveReview = movieReviews.words(fileid)
        positiveReviewSet.append((classifierBagWords(positiveReview), "pos"))
    shuffle(positiveReviewSet)

    for fileid in movieReviews.fileids("neg"):
        negativeReview = movieReviews.words(fileid)
        negativeReviewSet.append((classifierBagWords(negativeReview), "neg"))
    shuffle(negativeReviewSet)

    test_set = positiveReviewSet[:200] + negativeReviewSet[:200]
    train_set = positiveReviewSet[200:] + negativeReviewSet[200:]

    classifier = NaiveBayesClassifier.train(train_set)
    classifierAccuracy = classify.accuracy(classifier, test_set)
    print(classifierAccuracy)
    joblib.dump(classifier, "imdb_movies_reviews.pkl")


def classifierPredict(movieName: str) -> classifierPrediction:
    classifier = joblib.load("imdb_movies_reviews.pkl")
    movieReviews, isDebounced = debounceMovieInfo(movieName)

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
