import asyncio

from flask import Flask

from model.dbModel import BaseEntity, Engine
from model.movieSentimentAnalysis import classifierPredict

app = Flask(__name__)


@app.route("/search/<movieName>")
def search(movieName: str):
    try:
        reviews, percentage, isDebounced = asyncio.run(classifierPredict(movieName))
        return {
            "positiveReviewPercentage": percentage,
            "isDebounced": isDebounced,
            "movieReviews": reviews,
        }
    except Exception as err:
        return {"error": err.args}


def main():
    BaseEntity.metadata.create_all(bind=Engine)
    app.run(debug=True, port=4000)


if __name__ == "__main__":
    main()
