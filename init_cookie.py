from requests.cookies import RequestsCookieJar
import re
import time
from user_login import Login


class Cookie:
    """
    模拟浏览器第一次访问拿到需要的cookie值，为后面的访问做铺垫。
    """
    def __init__(self):
        self.browser = Login.browser
        self.cookie_jar = RequestsCookieJar()


    def cookies(self):
        """
        设置cookie，模拟初始访问，得到两个必须cookie，方便以后请求
        :return: cookie值
        """
        cookie_url = 'https://kyfw.12306.cn/otn/HttpZF/logdevice?' \
                     'algID=iWhWaBoyZ3&' \
                     'hashCode=qHw1myKMKxOlgLBZq5wSN8vEIE69yeXrumuJsvQCRmU&' \
                     'FMQw=0&q4f3=zh-CN&VPIf=1&custID=133&VEek=unknown&dzuS=0&' \
                     'yD16=0&EOQP=45ecafdf15a7630b9cfe4e92a00f952e&lEnu=180897178&' \
                     'jp76=52d67b2a5aa5e031084733d5006cc664&hAqN=Win32&' \
                     'platform=WEB&ks0Q=d22ca0b81584fbea62237b14bd04c866&' \
                     'TeRS=824x1536&tOHY=24xx864x1536&Fvje=i1l1o1s1&q5aJ=-8&' \
                     'wNLf=99115dfb07133750ba677d055874de87&' \
                     '0aew=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/73.0.3683.86%20Safari/537.36&' \
                     'E3gR=39707e804e88665a23836bd60110c00d&' \
                     'timestamp={}'.format(str(round(time.time() * 1000)))

        rsp = self.browser.get_url(cookie_url)
        # print(rsp.text)

        pattern = u'(?<=").*?(?=")'
        result = re.findall(pattern, rsp.text)
        # print(result)

        self.cookie_jar.set("RAIL_EXPIRATION", result[2], domain="kyfw.12306.cn")
        self.cookie_jar.set("RAIL_DEVICEID", result[10], domain="kyfw.12306.cn")
        return self.cookie_jar
