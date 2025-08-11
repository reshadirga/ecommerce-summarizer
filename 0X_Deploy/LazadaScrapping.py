#!/usr/bin/env python
# coding: utf-8

# <h3>Extract data from <a href="https://www.lazada.co.id/">Lazada</a></h3>

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
#         options.headless = True
        options.add_argument("--width=2560")
        options.add_argument("--height=1440")
        options.add_argument("--incognito")
        options.add_argument("--single-process")
        options.add_argument("--no-sandbox")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Firefox(options=options, service=geckodriver_path)
        driver.get(url)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, 'html.parser')

        delay = 30 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '_17mcb')))

            print("Page is ready!")
            
        except TimeoutException:
            print("Loading took too much time!")
            driver.close()

        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        driver.close()
        return soup
    
    elif response_type == 'json':
        
        cookies = {
            "__wpkreporterwid_": "3a462388-e175-4795-bc99-1703c146274a",
            "_bl_uid": "q6l1L73Rzeeft0fC9k8wjbsgXqyI",
            "_tb_token_": "57533e367517e",
            "cna": "1LWmG4Oo/hICAZ61R1lONIm9",
            "hng": "ID|id-ID|IDR|360",
            "hng.sig": "dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ",
            "isg": "BJqaNSQyrYoHSyEmE1HiPYaI6Ea8yx6lOa7utaQTRi34FzpRjFtutWBh53uL3JY9",
            "l": "eBEgqrmmTEDTD2DvmOfahurza77OSIOYYuPzaNbMiOCPO95p5SjFW6kHBPT9C36NhsOvR3J-P9DHBeYBcIDjLbHEAjH5SNDmn",
            "lzd_cid": "3361bcaa-7fea-461a-9cf9-e0a0ad2c3423",
            "lzd_sid": "12f9e528f9823b7000c26329401b3ccf",
            "t_fv": "1663027155350",
            "t_sid": "CCZWNZ0ua1L2CfxDStBTm6VvnoHxDiZd",
            "t_uid": "3361bcaa-7fea-461a-9cf9-e0a0ad2c3423",
            "tfstk": "cPc1BRMBimhEhK5VkVTeboCQQLPRZkC_8FZn5H7RhvxduugCiV1zVJzIoMeTty1..",
            "utm_channel": "NA",
            "x5sec": "7b22617365727665722d6c617a6164613b32223a223637333039396131643932666538323033346630666636623434336237616363434e65502f356747454e6e703137533738634b67614443633463657941304144227d",
            "xlly_s": "1"
        }
        
        response = requests.get(url, cookies=cookies)
        return json.loads(response.text)

# Setup scraping condition
from selenium.webdriver.firefox.service import Service
geckodriver_path = Service('/Users/admin/Downloads/geckodriver')

# Create function to generate query
def generate_query(page_n, query, price_max, price_min):
    
    if ~pd.isnull(price_max) or ~pd.isnull(price_min):
    
        if ~pd.isnull(price_max):
            pmax = str(price_max)
        else:
            pmax = ""

        if ~pd.isnull(price_min):
            pmin = str(price_min)
        else:
            pmin = ""
            
        price_query = "&price="+pmin+"-"+pmax
    
    else:
        price_query = ""
    
    query_space = query.replace(' ', '%20')
    return "https://www.lazada.co.id/catalog/?_keyori=ss&ajax=true&from=input&page="+str(page_n)+"&q="+query_space#+price_query

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
    
    
#     df['top_rated'] = get_top_rated(df['rating'], df['sold'], df['review'])
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
    
    df['tag'] = np.nan
    
    df['tag'].loc[cheap] = 'cheap'
    df['tag'].loc[expensive] = 'expensive'
    df['tag'].loc[sold] = 'sold'
    df['tag'].loc[rated] = 'rated'
    df['tag'].loc[top] = 'top'
    df = df.dropna(axis='index', subset=['tag']).set_index('tag')


    result = df.to_json(orient='index')
    parsed = json.loads(result)
    json.dumps(parsed, indent=4)
    return parsed
    
    
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
def lazada_scrap(queryId):
    # Get queries from front end
    platform = "Lazada"
    query = get_query(queryId)['query']
    searchLimit = 20
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
    limit_result = searchLimit

    while len(list_listing_names) < limit_result:

    #     Get responses
        url = generate_query(page_n, query, price_max, price_min)
        responses = get_response(url, 'json')

        for response in responses['mods']['listItems']:

            # Get listing name
            list_listing_names.append(response['name'])

            # Get seller name
            list_seller_names.append(response['sellerName'])

            # Get listing prices
            list_listing_prices.append(response['price'])

            # Get listing ratings
            list_listing_ratings.append(response['ratingScore'])

            # Get listing thumbnails
            list_listing_thumbnails.append(response['image'])

            # Get listing solds
            try:
                list_listing_solds.append(response['soldRangeCount']['id'])
            except:
                list_listing_solds.append(np.nan)

            # Get listing locations
            list_listing_locations.append(response['location'])

            # Get listing reviews
            list_listing_reviews.append(response['review'])

            # Get is top ads
            list_is_top_ads.append('')

            # Get listing urls
            list_listing_urls.append(response['itemUrl'])

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
    df_result['platform'] = "Lazada"
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

    connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    connection.connect()

    df_result_min = df_result.to_json(orient="index")

    json_data = {
        'queryId': queryId,
        'platform': platform,
        'ScrapRes': df_result_min
    }

    connection.request('POST', '/classes/ScrapResMin', json.dumps(
            json_data
         ), {
            'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
            'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU',
            'Content-Type': 'application/json'
         })
    
    return summarise(df_result)

