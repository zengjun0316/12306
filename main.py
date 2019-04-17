from book_ticket_trainNum import BookTicket
from user_login import Login
from user_verify import Captcha
from init_cookie import Cookie

if __name__ == '__main__':
    browser = Login.browser
    browser.cookie_jar = Cookie().cookies()
    Captcha().sys_verify(browser)
    Login().sys_login()
    BookTicket().book_tickets()
