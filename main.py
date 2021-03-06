from sendMail import send_mail
import retrying
import redis
from myschedual import Schedule
from multiprocessing import Pool
import time
import subprocess


def run():
    s = Schedule()
    s.run()


@retrying.retry(retry_on_exception=ConnectionRefusedError, stop_max_attempt_number=3)
def check_run_loop():
    """
    从redis爬虫任务队列里取出一个爬虫任务，并
    """

    from zhaobiaoCral.settings import REDIS_CONF

    r = redis.StrictRedis(**REDIS_CONF["redis_conf"])
    tmp = ''

    while True:
        # 查看redis
        try:
            cral_name = r.lindex(REDIS_CONF["queue_name"], -1)
            if cral_name == tmp:
                continue
            tmp = cral_name
        except Exception:
            raise ConnectionRefusedError

        if cral_name:
            #start cral
            cral_name = cral_name.decode("utf-8")
            subprocess.Popen(f'scrapy crawl {cral_name} -s LOG_FILE=log/{cral_name}.log'.split())
            time.sleep(10)
        else:
            time.sleep(1)


def mycallback_run():
    # 发送邮件
    send_mail('招标爬虫', 'check_run错误')
    print('招标爬虫', 'check_run错误')

def mycallback_push():
    # 发送邮件
    send_mail('招标爬虫', 'push错误')
    print('招标爬虫', 'check_run错误')

if __name__ == '__main__':
    pool = Pool(2)
    pool.apply_async(check_run_loop, callback=mycallback_run)
    pool.apply_async(run, callback=mycallback_push)
    pool.close()
    pool.join()