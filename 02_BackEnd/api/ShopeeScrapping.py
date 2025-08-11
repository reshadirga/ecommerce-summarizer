#!/usr/bin/env python
# coding: utf-8

# <h3>Extract data from <a href="https://www.shopee.co.id/">Shopee</a></h3>

# In[1]:


# Install dependencies
# !pip install pandas
# !pip install beautifulsoup4
# !pip install selenium

# Load dependencies
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import json
import time
import re

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os

# Create function to get url queries from front end
import requests

def get_query(queryId):
    url = "https://parseapi.back4app.com/classes/Queries/"+queryId
    headers = {
        "X-Parse-Application-Id": "RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI",
        "X-Parse-Rest-Api-Key": "7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU"
      }
    r = requests.get(url, headers=headers)
    return r.json()

# Setup scraping condition
from selenium.webdriver.chrome.service import Service
geckodriver_path = Service('/Users/admin/Downloads/geckodriver')

# Create function to get response
def get_response(url, response_type):
    if response_type == 'html':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--width=2560")
        chrome_options.add_argument("--height=1440")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get(url)

        # Scroll to bottom
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.clientHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.clientHeight);")

            # Wait to load page
            ads = []
            total_ads = -999
            while total_ads < len(ads):
                total_ads = len(ads)
                time.sleep(SCROLL_PAUSE_TIME)
                html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                soup = BeautifulSoup(html, 'html.parser')
                ads = soup.select('div[class*="VTjd7p"]')

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.clientHeight")
            if new_height == last_height:
                break
            last_height = new_height

            print("Page is ready!")

        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        driver.close()
        return soup
    
    elif response_type == 'json':
        headers = {
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        return json.loads(response.text)

# Create function to generate query
def generate_query(query):    
    return query.replace(' ', '%20')

def generate_url_json(page_n, query, price_max, price_min):

    if ~pd.isnull(price_max):
        pmax = "&price_max="+str(price_max)
    else:
        pmax = ""

    if ~pd.isnull(price_min):
        pmin = "&price_min="+str(price_min)
    else:
        pmin = ""
    
    query_space = query.replace(' ', '%20')
    
    return "https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword="+query_space+"&limit=60&newest="+str(page_n*60)+"&order=desc&page_type=search"+pmax+pmin+"&scenario=PAGE_GLOBAL_SEARCH&version=2"

# Create function to generate thumbnail link
def generate_listing_thumbnail(image):
    return "cf.shopee.co.id/file/"+image+"_tn"

# Create function to generate listing url
def generate_listing_url(name, shopid, itemid):
    name = re.sub('[^A-Za-z0-9]+', '-', name)
    return "https://shopee.co.id/"+name+"-i."+str(shopid)+"."+str(itemid)

def get_price_display(x):
    try:
        list_ = x.prettify().split('\n')
        result = []
        for element in list_:
            if "<" not in element:
                element = element.replace(" ","")
                result.append(element)
            
        return ''.join(result)
    except:
        return np.nan

def get_sold(x):
    try:
        if "RB" in x:
            x_split = x.split(',')
            first = int(''.join(re.findall("\d+", x_split[0])))
            try:
                second = int(''.join(re.findall("\d+", x_split[1])))
            except:
                second = 0

            result = first*1000 + second*100

        else:
            result = int(''.join(re.findall("\d+", x)))
    
        return result
    
    except:
        return (np.nan)
    
def get_review(x):
    try:
        return int(''.join(re.findall("\d+", x)))
    except:
        return (np.nan)

def get_min_price(x):
    try:
        min_price = x.split("-")[0]
        return int(''.join(re.findall("\d+", min_price)))
    except:
        return(np.nan)

def get_max_price(x):
    try:
        max_price = x.split("-")[1]
        return int(''.join(re.findall("\d+", max_price)))
    except:
        return(get_min_price(x))

def get_sold(x):
    try:
        return int(''.join(re.findall("\d+", x)))
    except:
        return (np.nan)

def get_review(x):
    try:
        return int(''.join(re.findall("\d+", x)))
    except:
        return (np.nan)

def summarise(df):
    cheapest = df['price_min'].min()
    expensive = df['price_max'].max()
    most_sold = df['sold'].max()
    most_rated = df['review'].max()
    
    if len(df['review']) - df['review'].isna().sum() != 0:
        df['top_rated'] = df['rating'] * df['review']
    else:
        df['top_rated'] = df['rating'] * df['sold']
        
    top_rated = df['top_rated'].max()
    
    cheap = df.index[df['price_min'] == cheapest].tolist()
    expensive = df.index[df['price_max'] == expensive].tolist()
    sold = df.index[df['sold'] == most_sold].tolist()
    rated = df.index[df['review'] == most_rated].tolist()
    top = df.index[df['top_rated'] == top_rated].tolist()
    
    cheap = get_top_rated_also(df, cheap)
    expensive = get_top_rated_also(df, expensive)
    sold = get_top_rated_also(df, sold)
    rated = get_top_rated_also(df, rated)
    top = get_cheap_also(df, top)
    
    ad_cheap = df.loc[cheap].reset_index().to_json(orient='index')
    ad_expensive = df.loc[expensive].reset_index().to_json(orient='index')
    ad_sold = df.loc[sold].reset_index().to_json(orient='index')
    ad_rated = df.loc[rated].reset_index().to_json(orient='index')
    ad_top = df.loc[top].reset_index().to_json(orient='index')
    
    df_summary = {
        'cheap': ad_cheap,
        'expensive': ad_expensive,
        'sold': ad_sold,
        'rated': ad_rated,
        'top': ad_top
    }

    return json.loads(json.dumps(df_summary, indent=4))
    
    
def get_top_rated_also(df, indexes):
    if len(indexes) <= 1:
        return indexes
    else:
        top_rated = df[df.index.isin(indexes)]['top_rated'].max()
        return [df.index[df['top_rated'] == top_rated].tolist()[0]]
    
def get_cheap_also(df, indexes):
    if len(indexes) <= 1:
        return indexes
    else:
        cheapest = df[df.index.isin(indexes)]['price_min'].min()
        return [df.index[df['price_min'] == cheapest].tolist()[0]]

# Total function
def shopee_scrap(queryId):
    # Get queries from front end
    platform = "Shopee"
    query = get_query(queryId)['query']
    searchLimit = int(get_query(queryId)['searchParam_shopee'])
    price_max = get_query(queryId)['price_max']
    price_min = get_query(queryId)['price_min']
    
    # Get individual listing informations on parent page
    list_listing_names = []
    list_seller_names = []
    list_listing_prices = []
    list_listing_ratings = []
    list_listing_thumbnails = []
    list_listing_solds = []
    list_listing_locations = []
    list_listing_reviews = []
    list_is_top_ads = []
    list_listing_urls = []

    page_n = 0
    last_page = -999
    limit_result = searchLimit

    if ~pd.isnull(price_max):
        pmax = "&maxPrice="+str(price_max)
    else:
        pmax = ""

    if ~pd.isnull(price_min):
        pmin = "&minPrice="+str(price_min)
    else:
        pmin = ""

    while True:
        if last_page == page_n:
            break
        if len(list_listing_names) >= limit_result:
            break

        url = "https://shopee.co.id/search?keyword="+generate_query(query)+pmax+pmin+"&noCorrection=true&page="+str(page_n)
        response_type = 'html'
        get_response_ = get_response(url, response_type)
        last_page = page_n

        # Top ads
        response = BeautifulSoup(get_response_.select('div[class*="shopee-search-item-result"]')[0].decode_contents(), 'html.parser')

        # Get number of top ads
        ads = response.select('div[class*="shopee-search-item-result__item"]')

        for ad in ads:
            index_ = ads.index(ad)

            # Get listing name
            try:
                response_zoom = response.select('div[class*="Cve6sh"]')[index_].decode_contents()
                list_listing_names.append(response_zoom)
            except:
                list_listing_names.append(np.nan)

            # Get seller name
            try:
                response_zoom = response.select('span[class*="css-1kurdsh"]')[0].decode_contents()
                list_seller_names.append(response_zoom.split('/>')[1])
            except:
                list_seller_names.append(np.nan)

            # Get listing price
            try:
                response_zoom = response.select('div[class*="rVLWG6"]')[index_]
                list_listing_prices.append(response_zoom)
            except:
                list_listing_prices.append(np.nan)

            # Get listing rating
            try:
                rating = []
                response_zoom = response.select('div[data-sqe*="rating"]')[index_].decode_contents()
                response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div[class*="shopee-rating-stars__lit"]')
                for response_zoom_ in response_zoom:
                    percentage_rate = response_zoom_['style']
                    percentage_rate = str(percentage_rate).split(": ")[1]
                    rating.append(float((percentage_rate).strip(";%"))/100)
                list_listing_ratings.append(round(sum(rating),2))
            except:
                list_listing_ratings.append(np.nan)

            # Get listing thumbnail photos
            try:
                response_zoom = response.select('img[class*="vc8g9F"]')[index_]['src']
                list_listing_thumbnails.append(response_zoom)
            except:
                list_listing_thumbnails.append(np.nan)

            # Get listing sold
            try:
                response_zoom = response.select('div[class*="uEPGHT"]')[index_].decode_contents()
                list_listing_solds.append(response_zoom)
            except:
                list_listing_solds.append(np.nan)

            # Get seller location
            try:
                response_zoom = response.select('div[class*="zGGwiV"]')[index_].decode_contents()
                list_listing_locations.append(response_zoom)
            except:
                list_listing_locations.append(np.nan)

            # Get listing reviews
            list_listing_reviews.append(np.nan)

            # Is Top Ads
            list_is_top_ads.append(np.nan)

            # Get listing url
            try:
                response_zoom = response.select('a[data-sqe*="link"]')[index_]['href']
                list_listing_urls.append("https://shopee.co.id/"+response_zoom)
            except:
                list_listing_urls.append(np.nan)

            page_n = page_n + 1

    
    # Prepare dataset for posting to backend
    # Consolidate result on a list    
    result = {
        'title': list_listing_names,
        'seller': list_seller_names,
        'price_display': list_listing_prices,
        'rating': list_listing_ratings,
        'thumbnail': list_listing_thumbnails,
        'sold': list_listing_solds,
        'location': list_listing_locations,
        'review': list_listing_reviews,
        'is_top_ads': list_is_top_ads,
        'url': list_listing_urls

    }

    df_result = pd.DataFrame(result)
    df_result = df_result[:limit_result]

    df_result['currency'] = "IDR"
    df_result['platform'] = "Shopee"
    df_result['rating'] = pd.to_numeric(df_result['rating'].fillna("0"), errors='ignore')
    df_result['price_display'] = [get_price_display(x) for x in df_result['price_display']]
    df_result['price_min'] = [get_min_price(x) for x in df_result['price_display']]
    df_result['price_max'] = [get_max_price(x) for x in df_result['price_display']]
    df_result['sold'] = [pd.to_numeric(get_sold(x), errors = 'coerce') for x in df_result['sold']]
    df_result['review'] = [pd.to_numeric(get_review(x), errors = 'coerce') for x in df_result['review']]

    df_result['title'] = df_result['title'].astype(pd.StringDtype())
    df_result['seller'] = df_result['seller'].astype(pd.StringDtype())
    df_result['price_display'] = df_result['price_display'].astype(pd.StringDtype())
    df_result['thumbnail'] = df_result['thumbnail'].astype(pd.StringDtype())
    df_result['location'] = df_result['location'].astype(pd.StringDtype())
    df_result['is_top_ads'] = df_result['is_top_ads'].astype(pd.StringDtype())
    df_result['url'] = df_result['url'].astype(pd.StringDtype())
    df_result['currency'] = df_result['currency'].astype(pd.StringDtype())
    df_result['platform'] = df_result['platform'].astype(pd.StringDtype())
    
    # Post to backend
    import requests
    import json
    import http.client as httplib

    # connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    # connection.connect()

    # df_result_min = df_result.to_json(orient="index")

    # json_data = {
    #     'queryId': queryId,
    #     'platform': platform,
    #     'ScrapRes': df_result_min
    # }

    # connection.request('POST', '/classes/ScrapResMin', json.dumps(
    #         json_data
    #      ), {
    #         'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
    #         'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU',
    #         'Content-Type': 'application/json'
    #      })
    
    return {
        'summary': summarise(df_result),
        'df': df_result
        }

