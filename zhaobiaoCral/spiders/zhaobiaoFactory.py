import json
import redis
from .zhaobiaoBaseSpider import BaseSpider
import datetime
from datetime import date, timedelta
from base.mydate import time_change_format


class _zhaobiaoSpiderCreator():
    """
    招标爬虫生成器，当用cmdline运行scrapy爬虫的时候必定会用此类生成爬虫
    """
    cral_conf_dct = {}
    def __new__(cls, create_type, redis_conf=None, queue_name=None):
        # 获得cral conf json
        get_cral_conf = _GetCralConf(create_type, redis_conf=redis_conf, queue_name=queue_name)
        cls.cral_conf_dct = get_cral_conf.get()

        cls.__add_func()
        cls.__add_log_conf()
        cls.__add_time()

        # 返回爬虫类
        return type(cls.cral_conf_dct['name'], (BaseSpider,), cls.cral_conf_dct)

    @classmethod
    def __add_func(cls):
        # 把所有的函数放入字典中
        for func_name in cls.cral_conf_dct['func']:
            cls.cral_conf_dct.update(
                {func_name: cls.__get_wanted_func(func_name)}
            )

    @classmethod
    def __get_wanted_func(cls, func_name):
        """
        获取想要的函数
        :param func_name:  函数名
        :param dct:  函数参数
        """

        def tmp(self, response):
            for parse_name in self.func[func_name]:
                # 获取功能型方法
                f = getattr(self, parse_name)
                d = {'caller_name': func_name}
                # 有参数的方法，带上函数参数
                if  self.func[func_name][parse_name] != {}:
                    yield from f(self.func[func_name][parse_name], response, **d)
                else: yield from f(response)
        #   函数名更换
        tmp.__name__ = func_name

        return tmp

    @classmethod
    def __add_log_conf(cls):
        # LOG CONF
        to_day = datetime.datetime.now()
        log_file_path = "log/{}_{}_{}_{}".format(cls.cral_conf_dct['name'], to_day.year, to_day.month, to_day.day)

        custom_settings = {
            # 设置管道下载
            # 'ITEM_PIPELINES': {
            #     'autospider.pipelines.DcdAppPipeline': 300,
            # },
            # 设置log日志
            'LOG_LEVEL': 'WARNING',
            'LOG_FILE': log_file_path
        }
        cls.cral_conf_dct.update(custom_settings)

    @classmethod
    def __add_time(cls):
        """
        为爬虫配置dict加上时间属性
        :return:
        """
        if "date_format" in cls.cral_conf_dct:
            date_format = cls.cral_conf_dct["date_format"][0]
        else:
            date_format = "%Y-%m-%d"
        period_str = cls.cral_conf_dct.get("period", "1")
        period = int(period_str) # 转成数字类型
        date_judge = 'start_time' in cls.cral_conf_dct and 'start_time' in cls.cral_conf_dct
        if not date_judge:
            # 添加今日start end date
            cls.cral_conf_dct["end_time"] = (
                    date.today()).strftime(date_format)

            cls.cral_conf_dct["start_time"]  = (
                    date.today() - timedelta(period)).strftime(date_format)

        # 建立不同格式的日期列表
        if "date_format" in cls.cral_conf_dct:
            date_format_list = cls.cral_conf_dct["date_format"]
            start_times, end_times = [], []
            for date_format in date_format_list:
                if not date_judge:
                    start_times.append((date.today()).strftime(date_format))
                    end_times.append((date.today() - timedelta(period)).strftime(date_format))
                else:
                    start_times.append(
                        time_change_format(cls.cral_conf_dct["start_time"], "%Y-%m-%d", date_format))
                    end_times.append(
                        time_change_format(cls.cral_conf_dct["end_time"], "%Y-%m-%d", date_format))
            # 添加今日start end date
            cls.cral_conf_dct["end_times"] = end_times
            cls.cral_conf_dct["start_times"] = start_times

class _GetCralConf():
    """
    获取cral conf
    """
    def __init__(self, source, redis_conf=None, queue_name=None):
        self.source = source
        if source == "redis":
            self.redis_conf = redis_conf
            self.queue_name = queue_name

    def get(self):
        """
        获取json
        :return:
        """
        return getattr(self, self.source)()

    def json(self):
        """
        test
        :return:
        """
        with open(r'C:\Users\Admin\PycharmProjects\scrapyProjects\zhaobiaoCral\test1.json', 'rb') as f:
            json_ = f.read()
            return json.loads(json_)

    def redis(self):
        """
        从
        :return:
        """
        r = redis.StrictRedis(**self.redis_conf)
        # 弹出爬虫名
        cral_name = r.rpop(self.queue_name).decode("utf-8")
        try:
            # 弹出爬虫conf json
            cral_json = r.get(cral_name)
        except:
            today = datetime.datetime.now()
            log_time = "  {}_{}_{}".format(today.year, today.month, today.day)
            error_info = 'redis  lost  json  cral_name:  ' + cral_name + log_time
            with open("log/run_log", "a") as f:
                f.write(error_info)
            raise Exception(error_info)

        cral_dct = json.loads(cral_json)
        return cral_dct

from ..settings import REDIS_CONF

# create new spider
FleshSpider = _zhaobiaoSpiderCreator(
    "redis", **REDIS_CONF)