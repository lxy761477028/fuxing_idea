#! -*- coding:utf-8 -*-
# !/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import cv2
import numpy as np
# from SSD_Detection import SSD_Detection  # 有一个SSD_Detection.py的文件里面放了关于图片目标检测的相关程序，这里不给出这个程序
import socket

# detector = SSD_Detection(0.10)  # 构建检测模型对象


class MyHandler(BaseHTTPRequestHandler):
    # def do_GET(self):
    #     # self.wfile.write("这是一个http后台服务。".encode())
    #     data = {
    #         "code": 1
    #     }
    #     jsonData = json.dumps(data)
    #     self.wfile.write(jsonData.encode())


    def do_POST(self):

        body = self.rfile.read(int(self.headers['content-length']))

        json_data = json.loads(body)

        self.send_response(200)
        self.end_headers()

        data = {
            "code": 1
        }
        jsonData = json.dumps(data)
        self.wfile.write(jsonData.encode())


    def do_GET(self):
        # self.wfile.write("这是一个http后台服务。".encode())
        self.send_response(200)
        self.end_headers()
        data = {
            "code": 1
        }
        jsonData = json.dumps(data)
        self.wfile.write(jsonData.encode())

def main():
    try:
        server = HTTPServer(('127.0.0.1', 8080), MyHandler)  # 启动服务
        print('welcome to  the  server.......')
        server.serve_forever()  # 一直运行
    except KeyboardInterrupt:
        print('shuting  done server')
        server.socket.close()


if __name__ == '__main__':
    main()
