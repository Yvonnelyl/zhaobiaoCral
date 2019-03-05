# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from .items import *
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Text2VectorPipeline():
    """
    把文件分类成词向量，并作处理
    """


class ExtractKeywordPipeline():
    """
    把关键词提取出来
    """


class OracleAsyncPipeline():
    """
    oracle异步写入的通道
    """
    def __init__(self, conn_dct):
        self.dbpool = adbapi.ConnectionPool('cx_Oracle', **conn_dct)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            conn_dct=crawler.settings.get('ORACLE_CONN')
        )

    def open_spider(self, spider):
        """爬虫运行后的数据库连接"""
        self.tablename_n_sql_list = [tablename_n_sql for tablename_n_sql in self.get_insert_sql()]

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def close_spider(self, spider):
        self.dbpool.close()

    def insert_db(self, tx, item):
        for tablename_n_sql in self.tablename_n_sql_list:
            # 获取表名与insert—sql
            table_name = tablename_n_sql[0]
            sql = tablename_n_sql[1]
            columns = self.get_columns(table_name)
            try:
                # 提取出item中的准备插入该表的值
                values = [item[cln][0] for cln in columns]
            except KeyError:
                continue
            tx.execute(sql, tuple(values))

    def get_columns(self, table_name):
        """
        获取table的列
        """
        return [cln for cln in self.insert_table[table_name]]

    def get_insert_sql(self):
        """
        根据
        :return:
        """

        conf = self.get_cral_conf()
        self.insert_table = conf["dct"]["table"]

        for table_nm in self.insert_table:
            cln = ','.join(self.insert_table[table_nm])
            value_format = ','.join([':' + str(num) for num in range(1, len(self.insert_table[table_nm]) + 1)])
            sql = f'INSERT INTO {table_nm} ({cln}) VALUES ({value_format})'.format()
            yield (table_nm, sql)

    def get_cral_conf(self):
        with open(r'C:\Users\Admin\PycharmProjects\scrapyProjects\zhaobiaoCral\item.json', 'rb') as f:
            return json.loads(f.read())


class ZhaoBiaoFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, FileItem):
            for file_url in item['file_urls']:
                yield scrapy.Request(file_url)
        else:
            return item

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
        item['file_paths'] = file_paths
        return item

    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 提取url前面名称作为图片名
        file_name = request.url.split('/')[-1]
        # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        folder_strip = re.sub(r'[?\\*|“<>:/]', '', str(name))
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(folder_strip, file_name)
        return filename
