# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from .items import FileItem
from twisted.enterprise import adbapi
from scrapy.pipelines.files import FilesPipeline, FileException
from scrapy import Request
from base.fileType import filetype
import re
from hashlib import md5
from zhaobiaoCral.settings import  ACCEPTFILETYPE

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ZBFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        # if isinstance(item, items.FileItem):
        return [
            Request(x, meta={'farea': item['farea']}) for x in item.get(self.files_urls_field, [])
        ]

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
        if not isinstance(item, FileItem):
            return item
        file_paths = [x['path'] for ok, x in results if ok]
        # 如果是file下载又为空就扔掉
        if not file_paths:
            raise DropItem("Item contains no files")
        else:
            # 把字符串拼起来
            item['fpath'] = ','.join(file_paths)
            item['file_urls']  = ','.join(item['file_urls'])

        return item

    def file_path(self, request, response=None, info=None):
        if hasattr(self, "doc_type_code"):
            path = self.__get_path(self.doc_type_code, request)
            return path
        else: return ''


    def __get_path(self, doc_type_code, request):
        # 接收上面meta传递过来的图片名称
        farea = request.meta['farea']
        # 提取url前面名称作为图片名
        file_name = re.split(r'/', request.url)[-1]
        # 若没有后缀名 根据文件头判断后缀名
        if not re.search(r"\.[a-zA-Z]+$", file_name):
            file_type = filetype(doc_type_code)

            if '=' in file_name:
                # 如果是垃圾，只能转码成md5 32字符串作为文件名
                file_name = md5(file_name.encode("utf-8")).hexdigest()
            file_name += f'.{file_type}'
            # 清洗Windows系统的文件夹非法字符，避免无法创建目录
            folder_strip = re.sub(r'[?\\*|“<>:/]', '', str(farea))
            # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
            filename = u'{0}/{1}'.format(folder_strip, file_name)
            return filename

        else:
            folder_strip = re.sub(r'[?\\*|“<>:/]', '', str(farea))
            filename = u'{0}/{1}'.format(folder_strip, re.sub("\&.+", "", file_name))

            # 清除 不是base.acceptFileType中包含的文件类型
            for _, file_type_name in ACCEPTFILETYPE.items():
                if filename.endswith(file_type_name):
                    return filename
            raise FileException

        # 看是不是文件名 or 请求的.html?一堆参数&之类的垃圾


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
        # if self.judge_item(item):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        if isinstance(item, FileItem):
            pass
        item_name = re.search('.+\.(.+)\'', str(item.__class__))[1]
        d = dict(item)

        # 表名, 字段名, 变量
        table_name = self.item_table_dict[item_name]
        cln_name_list = list(d)
        cln_values = tuple(d.values())

        # 生成sql
        sql = self._get_insert_sql(table_name, cln_name_list)
        # 运行
        try:
            tx.execute(sql, cln_values)
        except Exception:
            print(cln_values)
            raise Exception(cln_values)


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