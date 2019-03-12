# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from . import items
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ZBFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, items.FileItem):
            return [Request(x, meta={'farea': item['farea']}) for x in item.get(self.files_urls_field, [])]

    def item_completed(self, results, item, info):
        """
        Here’s a typical value of the results argument:

                [(True,
                  {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
                   'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
                   'url': 'http://www.example.com/files/product1.pdf'}),
                 (False,
                  Failure(...))]
        """
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        else:
            item['fpath'] = ','.join(file_paths)
            item['file_urls']  = ','.join(item['file_urls'])

        return item

    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        farea = request.meta['farea']
        # 提取url前面名称作为图片名
        file_name = request.url.split('/')[-1]
        # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        folder_strip = re.sub(r'[?\\*|“<>:/]', '', str(farea))
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(folder_strip, file_name)
        return filename


class OracleAsyncPipeline():
    """
    oracle异步写入的通道
    """
    def __init__(self, conn_dct, item_table_dict):
        self.dbpool = adbapi.ConnectionPool('cx_Oracle', **conn_dct)
        self.item_table_dict = item_table_dict

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            conn_dct=crawler.settings.get('ORACLE_CONN'),
            item_table_dict=crawler.settings.get('ITEM_TABLE')
        )

    def open_spider(self, spider):
        """爬虫运行后的数据库连接"""
        pass

    def process_item(self, item, spider):
        if self.judge_item(item):
            self.dbpool.runInteraction(self.insert_db, item)
        return item

    def judge_item(self, item):
        if not isinstance(item, items.FileItem):
            return True

    def insert_db(self, tx, item):
        item_name = re.search('.+\.(.+)\'', str(item.__class__))[1]
        d = dict(item)

        # 表名, 字段名, 变量
        table_name = self.item_table_dict[item_name]
        cln_name_list = list(d)
        cln_values = tuple(d.values())

        # 生成sql
        sql = self._get_insert_sql(table_name, cln_name_list)

        # 运行
        tx.execute(sql, cln_values)

    def close_spider(self, spider):
        self.dbpool.close()

    def _get_insert_sql(self, table_name, cln_name_list):
        """
        拼接sql
        """
        # 生成"col1, col2, col3, col4"
        cln = ','.join(cln_name_list)
        # 生成 :1,:2,:3
        value_format = ','.join([':' + str(num) for num in range(1, len(cln_name_list) + 1)])
        # 拼接sql
        sql = f'INSERT INTO {table_name} ({cln}, fudtime, fisuse) VALUES ({value_format}, sysdate, \'1\')'.format()
        return sql


class FileInfoPipeline(OracleAsyncPipeline):
    def judge_item(self, item):
        if isinstance(item, items.FileItem):
            return True
