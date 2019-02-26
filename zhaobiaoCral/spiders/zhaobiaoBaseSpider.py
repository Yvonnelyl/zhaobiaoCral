# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy import Request, spiders
from .. import items
from scrapy.loader import ItemLoader
import uuid
import re
import traceback


class BaseSpider(spiders.Spider):

    def start_requests(self):
        print('start_requests')
        for p in self.param:
            yield Request(self.start_url.format(self=self, **p), callback=self.parse, meta={"cln": p['meta']})

    def parse_list(self,dct, response):
        print('start_parse_list')
        table = getattr(response, dct['table_row']['method'])(dct['table_row']['path'])
        if 'item_loader' in dct:
            for row in table:
                row_item_loader = ItemLoader(item=items.OriginItem(), selector=row)
                for name, param in dct['item_loader'].items():
                    method = param[0]
                    path = param[1]
                    getattr(row_item_loader, method)(name, path)
                row_item = row_item_loader.load_item()
                response.meta.update({'item': row_item})
                if 'reuquest' in dct['yield']:
                    for url in row_item['furl']:
                        yield Request(
                            url=self._relative_to_absolute(url, response),
                            meta=response.meta,
                            callback = getattr(self, dct['yield']['reuquest']['callback'])
                        )

    def parse_article(self, dct, response):
        if 'meta_item' in dct:
            row_item = response.meta['item']
            row_item[dct['meta_item']['article']] = [response.text]
            row_item[dct['meta_item']['id']] = [uuid.uuid4().hex]
            for name in self.item_value:
                row_item[name] = getattr(self, name)
            for name in response.meta['cln']:
                row_item[name] =response.meta['cln'][name]
        yield row_item

    def next_page(self, response):
        next_page_request = response.request
        next_page_url = self._get_next_page_url(response)
        if next_page_url:
            next_page_request.url = next_page_url
            next_page_request.callback = getattr(self, self._get_caller_func_name())
            yield next_page_request

    def _get_next_page_url(self, response):
        """
        demand：
            self.nextpage_xpath  or  self.nextpage_url_num_re
            self.main_url
        要么用xpath获取，要么num+1，返回下一页url
        :param url:
        :param response:
        :return:
        """
        if self.nextpage_xpath:
            relative_url = response.xpath(self.nextpage_xpath)
            return self.__relative_to_absolute(relative_url, response)

        elif self.nextpage_url_num_search_re:
            return self.__get_url_by_increase_num(response.url)

    def _relative_to_absolute(self, url, response):
        """
         demand：
                     self.main_url
        判断相对路径url为“./”还是“/”。
        前者加上现在的url，后者将加上main_url
        :param url: url相对路径
        :return: url绝对路径
        """
        if url.startswith('/'):
            return self.main_url + url
        elif url.startswith('./'):
            return response.url + url

    def _get_url_by_increase_num(self, url):
        """
        demand:
            self.nextpage_url_num_extract_re
        用正则提出这一页url的页数+1后覆盖原页数，返回下一页url
        :param url: 这一页的url
        :return: 下一页url
        """
        re_result = re.search(self.nextpage_url_num_search_re, url)
        if re_result:
            num = int(re_result.group(1))
            num += 1
            print('翻页：' + str(num))
            num_start_index = re_result.regs[1][0]
            num_end_index = re_result.regs[1][1]
            return url[:num_start_index] + str(num)+ url[num_end_index:]

    @classmethod
    def _get_self_func_name(cls):
        return traceback.extract_stack()[-2][2]

    @classmethod
    def _get_caller_func_name(cls):
        return traceback.extract_stack()[-3][2]

