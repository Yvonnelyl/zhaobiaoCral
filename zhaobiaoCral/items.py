# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json
from scrapy.loader.processors import Join, MapCompose, TakeFirst
# 从此文件中获取item路径
from .settings  import CREATE_ITEM
import re


def _utf8_to_gbk(string):
    return string.encode('gbk',errors='ignore').decode('gbk')

def _drop_gang_ntr(string):
    return re.sub(r'\n|\t|\r', '', string)

def oracle_field():
    return scrapy.Field(
        input_processor=MapCompose(_utf8_to_gbk, _drop_gang_ntr),
        output_processor = TakeFirst()
    )


class __OriginItem(scrapy.Item):
    farticleid = oracle_field()


class FileItem(scrapy.Item):
    farticleid = scrapy.Field()
    file_urls = scrapy.Field()
    fpath = scrapy.Field()
    farea = scrapy.Field()


class TextItem(__OriginItem):
    fhtml = oracle_field()
    fartcle = oracle_field()
    ftext = oracle_field()


for item_name, field_list in CREATE_ITEM.items():
    # 构建包含Field的字典
    _d = dict(
        [(field_name, oracle_field()) for field_name in field_list]
    )
        #  创建 item类
    vars()[item_name] = type(item_name, (__OriginItem,), _d)