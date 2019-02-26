from hashlib import md5
import requests
import retrying
import time


"""
若快，一个验证码识别平台
"""
header = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }
# request引擎
agent = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        ]

ruokuai_api_url = 'http://api.ruokuai.com/create.json'


class re_requests_exception(Exception):
    pass


class RuoKuai:
    """
    若快验证码识别模块
    """
    def __init__(self, username, password, soft_id,
                 soft_key, path, header=header,
                 agent=agent, ruokuai_api_url=ruokuai_api_url):
        """
        初始化验证码识别模块
        :param username: 用户名
        :param password: 密码
        :param soft_id:  内部变量（不变）=        :param soft_key: 内部变量（不变）
        :param path:     保存本地文件路径
        """
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        # 传递参数
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = header
        self.agent = agent
        self.path = path
        self.ruokuai_api_url = ruokuai_api_url

        self.base_params = dict()
        self.files = dict()

    def  loop_verify(self, im, verify_func,
                         im_type=2040, timeout=60, *args, **kwargs):
        """

        :param im:  图片字节流
        :param verify_func: 验证函数 must return a judge info like:
            def a():
                if 1:
                    return 1
                else:
                    return 0
        :param im_type:
        :param timeout:
        :param args: 验证函数参数
        :param kwargs: 验证函数参数
        :return:
        """
        self.load_img(im, im_type=im_type, timeout=timeout)
        self._loop_get_result(verify_func, *args, **kwargs)

    @retrying.retry(retry_on_exception=re_requests_exception, stop_max_attempt_number=5)
    def get_verify_code(self):
        r = requests.post(self.ruokuai_api_url, data=self.params, files=self.files, headers=self.headers)
        respond_json = r.json()
        if 'Result' not in respond_json:
            print("若快识别失败，1秒后更换验证码再次尝试")
            time.sleep(1)
            raise re_requests_exception
        return respond_json['Result']

    def load_img(self, im, im_type, timeout):
        """
        im: 图片字节
        im_type: 题目类型,若快网站上查，收费不。4位验证码为2040
        """
        self.params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        self.params.update(self.base_params)
        self.files = {'image': ('a.jpg', im)}

    @retrying.retry(retry_on_exception=re_requests_exception, stop_max_attempt_number=5)
    def _loop_get_result(self, verify_code_judge_func, *args, **kwargs):
        """
        :param verify_code_judge_func:  must return a judge info
        :return:
        """
        r = requests.post(self.ruokuai_api_url, data=self.params, files=self.files, headers=self.headers)
        respond_json = r.json()
        if not 'Result' in respond_json:
            print(u"若快识别失败，1秒后更换验证码再次尝试")
            time.sleep(1)
            raise re_requests_exception
        else:
            judge = verify_code_judge_func(respond_json['Result'], *args, **kwargs)
            if not judge:
                raise Exception('not a function returning judge info')
            if judge is False:
                raise re_requests_exception