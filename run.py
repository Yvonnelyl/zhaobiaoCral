from scrapy import cmdline
import redis
import json

while True:
    r  = redis.StrictRedis(host='localhost', port=6379)
    cral_conf_json = r.rpop('zbcral')
    json.
    cmdline.execute('scrapy crawl '.split())

{

}