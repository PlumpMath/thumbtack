from flask import Flask, request
from pymongo import MongoClient
import datetime
import secrets
import ssl

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

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
