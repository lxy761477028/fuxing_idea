class Config(object):
    IP = "0.0.0.0"
    PORT = 7000
    URL = ""
    APPLD = ""
    LICENSE = ""


class mqConfig(object):
    MQ_IP = '172.16.100.221'
    MQ_PORT = 25671
    URL = r'http://127.0.0.1:7000/'


class mysqlConfig(object):
    HOST = "172.16.100.221"
    PORT = 2009
    USER = "root"
    PASSWORD = "1qaz2wsx"
    DATABASE = "ring_integration"


class tokenConfig(object):
    APPLD = ""
    LICENSE = ""
    SUCCESS = "0"
    FAIL = "1"

