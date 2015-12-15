from flask import Flask, request
from pymongo import MongoClient
import datetime
import secrets

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/thumbtack/<url>', methods=['POST'])
@crossdomain(origin='*')
def add_message(url):
    try: 
        json = request.get_json()
        json['fromapi_remoteaddr'] = request.remote_addr
        json['fromapi_date'] = datetime.datetime.utcnow()
        json['url'] = url

        client = MongoClient(secrets.MONGODBHOST)
        db = client[secrets.MONGODBDB]
        db.authenticate(secrets.MONGODBUSER, secrets.MONGODBPASS)
        logcollection = db[secrets.MONGODBCOLLECTION]

        objid = logcollection.insert_one(json)

        client.close()

        return "success"
    except:
        return "failure"

if __name__ == "__main__":
    app.run(port=8001)
