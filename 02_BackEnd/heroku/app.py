from flask import Flask, request
import pandas as pd
import ConnectBackEnd

app = Flask(__name__)

@app.route('/', endpoint='home', methods=["GET", "POST"])
@app.route('/post_full_search/<objectId>/<resultObj>', endpoint='post_full_search', methods=["POST"])
@app.route('/get_queries/<objectId>', endpoint='get_queries', methods=["GET"])
@app.route('/post_search/<resultObj>', endpoint='post_search', methods=["POST"])
@app.route('/get_new_query_id/<resultObj>', endpoint='get_new_query_id', methods=["GET"])

def index(objectId = "", resultObj = ""):
    if request.endpoint == 'home':
        return {'test': 'successful'}
    if request.endpoint == 'post_full_search':
        return ConnectBackEnd.post_full_search(objectId, resultObj)
    if request.endpoint == 'get_queries':
        return ConnectBackEnd.get_queries(objectId)
    if request.endpoint == 'post_search':
        return ConnectBackEnd.post_search(resultObj)
    if request.endpoint == 'get_new_query_id':
        return ConnectBackEnd.get_new_query_id(resultObj)

if __name__ == "__main__":
    app.run()