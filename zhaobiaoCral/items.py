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

def oracle_field():
    return scrapy.Field(input_processor=MapCompose(_utf8_to_gbk, _drop_gang_ntr))


class __OriginItem(scrapy.Item):
    fudtime = oracle_field()
    fisuse = oracle_field()


class FileItem(__OriginItem):
    farticleid = oracle_field()
    file_urls = oracle_field()
    fpath = oracle_field()


class HtmlItem(__OriginItem):
    farticleid = oracle_field()
    farticlehtml = oracle_field()


class TextItem(__OriginItem):
    farticleid = oracle_field()
    fxpath = oracle_field()
    fartcle = oracle_field()
    ftext = oracle_field()


for item_dct in _load_item_info():
    for name in item_dct:
        # 构建包含Field的字典
        _d = dict(
            [(name, oracle_field()) for name in item_dct[name]]
        )
        #  创建 item类
        vars()[name] = type(name, (__OriginItem,), _d)