import nltk

from model.movieSentimentAnalysis import classifierTrainingTesting
from services.customFns import ClassifierStorage

nltk.download("punkt")
nltk.download("movie_reviews")
nltk.download("stopwords")


classifier, classifierAccuracy = classifierTrainingTesting()
ClassifierStorage.store(classifier)
print("Classifier Accuracy :\t", classifierAccuracy)
