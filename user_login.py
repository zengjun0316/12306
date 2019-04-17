import getpass
from analog_browser import Browser
from user_verify import Captcha
from json import loads


class Login:
    """
    12306的用户登录,以及登录之后的两次验证。
    """
    browser = Browser() # 创建浏览器对象

    def __init__(self):
        self.browser = Login.browser
        self.username = ''
        self.password = ''

    def login(self, browser):
        """
        用户登录
        :param browser:
        :return:
        """
        login_url = 'https://kyfw.12306.cn/passport/web/login'
        self.username = input("请输入12306账号:")
        self.password = getpass.getpass("请输入密码:")
        user_data = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn'
        }

        rsp = browser.post_url(login_url, user_data)
        html = loads(rsp.content)
        return html

    def first_verify(self):
        """
        登录之后的第一次验证
        :return: 请求结果
        """
        print("------------第一次验证------------")
        first_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        first_data = {
            'appid': 'otn'
        }
        rsp = self.browser.post_url(first_url, first_data)
        html = loads(rsp.content)
        return html

    def second_verify(self, apptk):
        """
        登录之后的第二次验证
        :param apptk: 请求所需参数
        :return: 请求结果
        """
        print("------------第二次验证------------")
        second_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        second_data = {
            'tk': apptk,
        }
        rsp = self.browser.post_url(second_url, second_data)
        # print(rsp.text)
        html = loads(rsp.content)
        return html

    def sys_login(self):
        """
        用户登录主程序
        :return:
        """
        self.login(self.browser)
        result = self.first_verify()
        try:
            result = self.second_verify(result['newapptk'])
        except:
            print("登录失败,账号或密码错误!")
            Captcha().sys_verify()
            self.sys_login()
        self.username = result["username"]
        print("欢迎用户", result["username"], "您已登录成功！") if result["result_code"] == 0 else print(
            result["result_message"])
        return
