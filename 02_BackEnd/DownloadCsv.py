#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import requests

import tkinter
from tkinter import filedialog
import os
import requests
import json

# Create function to get url queries from front end

def get_query(queryId):
    url = "https://parseapi.back4app.com/classes/ScrapResMin/"+queryId
    headers = {
        "X-Parse-Application-Id": "XXXXX",
        "X-Parse-Rest-Api-Key": "XXXXX",
      }
    
    r = requests.get(url, headers=headers)
    return r.json()

# Create function to save search result
def download_tables(queries):

    result = pd.DataFrame()
    queries = queries.split("_")

    for queryId_ in queries[:len(queries)-1]:
        print(queryId_)
        response = get_query(queryId_)
        response_clean = json.loads(response['ScrapRes'])
        result = result.append(pd.DataFrame.from_dict(response_clean, orient='index'))
        
    result = result.reset_index().drop(columns=['index'])
    result = result.fillna('NaN')
    df_result_min = result.to_dict("index")

    return json.loads(json.dumps(df_result_min, indent=4))

