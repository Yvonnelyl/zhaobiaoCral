from sendMail import send_mail
import retrying
from scrapy import cmdline
import redis
from myschedual import Schedule
from zhaobiaoCral.settings import  REDIS_CONN
from multiprocessing import Pool
import time


@retrying.retry(retry_on_exception=ConnectionRefusedError, stop_max_attempt_number=3)
def push_by_schedual():
    r = redis.StrictRedis(**REDIS_CONN)
    # todo
    for cral_name in Schedule():
        try:
            r.lpush("zbcral", cral_name)
        except Exception:
            raise ConnectionRefusedError


@retrying.retry(retry_on_exception=ConnectionRefusedError, stop_max_attempt_number=3)
def check_run_loop():
    """
    从redis爬虫任务队列里取出一个爬虫任务，并
    """

    r = redis.StrictRedis(**REDIS_CONN)

    while True:
        # 查看redis
        try:
            cral_name = r.lindex('zbcral', -1)
        except Exception:
            raise ConnectionRefusedError

        if cral_name:
            #start cral
            cmdline.execute(f'scrapy crawl {cral_name}'.split())
        else:
            time.sleep(1)


def mycallback_run():
    # 发送邮件
    send_mail('招标爬虫', 'check_run错误')

def mycallback_push():
    # 发送邮件
    send_mail('招标爬虫', 'push错误')

if __name__ == '__main__':
    pool = Pool(2)
    pool.apply_async(check_run_loop, callback=mycallback_run)
    pool.apply_async(push_by_schedual, callback=mycallback_push)
    pool.close()
    pool.join()