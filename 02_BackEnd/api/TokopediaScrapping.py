#!/usr/bin/env python
# coding: utf-8

# <h3>Extract data from <a href="https://www.tokopedia.com/">Tokopedia</a></h3>

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


# In[2]:


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
            time.sleep(SCROLL_PAUSE_TIME)

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
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return json.loads(soup.text)    

# Create function to generate query
def generate_query(query):
    query_space = query.replace(' ', '%20')
    return query_space

# Scraping setup and user credentials
from selenium.webdriver.chrome.service import Service
geckodriver_path = Service('/Users/admin/Downloads/geckodriver')

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
        if "rb" in x:
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

# Post to backend
import requests
import json
import http.client as httplib

# Total function
def tokped_scrap(queryId):
    # Get queries from front end
    platform = "Tokopedia"
    query = get_query(queryId)['query']
    searchLimit = int(get_query(queryId)['searchParam_tokopedia'])
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
        pmax = "&pmax="+str(price_max)
    else:
        pmax = ""

    if ~pd.isnull(price_min):
        pmin = "&pmin="+str(price_min)
    else:
        pmin = ""

    while True:
        if last_page == page_n:
            break
        if len(list_listing_names) >= limit_result:
            break

        url = "https://www.tokopedia.com/search?navsource="+pmax+pmin+"&page="+str(page_n)+"&q="+generate_query(query)+"&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product"
        response_type = 'html'
        get_response_ = get_response(url, response_type)
        last_page = page_n

        # Top ads
        try:
            response = BeautifulSoup(get_response_.select('div[data-testid*="topadsCPMWrapper"]')[0].decode_contents(), 'html.parser')

            # Get number of top ads
            ads = response.select('div[class*="css-kkkpmy"]')

            for ad in ads:
                index_ = ads.index(ad)

                # Get listing name
                try:
                    response_zoom = response.select('img[data-testid*="imgProduct"]')[index_]['alt']
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[0].decode_contents()
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
                    response_zoom = response.select('div[class*="css-1ksb19c"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[1].decode_contents()
                    list_listing_prices.append(response_zoom)
                except:
                    list_listing_prices.append(np.nan)

                # Get listing rating
                try:
                    response_zoom = response.select('span[class*="css-t70v7i"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[3].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[0].decode_contents()
                    list_listing_ratings.append(response_zoom)
                except:
                    list_listing_ratings.append(np.nan)

                # Get listing thumbnail photos
                try:
                    response_zoom = response.select('img[class*="css-1c345mg"]')[index_]['src']
                    list_listing_thumbnails.append(response_zoom)
                except:
                    list_listing_thumbnails.append(np.nan)

                # Get listing sold
                try:
                    response_zoom = response.select('span[class*="css-1duhs3e"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[3].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[2].decode_contents()
                    list_listing_solds.append(response_zoom)
                except:
                    list_listing_solds.append(np.nan)

                # Get seller location
                try:
                    response_zoom = response.select('div[class*="css-1rn0irl"]')[index_].decode_contents()
                    response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[1].decode_contents()
                    list_listing_locations.append(response_zoom)
                except:
                    list_listing_locations.append(np.nan)

                # Get listing reviews
                list_listing_reviews.append(np.nan)

                # Is Top Ads
                list_is_top_ads.append('Yes')

                # Get listing url
                try:
                    response_zoom = response.select('a[class*="info-content"]')[index_]['href']
                    list_listing_urls.append(response_zoom)
                except:
                    list_listing_urls.append(np.nan)
        except:
            pass

        # Normal ads
        try:
            response = BeautifulSoup(get_response_.select('div[data-testid*="divSRPContentProducts"]')[0].decode_contents(), 'html.parser')

            # Get number of top ads
            ads = response.select('div[class*="css-12sieg3"]')

            for ad in ads:
                index_ = ads.index(ad)

                # Get listing name
                try:
                    response_zoom = response.select('div[class*="css-svipq6"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[0].decode_contents()
                    list_listing_names.append(response_zoom)
                except:
                    list_listing_names.append(np.nan)

                # Get seller name
                try:
                    response_zoom = response.select('div[class*="css-1rn0irl"]')[index_].decode_contents()
                    response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[1].decode_contents()
                    list_seller_names.append(response_zoom)
                except:
                    list_seller_names.append(np.nan)

                # Get listing price
                try:
                    response_zoom = response.select('div[class*="css-1ksb19c"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[1].decode_contents()
                    list_listing_prices.append(response_zoom)
                except:
                    list_listing_prices.append(np.nan)

                # Get listing rating
                try:
                    response_zoom = response.select('span[class*="css-t70v7i"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[3].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[0].decode_contents()
                    list_listing_ratings.append(response_zoom)
                except:
                    list_listing_ratings.append(np.nan)

                # Get listing thumbnail photos
                try:
                    response_zoom = response.select('img[class*="css-1c345mg"]')[index_]['src']
                    list_listing_thumbnails.append(response_zoom)
                except:
                    list_listing_thumbnails.append(np.nan)

                # Get listing sold
                try:
                    response_zoom = response.select('span[class*="css-1duhs3e"]')[index_].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('div')[3].decode_contents()
                    # response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[2].decode_contents()
                    list_listing_solds.append(response_zoom)
                except:
                    list_listing_solds.append(np.nan)

                # Get seller location
                try:
                    response_zoom = response.select('div[class*="css-1rn0irl"]')[index_].decode_contents()
                    response_zoom = BeautifulSoup(response_zoom, 'html.parser').select('span')[0].decode_contents()
                    list_listing_locations.append(response_zoom)
                except:
                    list_listing_locations.append(np.nan)

                # Get listing reviews
                list_listing_reviews.append(np.nan)

                # Is Top Ads
                list_is_top_ads.append('No')

                # Get listing url
                try:
                    response_zoom = response.select('a[class*="info-content"]')[index_]['href']
                    list_listing_urls.append(response_zoom)
                except:
                    list_listing_urls.append(np.nan)

            page_n = page_n + 1
        except:
            pass
        
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
    df_result['platform'] = "Tokopedia"
    df_result['rating'] = pd.to_numeric(df_result['rating'].fillna("0"), errors='ignore')
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

