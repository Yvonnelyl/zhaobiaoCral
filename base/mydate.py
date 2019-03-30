from datetime import datetime, date, timedelta
import time


def time_change_format(zw_time, old_format, new_format):
    """
    把中文格式时间：xx年xx月xx日
    转成：xx-xx-xx
    :param zw_time: 中文格式时间
    :return:        英文格式时间
    """
    t = time.strptime(zw_time, old_format)
    en_time = time.strftime(new_format, t)
    return en_time


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
