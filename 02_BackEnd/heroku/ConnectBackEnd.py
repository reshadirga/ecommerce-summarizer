
from unittest import result
import os

# From scrapping scripts
def post_full_search(queryId, df_result_min):
    import requests
    import json
    import http.client as httplib

    connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    connection.connect()

    json_data = {
        'queryId': queryId,
        'ScrapRes': df_result_min
    }

    connection.request('POST', '/classes/ScrapResMin', json.dumps(
            json_data
            ), {
            'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
            'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU',
            'Content-Type': 'application/json'
            })

    return json.loads(connection.getresponse().read())

# From result page - ScrapsId
def get_queries(searchId):
    import http.client
    import json
    import urllib.parse


    connection = http.client.HTTPSConnection('parseapi.back4app.com', 443)
    params = urllib.parse.urlencode({"where": json.dumps({
        "queryId": searchId
    })})
    connection.connect()
    connection.request('GET', '/classes/ScrapResMin?%s' % params, '', {
        'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
        'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU'
    })
    results = json.loads(connection.getresponse().read())
    
    return results

# From landing page - addQuery pt. 1
def post_search(userContext):
    import requests
    import json
    import http.client as httplib

    connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    connection.connect()

    json_data = {
        'lat': userContext.userLocation.lat + "",
        'long': userContext.userLocation.lon + "",
        'query': userContext.userInput.query + "",
        'price_max': userContext.userInput.maxPrice + "",
        'price_min': userContext.userInput.minPrice + "",
        'searchParam_blibli': userContext.searchParam.blibliParam_,
        'searchParam_bukalapak': userContext.searchParam.bukalapakParam_,
        'searchParam_shopee': userContext.searchParam.shopeeParam_,
        'searchParam_tokopedia': userContext.searchParam.tokopediaParam_
    }

    connection.request('POST', '/classes/Queries', json.dumps(
            json_data
            ), {
            'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
            'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU',
            'Content-Type': 'application/json'
            })

    return json.loads(connection.getresponse().read())

# From landing page - addQuery pt. 2
def get_new_query_id(userContext):
    import http.client
    import json
    import urllib.parse


    connection = http.client.HTTPSConnection('YOUR.PARSE-SERVER.HERE', 443)
    params = urllib.parse.urlencode({"where": json.dumps({
        'query': userContext.userInput.query + "",
        'price_max': userContext.userInput.maxPrice + "",
        'price_min': userContext.userInput.minPrice + ""
    })})
    connection.connect()
    connection.request('GET', '/classes/Queries?%s' % params, '', {
        'X-Parse-Application-Id': 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI',
        'X-Parse-REST-API-Key': '7It4g7Xdivpoe8mU6yaNZtC6yNw3cJ8WNCTT0rxU'
    })
    results = json.loads(connection.getresponse().read())

    return results[len(results)-1]['id']