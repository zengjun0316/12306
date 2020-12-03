import requests
from requests.cookies import RequestsCookieJar
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
# 哈哈哈哈
#hehe
# 禁用安全请求警告
disable_warnings(InsecureRequestWarning)


class Browser(object):
    """测试GIT"""
    """
    建立模拟浏览器，用于进行cookie存储，发送get、post请求等的操作。
    """

    def __init__(self):
        """
        初始化浏览器信息
        """
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/70.0.3538.77 Safari/537.36'
                        }
        self.session = requests.Session()  # 定义session，保持一个会话
        self.cookie_jar = RequestsCookieJar()  # 用于保存cookie

    def get_url(self, url):
        """
        get请求
        :param url:
        :return: 请求结果
        """
        return self.session.get(url, headers=self.headers, cookies=self.cookie_jar)

    def post_url(self, url, data):
        """
        post请求
        :param url: 地址
        :param data: post请求参数
        :return: 请求结果
        """
        return self.session.post(url, data=data, headers=self.headers, cookies=self.cookie_jar, timeout=3)
