def imdbFindUrl(movieSearchUrlRef: str) -> str:
    return "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + movieSearchUrlRef


def imdbMainUrl(href: str) -> str:
    return "https://www.imdb.com" + href


def normalizeMovieName(movieName):
    return movieName.lower()
