# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy import Request, spiders, FormRequest
from .. import items
from scrapy.loader import ItemLoader
import uuid
import re
import json


class BaseSpider(spiders.Spider):

    """
    基础爬虫：包含爬取页面的功能函数
    """
    def start_requests(self):
        """
        开始请求
        :return:
        """
        # 把url字符串统一转成列表 统一下面格式
        if type(self.start_url) == str:
            self.start_url = [self.start_url]
        # 建立空列表（字典） 统一下面格式
        if not hasattr(self, "param"):
            self.param = [dict()]

        # 如果有data，肯定是post
        if 'data' in self.param[0]:
            self.methods = "POST"
        methods = self.methods.upper()

        # 根据get  post方法选择不同request方法 并建立同名但不同逻辑的函数
        if methods == "GET":
            requests_fun = Request
            def get_date(p):
                return  dict()
        elif methods == "POST":
            requests_fun = FormRequest
            def get_date(p):
                for attr in p["data"]:
                    # 把self的start_date end_date format到data dict 里面
                    p["data"][attr] = p["data"][attr].foramat(self=self)
                return {"formdata": p["data"]}

        #  根据是否有param要format 建立同名但不同逻辑的函数
        if  "param" in self.param[0]:
            def get_url(url, p):
                return url.format(self=self, **p["param"])
        else:
            def get_url(url, p):
                return url.format(self=self)

        #建立函数判是否有meta 有责添加
        def get_meta(p):
            if "meta" in p:
                return {"meta": {"cln": p['meta']}}
            else: return {}

        # 开始请求（函数均由上述if else生成）
        for start_url in self.start_url:
            for p in self.param:
                yield requests_fun(
                    url=get_url(start_url, p),
                    **get_date(p), **get_meta(p),
                    callback=self.parse
                )

    def parse_json(self, dct, response, **d):
        yield from self.parse_list(dct, response, parse_type="json", **d)

    def __get_table_row(self, dct, response, parse_type):
        """
        获取table行
        """
        # 从html里用xpath提取
        if parse_type == "html":
            table = getattr(response, dct['table_row']['method'])(dct['table_row']['path'])
            if table:
                self.page_has_data = 1
            else:
                self.page_has_data = 0
        # 用json_path提取
        elif parse_type == "json":
            response_d = json.loads(response.text)
            try:
                if "json_in_json"  in dct:
                    response_d = self.__get_json_in_json(response_d, dct)

                path_list = dct["table_row"]["path"].split(',')
                table = self.__json_path(path_list, response_d)
            except KeyError:
                self.page_has_data = 0
            self.page_has_data = 1
        return table

    def __get_json_in_json(self, response_d, dct):
        """
        获取json里的json字符串
        """
        path_list = dct["json_in_json"]["path"].split(",")
        return json.loads(self.__json_path(path_list, response_d))

    def __json_path(self, json_path, json_d):
        """
        通过自定义的 json_path 找到json里的目标
        """
        if isinstance(json_path, str):
            json_tmp = json_d[json_path]
        elif isinstance(json_path, list):
            json_tmp = json_d
            for path in json_path:
                json_tmp = json_tmp[path]
        return json_tmp

    def parse_list(self,dct, response, **d):
        """
        处理列表方法
        :param dct:
        :param response:
        :return:
        """
        if "parse_type" in d:
            parse_type = d["parse_type"]
            table = self.__get_table_row(dct, response, parse_type)
        else:
            parse_type = "html"
            table = self.__get_table_row(dct, response, parse_type)

        for row in table:
            # guid
            article_id = uuid.uuid4().hex
            response.meta.update({'article_id': article_id})

            if 'item_loader' in dct:
                row_item = self.__item_loader(
                    "ListItem", dct['item_loader'], response, selector=row, load_type=parse_type)
                # 传给下一个函数
            if 'request' in dct:
                yield from self.__yield_request(
                    self._fix_url(row_item['furl'], response), dct['request'], response)

            row_item["farticleid"] = article_id

            # item_value是item的常数项，加上常数项
            for name in self.item_value:
                row_item[name] = getattr(self, name)

            # meta 传递值
            try:
                for name in response.meta['cln']:
                    row_item[name] = response.meta['cln'][name]
            except Exception:
                pass

            yield row_item

    def parse_article(self, dct, response, **d):
        # 生成uuid
        article_id = response.meta['article_id']

        #  正文的提取
        if "list" in dct:
            yield from self.__get_list(dct, article_id, response)
        # 保存html text
        if "text" in dct:
            yield from self.__get_text(dct, article_id, response)
        # 文件的提取
        if "file" in dct:
            yield from self.__get_file(dct, article_id, response)
        if "key_word" in dct:
            yield from self.__get_key_word(dct, article_id, response)

    def next_page(self,dct, response, caller_name , **d):
        # 获取下一页的url
        next_page_url = self._get_next_page_url(dct, response)
        #
        if next_page_url and self.page_has_data:
            # url 与 回调函数 抛出请求
            yield Request(url=next_page_url,
                          callback=getattr(self, caller_name)
                          , meta=response.meta)


    def __get_list(self, dct, article_id, response):
        pass

    def __get_file(self, dct, article_id, response):
        """扔出文件请求包给pipeline处理"""
        d = dct["file"]
        file_link = response.xpath(d["xpath"]).xpath('.//@href').extract()

        file_item = items.FileItem()
        file_item['file_urls'] = [self._fix_url(link, response) for link in file_link]
        file_item['farea'] = self.name
        file_item['farticleid'] = article_id

        yield file_item

    def __get_text(self, dct, article_id, response):
        d = dct["text"]

        self.article_xpath = d["xpath"] # 给keyword用
        text_item = items.TextItem()
        selectors = response.xpath(d["xpath"])
        text_item['farticleid'] = article_id
        text_item['fhtml'] = response.text # todo 编码问题
        text_item["fartcle"] = selectors.get()
        self.text = selectors.xpath('string(.)').extract_first()
        text_item["ftext"] = self.text

        yield text_item

    def __get_key_word(self, dct, article_id, response):
        d = dct["key_word"]
        #初始化提取关键字 的item
        key_word_item = items.KeywordItem()
        key_word_item['farticleid'] = article_id
        #     关键字：time       表达式列表：【re_str, re_str, re_str】
        for key_word, expression_list in d.items():
            # 循环expression_list中的正则，并提取文章内容。
            tmp_result = self.loop_extract(expression_list, response)
            key_word_item[key_word] = tmp_result
            yield key_word_item


    def loop_extract(self, expression_list, response):
        # 循环expression_list中的正则，并提取文章内容。提取成功才返回结果
        for expression in expression_list:
            if expression.startswith('/'):
                selectors = response.xpath(self.article_xpath)
                tmp_result = ','.join(selectors.xpath(expression).extract())
            else:
                re_str = self.my_re2re(expression)
                tmp_result = re.findall(re_str, self.text)
            if tmp_result:
                return tmp_result[0]
            else: continue
        return ''

    def my_re2re(self, expression):
        # 我的正則轉成真正的正則
        re_list = re.split(r'\)|\(', expression)
        if len(re_list) == 3:
            re_str = re_list[0] + '[\n\r\t ]+(.+)' + re_list[2]
            return re_str
        elif len(re_list) == 2:
            end = re_list[1].replace('...', '')
            if end:
                re_str = re_list[0] + '[\n\r\t ]+(.+' + end + ')'
            else:
                re_str = re_list[0] + '[\n\r\t ]+(.+' + '[\n\r\t ]+'
            return re_str
        else:
            raise Exception("keyword: key_word error")

    def __item_loader(self, item_name, dct, response, selector=None, load_type="html"):
        """
        :param dct:  item_name and  xpath
        :param selector:  提取目标
        :param response: 提取目标
        """
        if load_type == "json":
            result_item = getattr(items, item_name)()
            item_dict = dict()
            for name, param in dct.items():
                method = param[0]
                path = param[1]
                if method == "json":
                    item_dict[name] = self.__json_path(path, selector)
                elif method == "format":
                    item_dict[name] = path.format(self=self, **item_dict)
            item_dict = {name: value for name, value in item_dict.items() if not name.startswith("__")}
            result_item.update(item_dict)

        elif load_type == "html":
            item = getattr(items, item_name)
            row_item_loader = ItemLoader(item=item(), selector=selector)
            for name, param in dct.items():
                method = param[0]
                path = param[1]
                getattr(row_item_loader, method)(name, path)
            # 提取出来item
            result_item = row_item_loader.load_item()

        # url 相对-> 绝对
        print(result_item["furl"])
        if result_item["furl"]:
            result_item["furl"] = self._fix_url(result_item["furl"], response)
        return result_item

    def __yield_request(self,url, dct_requests, response):
        """
        :param url_list:  请求列表
        :param dct_yield:  含有回调函数名
        :param response:
        :return:
        """
        yield Request(
            url=self._fix_url(url, response),
            meta=response.meta,
            callback=getattr(self, dct_requests['callback'])
        )

    def _get_next_page_url(self, dct, response):
        """
        demand：
            self.nextpage_xpath  or  self.nextpage_url_num_re
            self.main_url
        要么用xpath获取，要么num+1，返回下一页url
        :param url:
        :param response:
        :return:
        """
        if "xpath" in dct:
            relative_url = response.xpath(dct["xpath"])
            return self._relative_to_absolute(relative_url, response)

        elif "url_num" in dct:
            return self._get_url_by_increase_num(dct["url_num"], response.url)

    def _fix_url(self, url, response):
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
        elif not url.startswith('http'):
            return response.url + url
        return url

    def _get_url_by_increase_num(self, re_extract_num, url):
        """
        demand:
            self.nextpage_url_num_extract_re
        用正则提出这一页url的页数+1后覆盖原页数，返回下一页url
        :param url: 这一页的url
        :return: 下一页url
        """
        re_result = re.search(re_extract_num, url)
        if re_result:
            num = int(re_result.group(1))
            num += 1
            num_start_index = re_result.regs[1][0]
            num_end_index = re_result.regs[1][1]
            return url[:num_start_index] + str(num)+ url[num_end_index:]

    # @classmethod
    # def _get_self_func_name(cls):
    #     return traceback.extract_stack()[-2][2]
    #
    # @classmethod
    # def _get_caller_func_name(cls):
    #     return traceback.extract_stack()[-3][2]