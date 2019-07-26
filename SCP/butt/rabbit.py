import pika
import json
import requests
from config import mqConfig


def mqListen():

    username = 'guest'
    pwd = 'guest'
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(pika.ConnectionParameters('172.16.100.221', 25671, credentials=user_pwd))
    chan = s_conn.channel()

    chan.queue_declare(queue='ring_integration_queue', durable=True)

    def callback(ch,method,properties,body):
        print("[消费者] recv %s" % body)
        data = json.loads(body.decode('utf-8'))
        response = requests.post(mqConfig.URL, json=data)
        print(response.text)
    chan.basic_consume(callback,  queue='ring_integration_queue', no_ack=True)
    print('[消费者] waiting for msg .')
    chan.start_consuming()#开始循环取消息
