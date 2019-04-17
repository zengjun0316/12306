from datetime import datetime

import time

from station_code import StationCode
from color import Color


class Utility(object):
    @classmethod
    def red_color(cls, code):
        return Color.red(code)

    @classmethod
    def green_color(cls, code):
        return Color.green(code)

    # 将历时转化为小时和分钟的形式
    @classmethod
    def get_duration(cls, time_str):
        duration = time_str.replace(':', '时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        return duration

    # 根据车站名获取电报码
    @classmethod
    def get_station_code(cls, station):
        codes_dict = StationCode().get_codes_dict()
        if station in codes_dict.keys():
            return codes_dict[station]

    # 输入出发地和目的地
    @classmethod
    def input_station(cls, code):
        station = input('{}：\n'.format(code))
        if not station in StationCode().get_codes_dict().keys():
            print(Color.red('Error:车站列表里无法查询到{}'.format(station)))
            station = input('{}：\n'.format(code))
        return station

    # 输入乘车日期
    @classmethod
    def input_train_date(cls):
        train_date = input('请输入购票时间,格式为2019-05-01:\n')
        try:
            train_time_structure = time.strptime(train_date, "%Y-%m-%d")
        except:
            print('时间格式错误，请重新输入')
            train_date = input('请输入购票时间,格式为2019-05-01:\n')
        time_flag, train_date = Utility.check_date(train_date)
        if not time_flag:
            train_date = input('请输入购票时间,格式为2019-05-01:\n')
            time_flag, train_date = Utility.check_date(train_date)
        return train_date

    @classmethod
    def get_train_date(cls, date_str):
        # 返回格式 Wed Aug 22 2018 00: 00:00 GMT + 0800 (China Standard Time)
        # 转换成时间数组
        time_array = time.strptime(date_str, "%Y%m%d")
        # 转换成时间戳
        timestamp = time.mktime(time_array)
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式
        gmt_format = '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)'
        time_str = time.strftime(gmt_format, time_local)
        return time_str

        # 获取一个时间是周几

    @classmethod
    def get_week_day(cls, date):
        week_day_dict = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五',
            5: '周六',
            6: '周天',
        }
        day = datetime.strptime(date, '%Y-%m-%d').weekday()
        return week_day_dict[day]

    # 转化日期格式
    @classmethod
    def get_date_format(cls, date):
        month = ''
        day = ''
        # date格式为2019-05-01
        date_list = date.split('-')
        if date_list[1].startswith('0'):
            month = date_list[1].replace('0', '')

        if date_list[2].startswith('0'):
            day = date_list[2].replace('0', '')
        return '{}月{}日'.format(month, day)

    # 检查购票日期是否合理
    @classmethod
    def check_date(cls, date):

        local_time = time.localtime()

        local_date = '%04d-%02d-%02d' % (local_time.tm_year, local_time.tm_mon, local_time.tm_mday)

        # 获得当前时间时间戳
        current_time_stamp = int(time.time())
        # 预售时长的时间戳
        delta_time_stamp = '2505600'
        # 截至日期时间戳
        dead_time_stamp = current_time_stamp + int(delta_time_stamp)
        # 获取预售票的截止日期时间
        dead_time = time.localtime(dead_time_stamp)
        dead_date = '%04d-%02d-%02d' % (dead_time.tm_year, dead_time.tm_mon, dead_time.tm_mday)
        # print(Colored.red('请注意合理的乘车日期范围是:{} 至 {}'.format(localDate, deadDate)))

        # 判断输入的乘车时间是否在合理乘车时间范围内
        # 将购票日期转换为时间数组
        train_time_structure = time.strptime(date, "%Y-%m-%d")
        # 转换为时间戳:
        train_time_stamp = int(time.mktime(train_time_structure))
        # 将购票时间修改为12306可接受格式 ，如用户输入2018-8-7则格式改为2018-08-07
        train_time = time.localtime(train_time_stamp)
        train_date = '%04d-%02d-%02d' % (train_time.tm_year, train_time.tm_mon, train_time.tm_mday)
        # 比较购票日期时间戳与当前时间戳和预售截止日期时间戳
        if current_time_stamp <= train_time_stamp <= dead_time_stamp:
            return True, train_date
        else:
            print(Color.red('Error:您输入的乘车日期:{}, 当前系统日期:{}, 预售截止日期:{}'.format(train_date, local_date, dead_date)))
            return False, None
