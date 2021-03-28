from datetime import datetime
from typing import Literal, Optional

movieReviewType = Literal["pos", "neg"]

classificationBagWords = dict[str, Literal[True]]

classifierPrediction = tuple[list[str], float, bool]

classifierTrainingSet = list[tuple[classificationBagWords, movieReviewType]]

storedMovieInfo = Optional[tuple[str, datetime, list[str]]]
