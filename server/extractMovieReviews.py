import time
from urllib.request import urlopen as openUrlWeb

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from customFns import imdbFindUrl, imdbMainUrl


def extractMovieReviews(movieName: str) -> list[str]:
    movieSearchUrlRef = movieName.replace(" ", "%20")

    imdbFindOpenUrl = openUrlWeb(imdbFindUrl(movieSearchUrlRef))
    imdbFindPage = BeautifulSoup(imdbFindOpenUrl, "lxml")
    resultTextElm = imdbFindPage.find("td", class_="result_text")
    linkHref = resultTextElm.a["href"]

    imdbMainOpenUrl = openUrlWeb(imdbMainUrl(linkHref))
    imdbMainPage = BeautifulSoup(imdbMainOpenUrl, "lxml")
    userCommentsElm = imdbMainPage.find("div", class_="user-comments")

    links: list[str] = []
    for link in userCommentsElm.find_all("a", href=True):
        links.append(link["href"])
    lastLink = links[-1]

    # driver = webdriver.Chrome("C:\\Users\\dell\\Desktop\\chromedriver.exe")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(imdbMainUrl(lastLink))
    for pos in range(20):
        try:
            loadMoreButton = driver.find_element_by_class_name("load-more-data")
            loadMoreButton.click()
            time.sleep(1)
        except Exception as err:
            print("An Exception Occured :\t", err)
            break
    driverPageSourceUrl = driver.page_source
    driverSourcePage = BeautifulSoup(driverPageSourceUrl, "lxml")

    listerListElm = driverSourcePage.find("div", class_="lister-list")

    e1 = listerListElm.find_all("a", class_="title")

    user_reviews: list[str] = []
    for pos in e1:
        raw = pos.text
        user_reviews.append(raw.replace("\n", ""))
    driver.quit()
    return user_reviews


# reviews()
