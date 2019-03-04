from sendMail import send_mail
import retrying
from scrapy import cmdline
import redis
from myschedual import Schedule
from multiprocessing import Pool
import time


s = Schedule()


@retrying.retry(retry_on_exception=ConnectionRefusedError, stop_max_attempt_number=3)
def check_run_loop():
    """
    从redis爬虫任务队列里取出一个爬虫任务，并
    """

    from zhaobiaoCral.settings import REDIS_CONF

    r = redis.StrictRedis(**REDIS_CONF["redis_conn"])

    while True:
        # 查看redis
        try:
            cral_name = r.lindex(REDIS_CONF["queue_name"], -1)
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
    pool.apply_async(s.run, callback=mycallback_push)
    pool.close()
    pool.join()