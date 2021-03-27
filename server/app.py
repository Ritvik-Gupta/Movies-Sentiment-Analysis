from typing import Literal

from flask import Flask

from movieSentimentAnalysis import classifierTrainingTesting, classifierPredict

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
