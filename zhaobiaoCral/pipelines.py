# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



class OracleAsyncPipeline(object):
    """
    oracle异步写入的通道
    """
    def open_spider(self, spider):
        """爬虫运行后的数据库连接"""
        conn_dct = {
            "dsn": "200.100.100.69/dgr",
            "user":"hiibase",
            "password":"hiibase"
        }
        self.insert_sqls = [sql for sql in self.get_insert_sql()]
        self.dbpool = adbapi.ConnectionPool('cx_Oracle', **conn_dct)

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def close_spider(self, spider):
        self.dbpool.close()

    def insert_db(self, tx, item):
        for insert_sql in self.insert_sqls:
            table_name = insert_sql[0]
            sql = insert_sql[1]
            clns = [cln for cln in self.insert_table[table_name]]
            try:
                values = [item[cln][0] for cln in clns]
            except KeyError:
                continue
            tx.execute(sql, tuple(values))

    def get_insert_sql(self):
        conf = self.get_cral_conf()
        self.insert_table = conf["dct"]["table"]
        for table_nm in self.insert_table:
            cln = ','.join(self.insert_table[table_nm])
            value_format = ','.join([':' + str(num) for num in range(1, len(self.insert_table[table_nm]) + 1)])
            sql = f'INSERT INTO {table_nm} ({cln}) VALUES ({value_format})'.format()
            yield (table_nm, sql)

    def get_cral_conf(self):
        with open(r'C:\Users\Admin\PycharmProjects\scrapyProjects\zhaobiaoCral\test.json', 'rb') as f:
            return json.loads(f.read())


class MyFilesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 提取url前面名称作为图片名
        image_name = request.url.split('/')[-1]
        # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        folder_strip = re.sub(r'[?\\*|“<>:/]', '', str(name))
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(folder_strip, image_name)
        return filename
