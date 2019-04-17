import re
from json import loads
from urllib import parse
from utility import Utility
from query_ticket import Query
from user_login import Login


class BookTicket:
    def __init__(self):
        self.browser = Login.browser

    def check_user(self):
        print('--------------checkuser----------------')
        check_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        check_data = {
            '_json_att': ''
        }
        rsp = self.browser.post_url(check_url, check_data)
        print(rsp.content)
        html = loads(rsp.content)
        print(html)

    def submit_order(self, query_data, train_dict):
        ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': parse.unquote(train_dict['secretStr']),
            'train_date': query_data['trainDate'],
            'back_train_date': '2019-04-11',
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': query_data['toStation'],
            'query_to_station_name': query_data['fromStation'],
            'undefined': ''
        }
        # print(data)
        rsp = self.browser.post_url(ticket_url, data)
        # print(rsp.content.decode('utf-8'))
        html = loads(rsp.content)
        # print(html)
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
                # print(repeat_submit_token)
                # print(key_check_is_change)
                return repeat_submit_token, key_check_is_change
            except:
                print('获取Token参数失败')

    def get_passenger(self, seatType, query_data, username, train_dict):

        # step 1: sumbit_order
        repeat_submit_token, key_check_is_change = self.submit_order(query_data, train_dict)

        # step2 : getPassengerDTOs
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        people_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        rsp = self.browser.post_url(people_url, data=data)
        passengers = rsp.json()['data']['normal_passengers']

        for passenger in passengers:
            if passenger['passenger_name'] == username:
                # step 3: Check order
                self.check_order_info(seatType, repeat_submit_token, passenger)
                # step 4:获取队列
                self.get_queue_count(seatType, repeat_submit_token, key_check_is_change, train_dict, passenger)
                return
            else:
                print('无法购票')

    def check_order_info(self, seat_type, repeat_submit_token, passenger):
        # 座位类型,passenger_flag,票类型(成人/儿童),name,身份类型(身份证/军官证….),身份证,电话号码,保存状态
        passenger_ticket_str = '{},{},1,{},{},{},{},,N'.format(seat_type, passenger['passenger_flag'],
                                                               passenger['passenger_name'],
                                                               passenger['passenger_id_type_code'],
                                                               passenger['passenger_id_no'],
                                                               passenger['mobile_no'],
                                                               )
        # 姓名,证件类型,证件号码,人的类型
        old_passenger_str = '{},{},{},{}'.format(passenger['passenger_name'], passenger['passenger_id_type_code'],
                                                 passenger['passenger_id_no'], passenger['passenger_type'])
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': passenger_ticket_str,
            'oldPassengerStr': old_passenger_str,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        check_url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        rsp = self.browser.post_url(check_url, data)
        print(rsp.content)
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

    def get_queue_count(self, seatType, repeatSubmitToken, keyCheckIsChange, trainDict, passenger):

        # data = {
        #     '_json_att' : '',
        #     'fromStationTelecode' : trainDict['fromTelecode'],
        #     'leftTicket': trainDict['leftTicket'],
        #     'purpose_codes': '00',
        #     'REPEAT_SUBMIT_TOKEN' : repeatSubmitToken,
        #     'seatType': seatType,
        #     'stationTrainCode': trainDict['trainName'],
        #     'toStationTelecode': trainDict['toTelecode'],
        #     'train_date': Utility.getTrainDate(trainDict['trainDate']),
        #     'train_location': trainDict['trainLocation'],
        #     'train_no': trainDict['trainNumber'],
        # }

        data = {
            'train_date': Utility.get_train_date(trainDict['trainDate']),
            'train_no': trainDict['trainNumber'],
            'stationTrainCode': trainDict['trainName'],
            'seatType': seatType,
            'fromStationTelecode': 'MDQ',
            'toStationTelecode': 'VIQ',
            'leftTicket': trainDict['leftTicket'],
            'purpose_codes': '00',
            'train_location': trainDict['trainLocation'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeatSubmitToken
        }
        queue_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        rsp = self.browser.post_url(queue_url, data)
        html = loads(rsp.content)
        print(html)

        if html['status']:
            print('系统获取队列信息成功')
            self.confirm_single_for_queue(seatType, repeatSubmitToken, keyCheckIsChange, passenger, trainDict)

        else:
            print('系统获取队列信息失败')
            return

    def confirm_single_for_queue(self, seatType, repeatSubmitToken, keyCheckIsChange, passenger, trainDict):

        # 座位类型,passenger_flag,票类型(成人/儿童),name,身份类型(身份证/军官证….),身份证,电话号码,保存状态
        passenger_ticket_str = '{},{},1,{},{},{},{},N'.format(seatType, passenger['passenger_flag'],
                                                              passenger['passenger_name'],
                                                              passenger['passenger_id_type_code'],
                                                              passenger['passenger_id_no'],
                                                              passenger['mobile_no'],
                                                              )
        # 姓名,证件类型,证件号码,人的类型
        old_passenger_str = '{},{},{},{}'.format(passenger['passenger_name'], passenger['passenger_id_type_code'],
                                                 passenger['passenger_id_no'], passenger['passenger_type'])

        data = {
            'passengerTicketStr': passenger_ticket_str,
            'oldPassengerStr': old_passenger_str,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': keyCheckIsChange,
            'leftTicketStr': trainDict['leftTicket'],
            'train_location': trainDict['trainLocation'],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeatSubmitToken,
        }
        confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        rsp = self.browser.post_url(confirm_url, data)
        html = loads(rsp.content)
        print(rsp.content)
        print(html)
        if html['data']['submitStatus'] == 'True':
            print('已完成订票，请前往12306进行支付')
        else:
            print('订票失败,请稍后重试!')

    def book_tickets(self, username):
        # 保持登录
        self.check_user()
        train_dicts, query_data = Query().get_query()
        # 这个地方座位类型也是不是固定的，如硬卧有时候是3，有时是A3
        seat_type = input('请输入车票类型,1无座,F动卧,M一等座,O二等座,1硬座,3硬卧,4软卧,6高级软卧,9商务座:\n')
        i = 0
        for train_dict in train_dicts:
            if train_dict[seat_type] == Utility.green_color('有') or train_dict[seat_type].isdigit():
                print('为您选择的车次为{},正在为您抢票中……'.format(Utility.red_color(train_dict['trainName'])))
                self.get_passenger(seat_type, query_data, username, train_dict)
                return
            else:
                i += 1
                if i >= len(train_dicts):  # 遍历所有车次后都未能查到座位，则打印错误信息
                    print(Utility.red_color('Error:系统未能查询到{}座位类型存有余票'.format(seat_type)))
                continue
