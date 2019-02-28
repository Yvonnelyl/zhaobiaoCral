import os
import uuid
import json


def check_dir(path):
    """
    检查是否存在路径，没有创建
    :param path: 路径
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def save_data(date_str, path, type = 'w'):
    """
    把字符串存进指定文档中
    :param date_str:    要存的字符串
    :param path:        文档路径
    """
    with open(path, type) as file:
        file.write(date_str)


def read_data(path, type = 'r'):
    """
    从文档中读出字符串
    :param path: txt文件的路径+文件名
    :return:     字符串
    """
    lines = []
    if os.path.exists(path):
        with open(path, type) as file:
            lines = file.readlines()
        return lines


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def  guid():
    return uuid.uuid4().hex


def json_to_dict(json_path):
    with open(json_path, 'rb') as f:
        conf_dict = json.loads(f.read())
    return conf_dict


def get_dir_son_file(file_dir):
    for _, _, files in os.walk(file_dir):
        return files  # 当前路径下所有非目录子文件


def get_file_dir(file):
    return os.path.dirname(os.path.realpath(file))
