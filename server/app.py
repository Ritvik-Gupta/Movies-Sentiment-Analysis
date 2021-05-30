import asyncio

from flask import Flask
from flask_cors import CORS

from model.dbModel import BaseEntity, Engine
from model.movieSentimentAnalysis import classifierPredict
from services.customFns import ClassifierStorage

app = Flask(__name__)
cors = CORS(app, resources={r"/search/*": {"origins": "*"}})


@app.route("/search/<movieName>")
def search(movieName: str):
    try:
        reviews, percentage, fetchState = asyncio.run(classifierPredict(movieName))

        if percentage > 60:
            message = "Good"
        elif percentage > 50:
            message = "Average"
        elif percentage > 40:
            message = "Below Average"
        else:
            message = "Bad"

        return {
            "positiveReviewPercentage": percentage,
            "fetchState": fetchState,
            "movieReviews": reviews,
            "message": message,
        }
    except Exception as err:
        return {"error": err.args}


async def main():
    BaseEntity.metadata.create_all(bind=Engine)
    await ClassifierStorage.load()
    app.run(debug=True, port=4000)


if __name__ == "__main__":
    asyncio.run(main())
