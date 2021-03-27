from flask import Flask

from dbModel import Engine, Movie, Review
from movieSentimentAnalysis import classifierPredict, classifierTrainingTesting

app = Flask(__name__)


@app.route("/search/<movieName>")
def search(movieName: str):
    movieReviews, positiveReviewPercentage = classifierPredict(movieName)
    return {
        "movieReviews": movieReviews,
        "positiveReviewPercentage": positiveReviewPercentage,
    }


def main():
    classifierTrainingTesting()
    app.run(debug=True)


if __name__ == "__main__":
    main()
