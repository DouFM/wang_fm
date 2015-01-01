# coding:utf-8
import logging


def init(log_name, log_file):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:\n%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def write_info(logger, information):
    if isinstance(information, unicode):
        information.encode('utf-8')
    logger.info(information)