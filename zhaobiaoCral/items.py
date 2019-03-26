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
    if string is not str:
        string = str(string)
    return string.encode('gbk',errors='ignore').decode('gbk')

def _drop_blank_ntr(string):
    return re.sub(r'\n|\t|\r| ', '', string)

def _drop_ntr(string):
    return re.sub(r'\n|\t|\r', '', string)

def oracle_field():
    """
    去掉 \n \r\ t与空格，再把utf8转成gbk
    :return:
    """
    return scrapy.Field(
        input_processor=MapCompose(_utf8_to_gbk, _drop_blank_ntr),
        output_processor=TakeFirst()
    )

def only_oracle_field():
    """
    只把utf8转成gbk
    :return:
    """
    return scrapy.Field(
        input_processor=MapCompose(_utf8_to_gbk, _drop_ntr),
        output_processor=TakeFirst()
    )


class __OriginItem(scrapy.Item):
    farticleid = only_oracle_field()


class FileItem(__OriginItem):
    file_urls = only_oracle_field()
    fpath = only_oracle_field()
    farea = only_oracle_field()


class TextItem(__OriginItem):
    fhtml = oracle_field()
    fartcle = only_oracle_field()
    ftext = only_oracle_field()


for item_name, field_list in CREATE_ITEM.items():
    # 构建包含Field的字典
    _d = dict(
        [(field_name, oracle_field()) for field_name in field_list]
    )
        #  创建 item类
    vars()[item_name] = type(item_name, (__OriginItem,), _d)