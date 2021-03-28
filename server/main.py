from model.movieSentimentAnalysis import classifierTrainingTesting
from services.customFns import ClassifierStorage


classifier, classifierAccuracy = classifierTrainingTesting()
ClassifierStorage.store(classifier)
print("Classifier Accuracy :\t", classifierAccuracy)
