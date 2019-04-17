import re
from json import loads
from urllib import parse
from utility import Utility
from query_ticket import Query
from user_login import Login


class BookTicket:
    def __init__(self):
        """
        初始化
        """
        self.browser = Login.browser
        self.seat_types_code = ["M", "O", "1", "N", "2", "3", "4", "F", "6", "9"]  # 座位类型列表
        self.seatType = "1"  # 默认’1‘硬座
        self.passenger_ticket_str = ''  # 购票所需的字符串
        self.old_passenger_str = ''  # 购票所需的字符串

    def check_user(self):
        """
        检查用户是否保持登录
        :return: True为成功标记
        """
        check_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        check_data = {
            '_json_att': ''
        }
        rsp = self.browser.post_url(check_url, check_data)
        # print(rsp.content)
        html = loads(rsp.content)
        if html['data']['flag']:
            return True
        else:
            print('检查失败，请重新登录')
            exit()

    def submit_order(self, query_data, train_dict):
        """
        提交订单，获取repeat_submit_token, key_check_is_change这两个参数
        :param query_data:用户输入的查找信息字典
        :param train_dict: 火车信息字典
        :return: repeat_submit_token, key_check_is_change
        """
        ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': parse.unquote(train_dict['secretStr']),
            'train_date': query_data['trainDate'],
            'back_train_date': '2019-04-12',
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': query_data['toStation'],
            'query_to_station_name': query_data['fromStation'],
            'undefined': ''
        }
        rsp = self.browser.post_url(ticket_url, data)
        html = loads(rsp.content)

        if html['status']:
            print('系统提交订单请求成功')
            print('---------验证获取rep_sub_token-----------')
            initdc = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
            data = {
                '_json_att': ''
            }
            rsp = self.browser.post_url(initdc, data)
            try:
                repeat_submit_token = re.findall(r"var globalRepeatSubmitToken = '(.*?)'", rsp.text)[0]
                key_check_is_change = re.findall(r"key_check_isChange':'(.*?)'", rsp.text)[0]
                return repeat_submit_token, key_check_is_change
            except:
                print('获取Token参数失败')

    def get_passenger(self, repeat_submit_token):
        """
        获取用户列表，给用户购票所需字符串赋值
        :param repeat_submit_token: 发送请求所需的data参数

        """
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        people_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        rsp = self.browser.post_url(people_url, data=data)
        html = loads(rsp.content)

        passengers = html['data']['normal_passengers']

        passenger_dict = {}  # 用户名字典
        i = 1  # 乘车人序号
        for passenger in passengers:
            passenger_dict[str(i)] = passenger['passenger_name']
            print(str(i) + '、' + passenger['passenger_name'])
            i += 1

        number = input("请选择乘车人序号(1,2,3)")
        passenger_num = number.split(',')

        try:
            for x in passenger_num:
                username = passenger_dict[x]

                for passenger in passengers:
                    if passenger['passenger_name'] == username:
                        # 座位类型,passenger_flag,票类型(成人/儿童),name,身份类型(身份证/军官证….),身份证,电话号码,保存状态
                        self.passenger_ticket_str += '{},{},1,{},{},{},{},N_'.format(self.seatType,
                                                                                     passenger['passenger_flag'],
                                                                                     passenger['passenger_name'],
                                                                                     passenger[
                                                                                         'passenger_id_type_code'],
                                                                                     passenger['passenger_id_no'],
                                                                                     passenger['mobile_no'],
                                                                                     )

                        # 姓名,证件类型,证件号码,人的类型
                        self.old_passenger_str += '{},{},{},{}'.format(passenger['passenger_name'],
                                                                       passenger['passenger_id_type_code'],
                                                                       passenger['passenger_id_no'],
                                                                       passenger['passenger_type'])
        except:
            print(("输入有误"))

    def check_order_info(self, repeat_submit_token):
        """
        检验订单信息
        :param repeat_submit_token: 发送请求所需的data参数
        :return:
        """
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.passenger_ticket_str,
            'oldPassengerStr': self.old_passenger_str,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        check_url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        rsp = self.browser.post_url(check_url, data)
        # print(rsp.content)
        html = loads(rsp.content)

        if html['data']['submitStatus']:
            print('系统校验订单信息成功')
            if html['data']['ifShowPassCode'] == 'Y':
                print('需要再次验证')
                return True
            if html['data']['ifShowPassCode'] == 'N':
                return False
        else:
            print('系统校验订单信息失败')
            return False

    def get_queue_count(self, repeat_submit_token, key_check_is_change, train_dict):
        """
        检验订单后，获取队列信息
        :param repeat_submit_token: 发送请求所需的data参数
        :param key_check_is_change: 发送请求所需的data参数
        :param train_dict: 火车信息字典
        :return:
        """

        data = {
            'train_date': Utility.get_train_date(train_dict['trainDate']),
            'train_no': train_dict['trainNumber'],
            'stationTrainCode': train_dict['trainName'],
            'seatType': self.seatType,
            'fromStationTelecode': train_dict['fromTelecode'],
            'toStationTelecode': train_dict['toTelecode'],
            'leftTicket': train_dict['leftTicket'],
            'purpose_codes': '00',
            'train_location': train_dict['trainLocation'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        queue_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        rsp = self.browser.post_url(queue_url, data)
        html = loads(rsp.content)
        # print(html)

        if html['status']:
            print('系统获取队列信息成功')
            self.confirm_single_for_queue(repeat_submit_token, key_check_is_change, train_dict)

        else:
            print('系统获取队列信息失败')
            return

    def confirm_single_for_queue(self, repeat_submit_token, key_check_is_change, train_dict):
        """
        下订单的最后一步请求。
        :param repeat_submit_token: 发送请求所需的data参数
        :param key_check_is_change: 发送请求所需的data参数
        :param train_dict: 火车信息字典
        """

        data = {
            'passengerTicketStr': self.passenger_ticket_str,
            'oldPassengerStr': self.old_passenger_str,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': key_check_is_change,
            'leftTicketStr': train_dict['leftTicket'],
            'train_location': train_dict['trainLocation'],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token,
        }
        confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        rsp = self.browser.post_url(confirm_url, data)
        html = loads(rsp.content)
        if html['data']['submitStatus']:
            print('已完成订票，请前往12306进行支付')
        else:
            print('订票失败,请稍后重试!')

    def select_order_details(self):
        """
        选择座位类型

        """
        print("座位码对照表：")
        print("-----------------------")
        print("|  序号 |  座位类型   |")
        print("|   M   |   一等座    |")
        print("|   O   |   二等座    |")
        print("|   1   |  硬座/无座  |")
        print("|   2   |    软座     |")
        print("|   3   |    硬卧     |")
        print("|   4   |    软卧     |")
        print("|   F   |    动卧     |")
        print("|   6   |  高级软卧   |")
        print("|   9   |   商务座    |")
        print("-----------------------")
        seat_type = input("请选择车座类型，enter键默认硬座（例如：1）:")
        if seat_type == '':
            self.seatType = "1"
        elif seat_type in self.seat_types_code:
            self.seatType = seat_type
        else:
            raise Exception("没有对应的车座类型！")

    def book_tickets(self):
        """
        订票主程序。

        """
        train_dicts, query_data = Query().get_query()
        # 保持登录
        if self.check_user():

            train_name = input("请选择车次")
            self.select_order_details()

            for train_dict in train_dicts:
                if train_dict['trainName'] == train_name:
                    print('您选择的车次为{},正在为您抢票中……'.format(Utility.red_color(train_dict['trainName'])))
                    repeat_submit_token, key_check_is_change = self.submit_order(query_data, train_dict)
                    self.get_passenger(repeat_submit_token)
                    self.check_order_info(repeat_submit_token)
                    self.get_queue_count(repeat_submit_token, key_check_is_change, train_dict)

