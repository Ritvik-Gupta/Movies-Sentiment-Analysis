from flask import Flask

from dbModel import Engine, Movie
from movieSentimentAnalysis import classifierPredict, classifierTrainingTesting

app = Flask(__name__)


@app.route("/search/<movieName>")
def search(movieName: str):
    try:
        movieReviews, positiveReviewPercentage, isDebounced = classifierPredict(
            movieName
        )
        return {
            "positiveReviewPercentage": positiveReviewPercentage,
            "isDebounced": isDebounced,
            "movieReviews": movieReviews,
        }
    except Exception as err:
        return {"error": err.args}


def main():
    classifierTrainingTesting()
    app.run(debug=True)


if __name__ == "__main__":
    main()
