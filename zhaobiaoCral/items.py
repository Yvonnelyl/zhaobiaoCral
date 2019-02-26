# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json
from scrapy.loader.processors import Join, MapCompose, TakeFirst


def _utf8_to_gbk(string):
    return string.encode('gbk',errors='ignore').decode('gbk')

def _drop_gang_ntr(string):
    return string.replace('\n\t\r', '')

def _load_item_info():
    with open(r'C:\Users\Admin\PycharmProjects\scrapyProjects\zhaobiaoCral\test.json','rb') as f:
        json_ = f.read()
        dct = json.loads(json_)
        yield dct['item']


for item_dct in _load_item_info():
    for name in item_dct:
        _d = dict(
            [(name, scrapy.Field(input_processor=MapCompose(_utf8_to_gbk, _drop_gang_ntr))) for name in item_dct[name]]
        )
        vars()[name] = type(name, (scrapy.Item,), _d)


