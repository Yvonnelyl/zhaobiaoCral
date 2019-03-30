from scrapy import cmdline
import redis


def test_for_cral(cral_name):

    r = redis.StrictRedis()
    r.delete("zbcral")
    r.lpush('zbcral',name)
    p = 'scrapy crawl ' + name + ' -s LOG_FILE=log/test.log'
    cmdline.execute(p.split())

if __name__ == "__main__":
    name = 'henan'
    test_for_cral(name)