import requests
from bs4 import BeautifulSoup
import time
import smtplib

class Currency:
    DOLLAR_RUB = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=%D0%BA%D1%83%D1%80%D1%81&aqs=chrome.0.0i131i433i512j69i57j0i433i512j0i131i433i512j0i512j0i131i433i512j0i512j0i131i433i512l3.1730j1j15&sourceid=chrome&ie=UTF-8'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}

    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            print("Курс сильно вырос, может пора что-то делать?")
            self.send_mail()
        elif currency <= self.current_converted_price + self.difference:
            print("Курс сильно упал, может пора что-то делать?")
            self.send_mail()
        print("Сейчас курс: 1 доллар = " + str(currency))
        time.sleep(3)
        self.check_currency()

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('sashaichenko7@gmail.com', 'jwifydvobnzvsljo')

        subject = 'Курс валют'
        body = 'Курс доллара изменился!'
        message = f'subject: {subject}\n\n{body}'

        server.sendmail(
            'sashaichenko1998@icloud.com',
            'sashaichenko7@gmail.com',
            message
        )
        server.quit()

currency = Currency()
currency.check_currency()
