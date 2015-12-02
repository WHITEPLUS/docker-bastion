import os, json, redis, logging
from flask import Flask, Response, request
from logging.handlers import RotatingFileHandler

log_handler = RotatingFileHandler('/var/log/api.log', maxBytes=100000, backupCount=10)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)

@app.route("/")
def index():
    return "OK"

@app.route("/keys/<user_id>", methods=['GET'])
def get_key(user_id):
    r = redis.Redis(host='cache', port=6379, db=0)
    data={
        'endpoint':'get-key',
        'result':'success',
        'user_id': user_id
    }
    if r.hexists('wp_authorized_keys', user_id):
        data['authorized_key'] = r.hget('wp_authorized_keys', user_id)
        return Response(json.dumps(data))
    # not found
    data['result'] = 'failed'
    data['error_title'] = 'Not Found'
    data['error_description'] = 'The %s\'s public key is not found.'%(user_id)
    return Response(json.dumps(data), 404)

@app.route("/keys/<user_id>", methods=['POST'])
def post_key(user_id):
    # auth_key = request.form['authorized_key']
    # r = redis.Redis(host='cache', port=6379, db=0)
    # r.hset('wp_authorized_keys', user_id, auth_key)
    # update_authorized_keys(r.hgetall('wp_authorized_keys'))
    data={
        'endpoint':'set-key',
        'result':'success',
        'user_id': user_id,
        'test': r.hgetall('wp_authorized_keys')
    }
    return Response(json.dumps(data))

def update_authorized_keys(r):
    r.hgetall('wp_authorized_keys')
    pass

if __name__ == "__main__":
    # r = redis.Redis(host='cache', port=6379, db=0)
    # update_authorized_keys(r.hgetall('wp_authorized_keys'))
    app.run(host='0.0.0.0', port=80)