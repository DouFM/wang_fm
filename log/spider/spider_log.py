#coding:utf-8
from log.log_base import init
from log.log_base import write_info
logger = None


def get_logger():
    global logger
    if not logger:
        logger = init("spider_logger", "log/spider/spider_log.txt")
    return logger


def log_info(information):
    write_info(get_logger(), information)

if __name__ == "__main__":
    log_info(("test log %s", "shabi"))
