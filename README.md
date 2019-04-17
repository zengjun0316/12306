### 12306自动抢票系统第一版
***
各文件说明

* analog_browser.py 建立模拟浏览器，用于进行cookie存储，为发送请求做准备

* book_ticket.py  暂时没用
 
* book_ticket_trainNum.py 关于选择车次的信息以及座位信息
 
* captcha.jpeg 下载下来登录需要的验证码图片
 
* color.py 查询余票时渲染余票信息
 
* init_cookie.py 模拟浏览器第一次访问拿到必须要的cookie值，为后面的访问做铺垫
 
* main.py  主函数测试
 
* query_ticket.py 查询火车的余票信息
 
* station_code.py 获取车站电报码
 
* station_code.txt 下载下来的车站电报码
 
* user_login.py 12306的用户登录,以及登录之后的两次验证
 
* user_verify.py 验证码的验证
 
* utility.py 需要用到的一些相关参数