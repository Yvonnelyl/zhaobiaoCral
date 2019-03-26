from scrapy import cmdline
import redis

name = 'shanxi'
r = redis.StrictRedis()
r.delete("zbcral")
r.lpush('zbcral',name)
p = 'scrapy crawl ' + name
cmdline.execute(p.split())
