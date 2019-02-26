from datetime import datetime, date, timedelta
import time


def time_zw_to_en(zw_time):
    """
    把中文格式时间：xx年xx月xx日
    转成：xx-xx-xx
    :param zw_time: 中文格式时间
    :return:        英文格式时间
    """
    t = time.strptime(zw_time, '%Y年%m月%d日')
    en_time = time.strftime("%Y-%m-%d", t)
    return en_time


def time_list_zw_to_en(zw_time_list):
    """
    把中文格式时间的列表：[xx年xx月xx日,...,yy年yy月yy日]
    转成普通时间列表：[xx-xx-xx,...,yy-yy-yy]
    是上面方法   time_zw_to_en  的扩展
    :param zw_time_list: 中文格式时间列表
    :return:             英文格式时间列表
    """
    time_list = []
    for time_zw in zw_time_list:
        time_list.append(time_zw_to_en(time_zw))
    return time_list


def get_datetime_today():
    """
    得到今天的日期（str）
    :return:
    """
    t = date.today()  # date类型
      # date转str再转datetime
    return str(t)


def get_str_yesterday():
    """
    得到昨天的日期（str类型）
    :return:
    """
    today = get_datetime_today()
    dt = datetime.strptime(today, '%Y-%m-%d')
    yesterday = dt + timedelta(days=-1)  # 减去一天
    yesterday = yesterday.strftime("%Y-%m-%d")
    return yesterday


def now():
    """
    now str format(%Y-%m-%d %H-%M-%S)
    :return:
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
