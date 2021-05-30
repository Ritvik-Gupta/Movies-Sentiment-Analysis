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

    userCommentsElm = imdbMainPage.find("div", class_="user-comments")
    if userCommentsElm == None:
        raise Exception("Movie cannot be Found on IMDB", "User Comments Element Error")

    links: list[str] = []
    for link in userCommentsElm.find_all("a", href=True):
        links.append(link["href"])
    lastLink = links[-1]

    # driver = webdriver.Chrome("C:\\Users\\dell\\Desktop\\chromedriver.exe")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(imdbMainUrl(lastLink))
    for title in range(20):
        loadMoreButton = driver.find_element_by_class_name("load-more-data")
        loadMoreButton.click()
        time.sleep(1)
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
