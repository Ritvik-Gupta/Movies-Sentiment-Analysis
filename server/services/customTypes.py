from datetime import datetime
from typing import Literal, Optional

fetchStateInfo = Literal["Scraped from Web", "Read from Cache", "Refectched and Cached"]

debouncedMovieStateInfo = tuple[list[str], fetchStateInfo]

movieReviewType = Literal["pos", "neg"]

classificationBagWords = dict[str, bool]

classifierPrediction = tuple[list[str], float, fetchStateInfo]

classifierTrainingSet = list[tuple[classificationBagWords, movieReviewType]]

storedMovieInfo = Optional[tuple[str, datetime, list[str]]]
