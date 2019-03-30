# -*- coding: utf-8 -*-
# Scrapy settings for zhaobiaoCral project
import  os

BOT_NAME = 'zhaobiaoCral'
SPIDER_MODULES = ['zhaobiaoCral.spiders']
NEWSPIDER_MODULE = 'zhaobiaoCral.spiders'
LOG_LEVEL = 'DEBUG'
# LOG_FILE = "mySpider.log"
DOWNLOAD_DELAY = 0.5
ITEM_PIPELINES = {
    'zhaobiaoCral.pipelines.ZBFilesPipeline': 250,
    'zhaobiaoCral.pipelines.OracleAsyncPipeline': 300,
}
project_dir = os.path.abspath(os.path.dirname(__file__))
# 保存路径
FILES_STORE = os.path.join(project_dir, "DownLoadFile")
FILES_URLS_FIELD = 'file_urls'
# 文件存储路径
FILES_EXPIRES = 90

#Self define param
ITEM_TABLE = {
    "FileItem": "fzbFile",
    "TextItem": "fzbText",
    "ListItem": "fzbList",
    "KeywordItem": "fzbKeyword"
}
ORACLE_CONN = {
   "dsn": "localhost/food",
   "user": "hii",
   "password": "hii"
}
REDIS_CONF  = {
   "redis_conf": {"host": "localhost", "port": 6379},
   "queue_name": "zbcral"
}
CREATE_ITEM = {
    "KeywordItem": [
        "money",
        "source_company"
    ]
}
ENGINE_INFO = "oracle+cx_oracle://hiibase:hiibase@200.100.100.69:1521/dgr",
# 下载文件时可以接受的文件类型
ACCEPTFILETYPE = {
        "d0cf11e0a1b11ae10000": 'xls',
        'ffd8ffe000104a464946': 'jpg',
        '89504e470d0a1a0a0000': 'png',
        '47494638396126026f01': 'gif',
        'd0cf11e0a1b11ae10000': 'doc',
        '255044462d312e350d0a': 'pdf',
        '504b0304140000080044': 'zip',
        '504b03040a0000080000': 'zip',
        '504b03040a0000000000': 'zip',
        '526172211a0700cf9073': 'rar',
        '1f8b0800000000000000': 'gz',
        '504b0304140006000800': 'docx',
        'd0cf11e0a1b11ae10000': 'wps',
}