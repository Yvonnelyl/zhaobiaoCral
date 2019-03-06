# _*_ coding:utf-8 _*_
'''
简介：经纬度转换脚本
转化流程：
1.从具体某个表中查询出需要转化经纬度数据的城市列表
2.对第一步中产生的城市名称列表进行遍历，通过调用getdata函数，传入对应城市的名称，以及申请的百度密钥，返回经度和纬度数据
'''
import urllib2
from json import loads
import cx_Oracle
from util import *
import requests
import sys
reload(sys)
import time

sys.setdefaultencoding('utf8')

def getoracledata(sql):
    # 查询出要转换经纬度的数据，这里为大于2016年12月1日，不同表的查询语句可能不一样，但城市名必须作为第一列
    data = cur.execute(sql)
    data = data.fetchall()
    # print data
    return data


def getdata(addr, baidukey):
    addrOk = addr.replace(" ", "").replace("&" ,'').replace("#" ,'')
    print addrOk
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s

    ' % (addrOk, baidukey)
    print url
    # 爬取3w多条报错
    # jsonstr = urllib2.urlopen(url).read()
    # time.sleep(1)
    rq = requests.get(url=url)
    jsonstr = rq.content.decode()
    json = loads(jsonstr)
    status = json['status']
    msg = "x"
    if status == 0:
        lon = json['result']['location']['lng']
        lat = json['result']['location']['lat']
        print lon, lat
    else:
        lon = ""
        lat = ""
        msg = json["msg"]
    return lon, lat, addr, status, msg


def insertintooracle(update, lon, lat, addr):
    print 'start insert'
    update_list = update.split(",")
    cur.execute("update %s set %s=%f ,%s=%f  where %s='%s'" % (
        update_list[0], update_list[1] ,float(lon), update_list[2] ,float(lat), update_list[3] ,addr))
    # 更新经纬度的语句，对于不同的表，fcity的名字可能不一样，需要修改
    conn.commit()
    print update_list[0]
    print 'finished insert'

def main(addr_sql, key):
    for sql in addr_sql.values():
        data = getoracledata(sql["select"])
        print len(data)

        for i in range(0, len(data)):
            try:
                location = getdata(data[i][0].decode('GBK').encode('UTF-8'), key)
                lon = location[0]
                lat = location[1]
                addr = location[2]
                status = location[3]
                if status == 0:
                    insertintooracle(sql["update"], lon, lat, addr)
                else:
                    print location[4]
            except Exception as e:
                print e

# UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8 in position 0: ordinal not in range(128)
# print "解析错误：%s"%(location[4])
# 对于解析不了的，地址异常的，如何标志？免得遗留一起导致每次循环带来大量开销
# to-do


if __name__ == '__main__':
    jsonFile_name = "cgf_weather.json"
    cfg_data = loadJsonCfg(jsonFile_name)
    # connect='hii/hii@10.76.31.53/dgr'
    # conn = cx_Oracle.connect(connect)
    connStr = '%s/%s@%s/%s' % (
        cfg_data["jdbc"]["user"], cfg_data["jdbc"]["pwd"], cfg_data["jdbc"]["ip"], cfg_data["jdbc"]["dbname"])
    print connStr
    # conn = cx_Oracle.connect(connStr)
    # for cx_Oracle 6.0+，<6.0则应设置NLS_LANG环境变量
    conn = cx_Oracle.connect(connStr, encoding="GBK", nencoding="UTF-8")
    cur = conn.cursor()
    main(cfg_data["addr_sql"], cfg_data["keys"]["baidu_key"])
    conn.close()
