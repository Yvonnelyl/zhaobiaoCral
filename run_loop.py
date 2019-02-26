from scrapy import cmdline
import redis
import json
import time


def get_detail_conf(cral_conf_json):
    """
    从cral_conf_json中获得更具体的参数
    :param cral_conf_json:
    """
    cral_name = cral_conf_json[1].decode('utf-8')
    return cral_name,


def get_detail_conf(r, ):
    r.brpop()


def loop_check_redis_cral():
    """
    从redis爬虫任务队列里取出一个爬虫任务，并
    """
    while True:
        r  = redis.StrictRedis(host='localhost', port=6379)
        cral_conf_json = r.brpop('zbcral')
        cral_name = get_detail_conf(r, cral_conf_json)
        cmdline.execute(f'scrapy crawl {cral_name} -s  LOG_FILE={cral_name}.log'.split())
        time.sleep(5)

if __name__ == "__main__":
    loop_check_redis_cral()