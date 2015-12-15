from flask import Flask, request
from pymongo import MongoClient
import datetime
import secrets
import ssl

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
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #context.load_cert_chain(certfile='/etc/letsencrypt/live/vps.provolot.com/cert.pem', keyfile='/etc/letsencrypt/live/vps.provolot.com/privkey.pem')
    app.run(host='0.0.0.0', port=8002)
