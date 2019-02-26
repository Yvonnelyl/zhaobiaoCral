import json
import redis
from .zhaobiaoBaseSpider import BaseSpider



class _zhaobiaoSpiderCreator():
    """
    招标爬虫生成器，当用cmdline运行scrapy爬虫的时候必定会用此类生成爬虫
    """
    def __new__(cls, create_type, redis_conf=None, queue_name=None):
        # 获得cral conf json
        get_cral_conf = _GetCralConf(create_type, redis_conf=None, queue_name=None)
        cral_conf_dct = get_cral_conf.get()
        # 把所有的函数放入字典中
        for func_name in cral_conf_dct['func']:
            cral_conf_dct.update(
                {func_name: cls.get_wanted_func(func_name)}
            )

        # 返回爬虫类
        return type(cral_conf_dct['name'], (BaseSpider,), cral_conf_dct)

    @classmethod
    def get_wanted_func(cls, func_name):
        """
        获取想要的函数
        :param func_name:  函数名
        :param dct:  函数参数
        """
        def tmp(self, response):
            for parse_name in self.func[func_name]:
                # 获取功能型方法
                f = getattr(self, parse_name)
                # 有参数的方法，带上函数参数
                if  self.func[func_name][parse_name] != {}:
                    yield from f(self.func[func_name][parse_name], response)
                else: yield from f(response)
        #   函数名更换
        tmp.__name__ = func_name
        return tmp


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
        r = redis.StrictRedis(**self.redis_conf)
        return r.brpop(self.queue_name)


# create new spider
FleshSpider = _zhaobiaoSpiderCreator(
    "redis",
    redis_conf={"host": "localhost", "port": 6379},
    queue_name="zbcral")