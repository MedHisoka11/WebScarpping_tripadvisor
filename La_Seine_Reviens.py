import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def get_all_pages():

    urls=['https://www.tripadvisor.fr/Attraction_Review-g187147-d189683-Reviews-Seine_River-Paris_Ile_de_France.html']

    for i in range(10,5456,10):
        url=f"https://www.tripadvisor.fr/Attraction_Review-g187147-d189683-Reviews-or{i}-Seine_River-Paris_Ile_de_France.html"
        urls.append(url)
    return urls

data = []
def parse_reviews(url):
    driver = webdriver.Chrome()
    driver.get(url)

    driver.implicitly_wait(10)

    # Obtenez le contenu de la page
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    reviews = soup.find_all("div", class_="_c")

    for review in reviews:
        rev = review.find("span", class_="JguWG").text
        rating = float(review.find("svg", class_="UctUV d H0")['aria-label'].split(" ")[0].strip().replace(',', '.'))

        data.append({
            "review": rev,
            "rating": rating
        })
    return data


def parse_all_reviews():
    pages=get_all_pages()
    for page in pages:
        parse_reviews(url=page)
        print(f'On scrape {page}')

parse_all_reviews()

df=pd.DataFrame(data)

df.to_csv('./La_Seine_Reviews.csv',index=False)
#r = requests.get('https://www.tripadvisor.fr/Attraction_Review-g187147-d189683-Reviews-Seine_River-Paris_Ile_de_France.html')
#print(r.status_code)