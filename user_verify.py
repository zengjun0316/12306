from json import loads
from PIL import Image


class Captcha:

    @staticmethod
    def get_image(browser):
        """
        获取验证图片到本地，并打开图片
        :param browser: 浏览器对象
        :return:
        """
        image_url = "https://kyfw.12306.cn/passport/captcha/captcha-image" \
                    "?login_site=E&module=login&rand=sjrand"
        rsp = browser.get_url(image_url)

        # 下载验证码图片
        with open('captcha.jpeg', 'wb') as f:
            f.write(rsp.content)
        # 打开图片
        img=Image.open('captcha.jpeg')
        img.show()
        img.close()

    def verify_img(self, browser):
        """
        验证码验证
        :param browser: 浏览器对象
        :return: 请求结果
        """
        coordinate = {
            '1': '42,42,',
            '2': '108,42,',
            '3': '185,42,',
            '4': '260,42,',  # 验证码的8个坐标
            '5': '42,118,',
            '6': '108,118,',
            '7': '185,118,',
            '8': '260,118,'
        }
        print("+----------+----------+----------+----------+")
        print("|    1     |    2     |    3     |    4     |")
        print("|----------|----------|----------|----------|")
        print("|    5     |    6     |    7     |    8     |")
        print("+----------+----------+----------+----------+")
        input_num = input("请在1—8中选择输入验证图片编号，以半角','隔开。(例如：1,3,5):")
        code = input_num.split(',')
        captcha = ''
        try:
            for i in code:
                # 判断i是否为第一个元素，是做=，不是做+=。
                captcha += coordinate[i] if (i is not input_num[0]) else coordinate[i]
        except:
            print("输入有误,请重新输入!")
            self.verify_img(browser)

        # 图片验证
        data = {
            'answer': captcha,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        rsp = browser.post_url(captcha_url, data)
        html = loads(rsp.content)
        return html

    # 验证系统
    def sys_verify(self, browser):
        """
        验证主程序
        :param browser: 浏览器对象，保持一个会话
        :return:
        """
        self.get_image(browser)
        verify_result = self.verify_img(browser)
        while verify_result['result_code'] is not '4':
            print('验证失败，已重新下载图片，请重新验证！')
            self.get_image(browser)
            verify_result = self.verify_img(browser)
        print("验证通过！")
        return
