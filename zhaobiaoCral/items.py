# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json
from scrapy.loader.processors import Join, MapCompose, TakeFirst
# 从此文件中获取item路径
from zhaobiaoCral.conf_path  import path


def _utf8_to_gbk(string):
    return string.encode('gbk',errors='ignore').decode('gbk')

def _drop_gang_ntr(string):
    return string.replace('\n\t\r', '')

def _load_item_info():
    """
    读取item类，抛出每一个item的构建信息
    :return:
    """
    with open(path["item"], 'rb') as f:
        json_ = f.read()
        dct = json.loads(json_)
        item_dict = dct['item']
        # 循环抛出item类构建信息
        for item_name, item_param in item_dict.items():
            yield item_param


class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_path = scrapy.Field()


for item_dct in _load_item_info():
    for name in item_dct:
        # 构建包含Field的字典
        _d = dict(
            [(name, scrapy.Field(input_processor=MapCompose(_utf8_to_gbk, _drop_gang_ntr))) for name in item_dct[name]]
        )
        #  创建 item类
        vars()[name] = type(name, (scrapy.Item,), _d)


