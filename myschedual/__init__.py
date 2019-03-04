# -*- coding: utf-8 -*-
import redis
from base.myio import get_file_dir, get_dir_son_file, json_to_dict
from zhaobiaoCral.settings import REDIS_CONF


class  Schedule():

    def __init__(self, redis_conf=REDIS_CONF):
        """
        :param schedule:  任务计划模块
        """
        # redis 连接
        self.redis_conn = redis_conf["redis_conn"]
        self.queque_name = redis_conf["queue_name"]
        self.r = redis.StrictRedis(**self.redis_conn)

        import schedule
        self.schedule = schedule
        # 爬虫函数参数
        self.run_spider_func_dict_param = {}
        # 爬虫计划任务参数字典
        schedule_path = 'cral_schedule.json'
        # 爬虫计划任务参数字典
        self.schedule_dict = json_to_dict(schedule_path)

    def run(self):
        """
        开始按计划运行
        :return:
        """
        # 爬虫时间设置
        self.__set_spider_schedule()
        # self.set_data_process_schedule()
        while True:
            self.schedule.run_pending()

    # def set_data_process_schedule(self):
    #     """
    #     三个数据处理操作设置定时任务
    #     :return:
    #     """
    #     conf_path = 'conf.json'
    #     run_project = Run(conf_path)
    #     tmp = self.schedule_dict['push']
    #     getattr(self.schedule.every(), tmp['period'][1]).at(tmp['at']).do(run_project.run_push)

    # def _get_spider_func_dict(self):
    #     """
    #     :return: 爬虫函数字典
    #     """
    #     self_path = get_file_dir(__file__)
    #     spider_path = self_path + '\spider'
    #     spider_pyfile_list = get_dir_son_file(spider_path)
    #     # 加入run spider函数
    #     for pyfile in spider_pyfile_list:
    #         self.run_spider_func_dict_param[pyfile.replace('.py', '')] = \
    #             'python ' + spider_path + '\\' + pyfile

    # 设定爬虫任务时间

    def __set_spider_schedule(self):
        """
        :param run_spider_func:  爬虫运行函数字典集合
        :param spider_schedule:  爬虫计划任务字典
        :return:
        """
        class _SpiderScheduleBeam():
            """
            一个dict to object
            """

            def __init__(self, spider_schedule):
                self.at = spider_schedule['at']
                self.unit = spider_schedule['period'][1]
                self.period = spider_schedule['period'][0]

        for spider_name in self.schedule_dict():
            # dict to object
            beam = _SpiderScheduleBeam(self.schedule_dict[spider_name])
            # 开始设定每个爬虫的计划
            getattr(self.schedule.every(), beam.unit).at(beam.at).do(
                # spider_name, r, queue
                self.r.lpush, self.queque_name, spider_name)

    # def __job_creator(self):
    #     #loop抛出job
    #     for spider_name in self.schedule_dict:
    #
    #         def job(spider_name, r, queue):
    #             r.lpush(queue, spider_name)
    #
    #         yield spider_name, job


if __name__ == '__main__':
    s  = Schedule()
    s.run()