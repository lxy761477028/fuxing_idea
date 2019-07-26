class Config(object):
    IP = "0.0.0.0"
    PORT = 7000
    # AI_URL = "http://127.0.0.1"
    # HOST = "127.0.0.1"
    # AI_PORT = [6000, 6001]
    # PROCESSES_NUM = [8, 4]
    AI_SERVING = [["127.0.0.1:6000", "127.0.0.1", 6000, 8],
                  ["127.0.0.1:6001", "127.0.0.1", 6001, 4]]

    LOGGING_FILE_PATH = './log'
    # LOGGING_CONFIG_FILE_PATH = './logging.conf'

    APPLD = ""
    LICENSE = ""
