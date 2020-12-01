from prettytable import PrettyTable
from json import loads
from utility import Utility
from user_login import Login
from station_code import StationCode
from color import Color


class Query:
    """
    查询火车余票信息。
    """

    def __init__(self):
        """
        初始化查票信息
        """
        # 简单测试git
        self.browser = Login.browser
        # 座位类型，订票下单时需要传入
        self.noSeat = '1'  # 无座
        self.firstClassSeat = 'M'  # 一等座
        self.secondClassSeat = 'O'  # 二等座
        self.advancedSoftBerth = '6'  # 高级软卧 A6
        self.hardBerth = '3'  # 硬卧 A3
        self.softBerth = '4'  # 软卧 A4
        self.moveBerth = 'F'  # 动卧
        self.hardSeat = '1'  # 硬座 A1
        self.businessSeat = '9'  # 商务座 A9

    @staticmethod
    def query_data():
        """
        查票信息（日期，出发地，目的地等）
        :return: 用户输入的查票信息字典
        """
        train_date = Utility.input_train_date()  # 日期
        from_station = Utility.input_station('请输入出发地')  # 出发地
        to_station = Utility.input_station('请输入目的地')  # 目的地
        from_station_code = Utility.get_station_code(from_station)  # 出发地电报码
        to_station_code = Utility.get_station_code(to_station)  # 目的地电报码

        query_data = {  # 用户输入的查票信息字典
            'fromStation': from_station,
            'toStation': to_station,
            'trainDate': train_date,
            'fromStationCode': from_station_code,
            'toStationCode': to_station_code
        }
        return query_data

    def get_query(self):
        """
        查找符合用户需要的火车信息
        :return: 符合用户需求的所有火车信息字典，以及用户输入的查票信息字典
        """
        StationCode.get_station_code(self.browser)  # 判断电报码文件是否存在
        query_data = self.query_data()

        url = (
            'https://kyfw.12306.cn/otn/leftTicket/query?'
            'leftTicketDTO.train_date={}&'
            'leftTicketDTO.from_station={}&'
            'leftTicketDTO.to_station={}&'
            'purpose_codes=ADULT'
        ).format(query_data['trainDate'],
                 query_data['fromStationCode'],
                 query_data['toStationCode'])
        # print(url)
        rsp = self.browser.get_url(url)
        html = loads(rsp.content)
        train_dicts = self.get_ticket_format(html, query_data)
        return train_dicts, query_data

    def get_ticket_format(self, result, query_data):
        """
        打印车票信息
        :param result: 请求返回的结果
        :param query_data: 用户输入的查票信息字典
        :return: 符合用户需求的所有火车信息字典
        """
        train_dict = {}  # 车次信息字典
        train_dicts = []  # 用于订票
        trains = []  # 用于在terminal里打印

        results = result['data']['result']
        maps = result['data']['map']

        for item in results:
            train_info = item.split('|')
            if train_info[11] == 'Y':

                train_dict['secretStr'] = train_info[0]

                train_dict['trainNumber'] = train_info[2]  # 5l0000D35273

                train_dict['trainName'] = train_info[3]  # 车次名称，如K232

                train_dict['fromTelecode'] = train_info[6]  # 出发地电报码

                train_dict['toTelecode'] = train_info[7]  # 出发地电报码

                train_dict['fromStation'] = maps[train_info[6]]  # 茂名

                train_dict['toStation'] = maps[train_info[7]]  # 河源

                train_dict['departTime'] = Color.green(train_info[8])  # 出发时间

                train_dict['arriveTime'] = Color.red(train_info[9])  # 到达时间

                train_dict['totalTime'] = Utility.get_duration(train_info[10])  # 总用时

                train_dict['leftTicket'] = train_info[12]  # 余票

                train_dict['trainDate'] = train_info[13]  # 2019-05-01

                train_dict['trainLocation'] = train_info[15]  # H2

                # 以下顺序貌似也不是一直固定的，我遇到过代表硬座的几天后代表其他座位了
                train_dict[self.businessSeat] = train_info[32]  # 商务座

                train_dict[self.firstClassSeat] = train_info[31]  # 一等座

                train_dict[self.secondClassSeat] = train_info[30]  # 二等座

                train_dict[self.advancedSoftBerth] = train_info[21]  # 高级软卧

                train_dict[self.softBerth] = train_info[23]  # 软卧

                train_dict[self.moveBerth] = train_info[33]  # 动卧

                train_dict[self.noSeat] = train_info[26]  # 无座

                train_dict[self.hardBerth] = train_info[28]  # 硬卧

                train_dict[self.hardSeat] = train_info[29]  # 硬座

                train_dict['otherSeat'] = train_info[22]  # 其他

                # 如果值为空，则将值修改为'--',有票则有字显示为绿色，无票红色显示
                for key in train_dict.keys():
                    if train_dict[key] == '':
                        train_dict[key] = '--'
                    if train_dict[key] == '有':
                        train_dict[key] = Color.green('有')
                    if train_dict[key] == '无':
                        train_dict[key] = Color.red('无')

                train = [Color.magenta(train_dict['trainName']) + Color.green('[ID]') if train_info[18] == '1' else
                         train_dict['trainName'],
                         Color.green(train_dict['fromStation']) + '\n' + Color.red(train_dict['toStation']),
                         train_dict['departTime'] + '\n' + train_dict['arriveTime'],
                         train_dict['totalTime'], train_dict[self.businessSeat], train_dict[self.firstClassSeat],
                         train_dict[self.secondClassSeat], train_dict[self.advancedSoftBerth],
                         train_dict[self.softBerth],
                         train_dict[self.moveBerth], train_dict[self.hardBerth], train_dict[self.hardSeat],
                         train_dict[self.noSeat],
                         train_dict['otherSeat']]

                # 直接使用append方法将字典添加到列表中，如果需要更改字典中的数据，那么列表中的内容也会发生改变，这是因为dict在Python里是object，不属于primitive
                # type（即int、float、string、None、bool)。这意味着你一般操控的是一个指向object（对象）的指针，而非object本身。下面是改善方法：使用copy()
                trains.append(train)
                train_dicts.append(train_dict.copy())  # 注意trainDict.copy()

        self.pretty_print(trains, query_data)  # 按照一定格式打印
        return train_dicts

    @staticmethod
    def pretty_print(trains, queryData):
        """
        按照一定格式打印，美化
        :param trains: 所有火车信息
        :param queryData: 用户输入的查票信息字典
        """
        header = ["车次", "车站", "时间", "历时", "商务座", "一等座", "二等座", '高级软卧', "软卧", "动卧", "硬卧", "硬座", "无座", '其他']
        pt = PrettyTable(header)
        date = queryData['trainDate']
        title = '{}——>{}({} {}),共查询到{}个可购票的车次' \
            .format(queryData['fromStation'], queryData['toStation'],
                    Utility.get_date_format(date), Utility.get_week_day(date), len(trains))
        pt.title = Color.cyan(title)
        pt.align["车次"] = "l"  # 左对齐
        for train in trains:
            pt.add_row(train)
        print(pt)
