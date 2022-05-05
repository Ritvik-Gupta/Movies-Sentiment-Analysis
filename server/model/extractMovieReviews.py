import time
from urllib.request import urlopen as openUrlWeb

from bs4 import BeautifulSoup
from selenium import webdriver
from services.customFns import imdbFindUrl, imdbMainUrl
from webdriver_manager.chrome import ChromeDriverManager


async def extractMovieReviews(movieName: str) -> list[str]:
    movieSearchUrlRef = movieName.replace(" ", "%20")

    imdbFindOpenUrl = openUrlWeb(imdbFindUrl(movieSearchUrlRef))
    imdbFindPage = BeautifulSoup(imdbFindOpenUrl, "lxml")

    resultTextElm = imdbFindPage.find("td", class_="result_text")
    if resultTextElm == None:
        raise Exception("Movie cannot be Found on IMDB", " Result Text Element Error")

    linkHref = resultTextElm.a["href"]
    imdbMainOpenUrl = openUrlWeb(imdbMainUrl(linkHref))
    imdbMainPage = BeautifulSoup(imdbMainOpenUrl, "lxml")

    reviewsHeaderLink = imdbMainPage.find(
        "div", attrs={"data-testid": "reviews-header"}
    )
    if reviewsHeaderLink == None:
        raise Exception(
            "Movie reviews cannot be found on IMDB",
            "User Reviews Header Link does not exist",
        )

    # driver = webdriver.Chrome("C:\\Users\\dell\\Desktop\\chromedriver.exe")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(imdbMainUrl(reviewsHeaderLink.a["href"]))
    for _ in range(20):
        try:
            loadMoreButton = driver.find_element_by_class_name("load-more-data")
            loadMoreButton.click()
            time.sleep(1)
        except:
            break
    driverPageSourceUrl = driver.page_source
    driverSourcePage = BeautifulSoup(driverPageSourceUrl, "lxml")

    listerListElm = driverSourcePage.find("div", class_="lister-list")
    if listerListElm == None:
        raise Exception("Movie cannot be Found on IMDB", " Lister List Element Error")

    listedTitles = listerListElm.find_all("a", class_="title")

    userReviews: list[str] = []
    for title in listedTitles:
        userReviews.append(title.text.replace("\n", ""))
    driver.quit()
    return userReviews
