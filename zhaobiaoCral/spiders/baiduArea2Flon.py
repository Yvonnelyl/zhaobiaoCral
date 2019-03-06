# example
from .zhaobiaoBaseSpider import BaseSpider
from scrapy import spiders
from scrapy import Request
from .. import items
from scrapy.loader import ItemLoader
import uuid


class ZhaobiaocralExample(BaseSpider):


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
            row_item_loader = ItemLoader(item=items.__OriginItem(), selector=row)
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