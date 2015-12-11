from flask import Flask, request
from pymongo import MongoClient
import secrets

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/thumbtack/<url>', methods=['POST'])
def add_message(url):
    try: 
        json = request.get_json()
        json['remote_addr'] = request.remote_addr

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
