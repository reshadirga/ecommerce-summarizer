from flask import Flask,render_template, request, jsonify
import BlibliScrapping
import BukalapakScrapping
import LazadaScrapping
import ShopeeScrapping
import TokopediaScrapping
import DownloadCsv
import time
import pandas as pd

app = Flask(__name__)

@app.route('/search/<objectId>', endpoint='search', methods=["POST", "GET"])
@app.route('/download/<objectId>', endpoint='downloads', methods=["POST", "GET"])

def index(objectId):
    if request.endpoint == 'search':
        return get_query(objectId)
    if request.endpoint == 'downloads':
        return DownloadCsv.download_tables(objectId)

def get_query(objectId):

    res_dict = {}

    print("running")

    print('blibli')
    try:
        res_blibli = BlibliScrapping.blibli_scrap(objectId)
    except:
        print('extract error')
        res_blibli = {
            'summary': 0,
            'df': pd.DataFrame()
            }

    print('bukalapak')
    try:
        res_bukalapak = BukalapakScrapping.bukalapak_scrap(objectId)
    except:
        print('extract error')
        res_bukalapak = {
            'summary': 0,
            'df': pd.DataFrame()
            }

    # print('lazada')
    # try:
    #     res_lazada = LazadaScrapping.lazada_scrap(objectId)
    # except:
    #     print('extract error')
    #     res_lazada = 0

    print('shopee')
    try:
        res_shopee = ShopeeScrapping.shopee_scrap(objectId)
    except:
        print('extract error')
        res_shopee = {
            'summary': 0,
            'df': pd.DataFrame()
            }

    print('tokopedia')
    try:
        res_tokopedia = TokopediaScrapping.tokped_scrap(objectId)
    except:
        print('extract error')
        res_tokopedia = {
            'summary': 0,
            'df': pd.DataFrame()
            }

    res_dict['blibli'] = res_blibli['summary']
    res_dict['bukalapak'] = res_bukalapak['summary']
    # res_dict['lazada'] = res_lazada
    res_dict['shopee'] = res_shopee['summary']
    res_dict['tokopedia'] = res_tokopedia['summary']

    result_df = pd.DataFrame()
    
    result_df = result_df.append([res_blibli['df'], res_bukalapak['df'], res_shopee['df'], res_tokopedia['df']])
    result_df = result_df.reset_index().drop(columns=['index', 'top_rated'])

    import requests
    import json
    import http.client as httplib

    connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    connection.connect()

    df_result_min = result_df.to_json(orient="index")

    json_data = {
        'queryId': objectId,
        # 'platform': platform,
        'ScrapRes': df_result_min
    }

    connection.request('POST', '/classes/ScrapResMin', json.dumps(
            json_data
         ), {
            'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
            'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU',
            'Content-Type': 'application/json'
         })

    print(json.loads(connection.getresponse().read()))

    return res_dict

if __name__ == "__main__":
    app.run()