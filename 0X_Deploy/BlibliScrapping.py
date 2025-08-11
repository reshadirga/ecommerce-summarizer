#!/usr/bin/env python
# coding: utf-8

# <h3>Extract data from <a href="https://www.blibli.com/">Blibli</a></h3>

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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
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

# Create function to get response
def get_response(url, response_type):
    if response_type == 'html':
        options = Options()
        options.add_argument("-remote-debugging-port=9224")
        options.add_argument("-headless")
        options.add_argument("-disable-gpu")
        options.add_argument("-no-sandbox")
        options.add_argument("--width=2560")
        options.add_argument("--height=1440")
        binary = FirefoxBinary(os.environ.get("FIREFOX_BIN"))
        driver = webdriver.Firefox(firefox_binary=binary, options=options, executable_path=os.environ.get("GECKODRIVER_PATH"))
        driver.get(url)
        delay = 3 # seconds

        # Scroll to bottom
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            print("Page is ready!")

        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    elif response_type == 'json':
        headers = {
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        return json.loads(response.text)

# Create function to generate query
def generate_url_json(page_n, query):
    query_space = query.replace(' ', '%20')
    return "https://www.blibli.com/backend/search/products?sort=&page="+str(page_n)+"&start="+str(page_n*40)+"&searchTerm="+query_space+"&intent=true&merchantSearch=true&multiCategory=true&customUrl=&&channelId=mobile-web&showFacet=false&userIdentifier=657116261.U.194952598446124.1659512226&isMobileBCA=false"

# Create function to generate listing url
def generate_listing_url(url):
    return "https://www.blibli.com"+url

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

# Post to backend
import requests
import json
import http.client as httplib

# Total function
def blibli_scrap(queryId):
    # Get queries from front end
    platform = "Blibli"
    print('searching query:', queryId)
    query = get_query(queryId)['query']
    searchLimit = int(get_query(queryId)['searchParam_blibli'])
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

    # Setup scraping condition
    limit_result = searchLimit
    df_result = pd.DataFrame()

    while len(df_result) < limit_result:

        obtained = len(df_result)

    #     Get responses
        url = generate_url_json(page_n, query)
        responses = get_response(url, 'json')
        
        try:
            print(responses['data']['products'])

            for response in responses['data']['products']:

                # Get listing name
                list_listing_names.append(response['name'])

                # Get seller name
                list_seller_names.append(response['merchantCode'])

                # Get listing prices
                list_listing_prices.append(response['price']['priceDisplay'])

                # Get listing ratings
                list_listing_ratings.append(response['review']['rating'])

                # Get listing thumbnails
                list_listing_thumbnails.append(response['images'][0])

                # Get listing solds
                try:
                    list_listing_solds.append(response['soldRangeCount']['id'])
                except:
                    list_listing_solds.append(0)

                # Get listing locations
                list_listing_locations.append(response['location'])

                # Get listing reviews
                list_listing_reviews.append(response['review']['count'])

                # Get is top ads
                list_is_top_ads.append('')

                # Get listing urls
                list_listing_urls.append(generate_listing_url(response['url']))

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

        if obtained == len(df_result):
            break

        df_result['price_min'] = [get_min_price(x) for x in df_result['price_display']]
        df_result['price_max'] = [get_max_price(x) for x in df_result['price_display']]

        if price_min != "":
            if price_max != "":
                df_result = df_result[(df_result['price_min'] >= int(price_min)) & (df_result['price_max'] <= int(price_max))]
            else:
                df_result = df_result[df_result['price_min'] >= int(price_min)]
        elif price_max != "":
            df_result = df_result[df_result['price_max'] <= int(price_max)]

    df_result = df_result[:limit_result]
    
    df_result['currency'] = "IDR"
    df_result['platform'] = "Blibli"
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

