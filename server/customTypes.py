from typing import Literal

movieReviewType = Literal["pos", "neg"]

classificationBagWords = dict[str, Literal[True]]

classifierPrediction = tuple[list[str], float, bool]

classifierTrainingSet = list[tuple[classificationBagWords, movieReviewType]]
