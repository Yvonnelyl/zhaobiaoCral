# -*- coding: utf-8 -*-
import schedule
import time
from base.myio import get_file_dir, get_dir_son_file, json_to_dict
import subprocess


class  Schedule():

    def __init__(self, schedule = schedule):
        """
        :param schedule:  任务计划模块
        """
        self.schedule = schedule
        # 爬虫函数参数
        self.run_spider_func_dict_param = {}
        # 爬虫计划任务参数字典
        self.schedule_dict = None

    def run(self):
        self.set_spider_schedule()
        self.set_data_process_schedule()
        while True:
            self.schedule.run_pending()

    def set_spider_schedule(self):
        schedule_path = 'schedule_time.json'
        # 爬虫计划任务参数字典
        self.schedule_dict = json_to_dict(schedule_path)
        # 获取爬虫函数字典
        self._get_spider_func_dict()
        # 爬虫时间设置
        self._set_spider_schedule()

    def set_data_process_schedule(self):
        """
        三个数据处理操作设置定时任务
        :return:
        """
        conf_path = 'conf.json'
        run_project = Run(conf_path)
        tmp = self.schedule_dict['extract']
        getattr(self.schedule.every(), tmp['period'][1]).at(tmp['at']).do(run_project.run_extract_etl)
        tmp = self.schedule_dict['group']
        getattr(self.schedule.every(), tmp['period'][1]).at(tmp['at']).do(run_project.run_group)
        tmp = self.schedule_dict['push']
        getattr(self.schedule.every(), tmp['period'][1]).at(tmp['at']).do(run_project.run_push)

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
    def _set_spider_schedule(self):
        """
        :param run_spider_func:  爬虫运行函数字典集合
        :param spider_schedule:  爬虫计划任务字典
        :return:
        """
        for spider_name, spider_func_param in self.run_spider_func_dict_param.items():
            beam = _SpiderScheduleBeam(self.schedule_dict[spider_name])
            getattr(self.schedule.every(), beam.unit).at(beam.at).do(subprocess.Popen, spider_func_param)


class _SpiderScheduleBeam():
    def __init__(self, spider_schedule):
        self.at = spider_schedule['at']
        self.unit = spider_schedule['period'][1]
        self.period = spider_schedule['period'][0]


if __name__ == '__main__':
    s  = Schedule()
    s.run()