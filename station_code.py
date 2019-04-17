import json
import os
import re


class StationCode:
    """
    获取车站电报码
    """

    @staticmethod
    def get_station_code(browser):
        """
        获取车站电报码
        :param browser: 浏览器对象
        """
        # 判断车站电报码文件是否存在
        if os.path.exists('station_code.txt'):
            return
        station_url = 'https://kyfw.12306.cn/otn/resources' \
                      '/js/framework/station_name.js?' \
                      'station_version=1.9018'
        rsp = browser.get_url(station_url)
        # print(rsp.text)
        pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
        result = re.findall(pattern, rsp.text)
        # 注意编码格式utf-8
        station = dict(result)
        with open('station_code.txt', 'w', encoding='utf-8') as f:
            # ensure_ascii = False 是为了防止乱码
            f.write(json.dumps(station,ensure_ascii = False))

    @staticmethod
    def get_codes_dict():
        """
        获取电报码字典
        :return: 电报码字典
        """
        with open('station_code.txt', 'r', encoding='utf-8') as file:
            dict = json.load(file)
            return dict
