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

@app.route('/', endpoint='home', methods=["POST", "GET"])
@app.route('/test', endpoint='test', methods=["POST", "GET"])
@app.route('/search/_blibli/<objectId>', endpoint='search_blibli', methods=["POST", "GET"])
@app.route('/search/_bukalapak/<objectId>', endpoint='search_bukalapak', methods=["POST", "GET"])
@app.route('/search/_shopee/<objectId>', endpoint='search_shopee', methods=["POST", "GET"])
@app.route('/search/_tokopedia/<objectId>', endpoint='search_tokopedia', methods=["POST", "GET"])
@app.route('/download/<objectId>', endpoint='downloads', methods=["POST", "GET"])

def index(objectId = ""):
    if request.endpoint == 'home':
        return "available path: '/test' for testing purpose; '/search/<objectId>' for start searching ads; and '/download/<objectId> for download search result"
    if request.endpoint == 'test':
        return {
            'test': 'is a success!'
        }
    if request.endpoint == 'search_blibli':
        return get_query_blibli(objectId)
    if request.endpoint == 'search_bukalapak':
        return get_query_bukalapak(objectId)
    if request.endpoint == 'search_shopee':
        return get_query_shopee(objectId)
    if request.endpoint == 'search_tokopedia':
        return get_query_tokopedia(objectId)
    if request.endpoint == 'downloads':
        return DownloadCsv.download_tables(objectId)

def get_query_blibli(objectId):

    import requests
    import json
    import http.client as httplib

    print("running")

    print('blibli')
    # try:
    res_blibli = BlibliScrapping.blibli_scrap(objectId)
    # except:
    #     print('extract error')
    #     res_blibli = {
    #         'summary': {'0': 0},
    #         'df': pd.DataFrame()
    #         }

    try:
        result_df = res_blibli['df']
        result_df = result_df.reset_index().drop(columns=['index', 'top_rated'])

        

        connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
        connection.connect()

        df_result_min = result_df.to_json(orient="index")

        json_data = {
            'queryId': objectId,
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
    except:
        print("no new file uploaded")

    return res_blibli['summary']

def get_query_bukalapak(objectId):

    import requests
    import json
    import http.client as httplib

    print("running")
    print('bukalapak')
    # try:
    res_bukalapak = BukalapakScrapping.bukalapak_scrap(objectId)
    # except:
    #     print('extract error')
    #     res_bukalapak = {
    #         'summary': {'0': 0},
    #         'df': pd.DataFrame()
    #         }

    try:
        result_df = res_bukalapak['df']
        result_df = result_df.reset_index().drop(columns=['index', 'top_rated'])


        connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
        connection.connect()

        df_result_min = result_df.to_json(orient="index")

        json_data = {
            'queryId': objectId,
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
    except:
        print("no new file uploaded")

    return res_bukalapak['summary']

def get_query_shopee(objectId):

    import requests
    import json
    import http.client as httplib

    print("running")
    print('shopee')
    # try:
    res_shopee = ShopeeScrapping.shopee_scrap(objectId)
    # except:
    #     print('extract error')
    #     res_shopee = {
    #         'summary': {'0': 0},
    #         'df': pd.DataFrame()
    #         }

    try:
        result_df = res_shopee['df']
        result_df = result_df.reset_index().drop(columns=['index', 'top_rated'])


        connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
        connection.connect()

        df_result_min = result_df.to_json(orient="index")

        json_data = {
            'queryId': objectId,
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
    except:
        print("no new file uploaded")

    return res_shopee['summary']

def get_query_tokopedia(objectId):

    import requests
    import json
    import http.client as httplib

    print("running")
    print('tokopedia')
    
    # try:
    res_tokopedia = TokopediaScrapping.tokped_scrap(objectId)
    # except:
    #     print('extract error')
    #     res_tokopedia = {
    #         'summary': {'0': 0},
    #         'df': pd.DataFrame()
    #         }

    try:
        result_df = res_tokopedia['df']
        result_df = result_df.reset_index().drop(columns=['index', 'top_rated'])


        connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
        connection.connect()

        df_result_min = result_df.to_json(orient="index")

        json_data = {
            'queryId': objectId,
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
    except:
        print("no new file uploaded")

    return res_tokopedia['summary']

if __name__ == "__main__":
    app.run()