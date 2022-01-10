import time
from collections import defaultdict
import bs4
import pandas as pd
import selenium.webdriver as webd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pymysql
import sentiment_analysis


def webscrape(airline):
    """ Input: airline: text used to go to reviews website for particular airline
    Output: reviews: list of HTML segments that contains all relevant review information """
    reviews = []
    browser = webd.Chrome(executable_path="C:/chromeDriver/chromedriver.exe")

    for page_num in range(1, 50):
        url = f'http://www.airlinequality.com/airline-reviews/{airline}/page/{page_num}/?sortby=post_date%3ADesc&pagesize=100'
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if soup.select('div.col-content article article.list-item'):
            reviews.append(soup.select('div.col-content article article.list-item'))
        else:
            break

    return reviews


def parse_review(review: bs4.element.Tag) -> dict:
    """
    Input: review: HTML segment that contains all relevant review information
    Output: d: dictionary of relevant review information
    """

    d = {}
    if review.select_one("div.rating-10 span"):
        d['rating'] = int(review.select_one("div.rating-10 span").text)
    d['headline'] = review.select_one("h2.text_header").text
    try:
        d['country'] = review.select_one('h3.text_sub_header').text\
            .replace(')', '(').split('(')[1]
    except IndexError:
        d['country'] = 'None'
    d['body'] = review.select_one("div.text_content").text.strip()
    rows = review.select('tr')
    for row in rows:
        if row.select('td')[1].attrs['class'][0] == 'review-rating-stars':
            for x in row.select('span'):
                try:
                    if x.attrs['class'] == ['star', 'fill']:
                        num = int(x.text)
                        d[row.td.attrs['class'][1]] = num
                except KeyError:
                    continue
        else:
            d[row.td.attrs['class'][1]] = row.select('td')[1].text
    return d


def webscrape_manager(airline_list):
    """
    Input: airline_list: list of airline names as strings
    Output: webscrape_info_dict: dictionary with keys as airline names and values as webscraped html code
    """
    webscrape_info_dict = {}

    for airline in airline_list:
        webscrape_info_dict[airline] = webscrape(airline)

    return webscrape_info_dict


def review_parser(airline_list, webscrape_info_dict):
    """
    Input: airline_list: list of airline names as strings
    webscrape_info_dict: dictionary with keys as airline names and values as webscraped html code
    Output: airline_dict: dictionary with keys as airline names and values as their respective reviews
    """
    airline_dict = defaultdict(list)
    i = 0
    for reviews in webscrape_info_dict.values():
        for review in reviews:
            for r in review:
                airline_dict[airline_list[i]].append(parse_review(r))
        i += 1
    return airline_dict


def copy_to_sql(airline_list, airline_dict, engine):
    """
    Input: airline_list: list of airline names as strings
    airline_dict: dictionary with keys as airline names and values as their respective reviews
    engine: directory to SQL database to store webscraped review data
    """
    for airline in airline_list:
        pd.DataFrame(airline_dict[airline]).to_sql(airline.split('-')[0], con=engine)


def getReviews(airline, engine):
    airline_list = [airline]
    webscrape_info_dict = webscrape_manager(airline_list)
    airline_dict = review_parser(airline_list, webscrape_info_dict)
    copy_to_sql(airline_list, airline_dict, engine)