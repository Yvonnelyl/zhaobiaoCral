# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
# 从此文件中获取item路径
from .settings  import CREATE_ITEM
import re
import time

#*-------------数据过滤器--------------*
def _time_process(date):
    if not isinstance(date, str):
        date = str(date)
    try:
        date = float(date)
    except Exception:
        try:
            date = int(date)
        except Exception:
            pass
        else:
            date = time.strftime("%Y-%m-%d", time.localtime(int(str(date)[:10])))
    else:
        date = time.strftime("%Y-%m-%d", time.localtime(int(str(date)[:10])))
    date = date.strip("[]<> ")[:10]
    return date.encode('gbk',errors='ignore').decode('gbk')

def _utf8_to_gbk(string):
    if string is not str:
        string = str(string)
    return string.encode('gbk',errors='ignore').decode('gbk')

def _drop_blank_ntr(string):
    return re.sub(r'\n|\t|\r| ', '', string)

def _drop_ntr(string):
    return re.sub(r'\n|\t|\r', '', string)
#*-------------oracle字段--------------*
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
#*-------------自定义Item--------------*
class __OriginItem(scrapy.Item):
    farticleid = only_oracle_field()


class FileItem(__OriginItem):
    file_urls = only_oracle_field()
    fpath = only_oracle_field()
    farea = only_oracle_field()


class TextItem(__OriginItem):
    fhtml = oracle_field()
    fartcle = oracle_field()
    ftext = oracle_field()


class ListItem(__OriginItem):
    ftitle = oracle_field()
    fwebsite = only_oracle_field()
    furl = only_oracle_field()
    fregion = oracle_field()
    # 进来的是1556xxxx的时候换成str
    ftime = scrapy.Field(
        input_processor=MapCompose(_drop_blank_ntr, _time_process),
        output_processor=TakeFirst()
    )
    zhaobiao_type = only_oracle_field()


class ErrorPageItem(__OriginItem):
    furl = scrapy.Field(input_processor=MapCompose(_utf8_to_gbk))
    fmethod = scrapy.Field(input_processor=MapCompose(_utf8_to_gbk))
    fparam = scrapy.Field(input_processor=MapCompose(_utf8_to_gbk))
    fmeta = scrapy.Field(input_processor=MapCompose(_utf8_to_gbk))


for item_name, field_list in CREATE_ITEM.items():
    # 构建包含Field的字典
    _d = dict(
        [(field_name, oracle_field()) for field_name in field_list]
    )
        #  创建 item类
    vars()[item_name] = type(item_name, (__OriginItem,), _d)