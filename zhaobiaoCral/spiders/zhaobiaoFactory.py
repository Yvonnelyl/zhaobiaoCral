import json
import traceback
from .zhaobiaoBaseSpider import BaseSpider
from scrapy import spiders
from scrapy import Request
from .. import items
from scrapy.loader import ItemLoader
import uuid


class _zhaobiaoSpiderCreator():
    """

    """
    def __new__(cls):
        cral_conf_dct = _GetCralConf('json')
        for func_name in cral_conf_dct['func']:
            cral_conf_dct.update(
                {func_name: cls.get_wanted_func(func_name, cral_conf_dct['func'][func_name])}
            )
        return cral_conf_dct['name'], type(cral_conf_dct['name'], (BaseSpider,), cral_conf_dct)

    @classmethod
    def get_wanted_func(cls, func_name,  dct):
            def tmp(self, response):
                for parse_name in self.func[func_name]:
                    f = getattr(self, parse_name)
                    yield from f(self.func[func_name][parse_name], response)
            tmp.__name__ = func_name
            return tmp


class _GetCralConf():
    def __new__(cls, source):
        return getattr(cls, source)()

    @classmethod
    def json(cls):
        """
        test
        :return:
        """
        with open(r'C:\Users\Admin\PycharmProjects\scrapyProjects\zhaobiaoCral\test1.json', 'rb') as f:
            json_ = f.read()
            return json.loads(json_)

    @classmethod
    def redis(cls):
        pass


# example
class ZhaobiaocralExample(BaseSpider):
    name = "ZhaobiaocralExample"
    main_url = 'http://www.basechem.org'
    fwebsite = ['四川政府采购网']
    fregion = ['四川']

    item_value = ['fwebsite', 'fregion']

    nextpage_xpath = None
    next_page_signal = None
    nextpage_url_num_search_re = 'http://www.basechem.org/search\?q=.+?&page=(.+)'

    param = [
        {'types': '邀请招标采购公告', 'code': '8a817ecb39b9902a0139b9a22bc00b47', 'meta': {'zhaobiao_type': '邀请招标'}},
        {'types': '邀请招标采购公告', 'code': '8a817ecb39d832560139d85a2ea70b06', 'meta': {'zhaobiao_type': '邀请招标'}},
        {'types': '竞争性谈判采购公告', 'code': '8a817ecb39b9902a0139b9a541e90b4f', 'meta': {'zhaobiao_type': '竞争性谈判'}},
        {'types': '竞争性谈判采购公告', 'code': '8a817ecb39d832560139d85b10ca0b0a', 'meta': {'zhaobiao_type': '竞争性谈判'}},
        {'types': '公开招标采购公告', 'code': '8a817ecb39b9902a0139b9a2dfaf0b4b', 'meta': {'zhaobiao_type': '公开招标'}},
        {'types': '公开招标采购公告', 'code': '8a817ecb39d832560139d858abff0afe', 'meta': {'zhaobiao_type': '公开招标'}},
        {'types': '竞争性磋商采购公告', 'code': '402886875355b06e01539d135c5a3b0e', 'meta': {'zhaobiao_type': '竞争性磋商'}},
        {'types': '竞争性磋商采购公告', 'code': '402886875355b06e01539dde85093fb9', 'meta': {'zhaobiao_type': '竞争性磋商'}},
        {'types': '询价采购公告', 'code': '8a817ecb39b9902a0139b9a5d8ea0b53', 'meta': {'zhaobiao_type': '询价采购公告'}},
        {'types': '询价采购公告', 'code': '8a817ecb39d832560139d85973c30b02', 'meta': {'zhaobiao_type': '询价采购公告'}},
        {'types': '单一来源采购公告', 'code': '8a817ecb39b9902a0139b9a72aed0b57', 'meta': {'zhaobiao_type': '单一来源采购公告'}},
        {'types': '单一来源采购公告', 'code': '8a817ecb39d832560139d85806a70afa', 'meta': {'zhaobiao_type': '单一来源采购公告'}},
    ]
    start_time = '2019-01-23'
    end_time = '2019-01-24'

    def start_requests(self):

        for p in self.param:
            types = p['types']
            code = p['code']
            meta = p['meta']

            url = f'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=search&years=2018&chnlNames={types}&chnlCodes={code}&title=&tenderno=&agentname=&buyername=&startTime={self.start_time}&endTime={self.end_time}&distin_like=510000&province=510000&city=&town=&provinceText=\u56DB\u5DDD\u7701&cityText=\u8BF7\u9009\u62E9&townText=\u8BF7\u9009\u62E9&pageSize=10&curPage=1&searchResultForm=search_result_anhui.ftl'.format()
            print(url)
            yield Request(url, callback=self.parse, meta=meta)

    def parse(self, response):
        table = response.xpath('//div[@class="info"]/ul/li')
        for row in table:
            row_item_loader = ItemLoader(item=items.OriginItem(), selector=row)
            row_item_loader.add_xpath('ftime',
                                      'concat(./div[@class="time curr"]/text()[2],"-",./div[@class="time curr"]/span/text())')
            row_item_loader.add_xpath('furl', './a/@href')
            row_item_loader.add_xpath('ftitle', './a/div[@class="title"]/text()')
            row_item = row_item_loader.load_item()
            for url in row_item['furl']:
                yield Request(self._relative_to_absolute(url, response), callback=self.parse_detail,
                              meta={'row_item': row_item})

    def parse_detail(self, response):
        """
        搜狗搜索页面爬虫
        :param response:
        :return:
        """
        # group_name = re.search(self.group_name_extract_re, response.url).group(1)
        row_item = response.meta['row_item']
        row_item['farticle'] = [response.text]
        row_item['farticleid'] = [str(uuid.uuid4()).replace('-', '')]
        for name in self.item_value:
            row_item[name] = getattr(self, name)
        yield row_item


# create new spider
_, FleshSpider = _zhaobiaoSpiderCreator()
# vars()[__cral_name] = __NewSpider
# del __NewSpider
# print(Zhaobiaocral.start_requests)
