#coding:utf-8
from log.log_base import init
from log.log_base import write_info
g_logger = None


def get_logger():
    global g_logger
    if not g_logger:
        g_logger = init("spider_task_logger", "log/spider/spider_task_log.txt")
    return g_logger


def log_info(information):
    write_info(get_logger(), information)


if __name__ == "__main__":
    log_info("test log")
