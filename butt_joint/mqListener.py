import stomp
import time
import json
import urllib.request


mq_hostname = '0.0.0.0'
mq_port = 10086

def tryConnect(mq_hostname, mq_port):
    try:
        #建立连接配置
        conn = stomp.Connection([(mq_hostname, mq_port)])
        #注册监听者
        conn.set_listener('', MyListener(conn))
        #连接监听
        conn.start()
        conn.connect()
        #开始监听接受消息
        conn.subscribe(destination='queue.ai', id=1, ack='client')
        conn.subscribe(destination='queue.reg', id=2, ack='client')
        conn.subscribe(destination='queue.mpr', id=3, ack='client')

        return conn
    except Exception as e:
        time.sleep(10)


class MyListener(object):

    def __init__(self, conn):
        self.conn = conn

    def on_error(self, headers, message):
        pass
        # logging.info('$$$ received an error: %s from MQ' % message)

    def on_message(self, headers, message):
        # 标记已处理消息
        self.conn.ack(id=headers['message-id'], subscription=headers['subscription'])
        # 获取监听到的消息，并处理
        jsonObj = json.loads(message)
        method = jsonObj.get("operationType")
        requestId = jsonObj.get("requestId")
        data = jsonObj.get("operationParams")

        message = json.dumps(data)
        param_dict = json.loads(message)

        # 调用处理函数
        import requests
        url = "http://127.0.0.1:5000/"
        file = requests.post(url, json=message)

        # 动态添加属性


        # 将对象序列化


        # 发送处理过的消息
        # self.conn.send(body=result, destination='queue.ai.result')


if __name__ == '__main__':
    conn = tryConnect(mq_hostname, mq_port)
    while True:
        try:
            time.sleep(1)
        except:
            conn.disconnect()