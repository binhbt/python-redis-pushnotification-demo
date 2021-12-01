from flask import Flask
from redis import Redis
from flask_sse import sse
from flask import request, abort
from flask import jsonify
import traceback
from flask_uwsgi_websocket import GeventWebSocket
import time
from util.log_utils import logger as LOG

app = Flask(__name__)
# app.wsgi_app = AuthMiddleWare(app.wsgi_app)
websocket = GeventWebSocket(app)


redis = Redis(host='redis', port=6379)

CHANNEL='notifications_channel'
pub = redis.pubsub()

@websocket.route('/echo/<client_id>')
def echo(ws, client_id):

    pub.subscribe(CHANNEL)
    while True:
        msg = get_redis_message()
        if msg:
            # str_mess = str(msg)+'-'+client_id
            # ws.send(str_mess.encode('utf-8'))
            send_message_to_ws(ws, client_id, msg)
        time.sleep(1)
def send_message_to_ws(ws, client_id, msg):
    try:
        client1 ='"client_id":"{}"'.format(client_id)
        client2 =client1.replace('"',"'")
        print(client1)
        print(client2)
        if client1 in str(msg) or client2 in str(msg):
            ws.send(msg)
        else:
            print(str(msg))
    except Exception as e:
        LOG.exception(e)
        print(e)
def get_socket_message_and_send(ws):
    msg = ws.receive()
    # ws.send(msg)
    if msg:
        redis.publish(
            channel=CHANNEL,
            message=msg
        ) 
    return msg 
def get_redis_message():
    data = pub.get_message()
    LOG.info(data)
    if data:
        message = data['data']
        if message and message != 1:
            return message
    return None
def publish_message(data, channel=CHANNEL):
    redis.publish(
        channel=channel,
        message=str(data)
    )

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/push', methods = ['POST'])
def push_notification():
    data =request.get_data()
    # print(data)
    # LOG.info(data)
    publish_message(data)
    return 'ok'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
