import json
import time
import tkinter as tk

import requests
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

HOST = "https://www.ticketswap.com"
EVENT_URL = 'https://www.ticketswap.com/event/audio-obscura-x-adriatique-w-ame-mano-le-tough-sofia-kourtesis-marino-canal-ade/regular-tickets/61b854eb-9ca1-43e5-8944-a610aaa8a549/2314759'
EVENT_URL = "https://www.ticketswap.com/event/verknipt-ade-house-special-ade-saturday/01fa1e6d-273e-4792-8ba2-a56686f0509b"

class TicketSwapMe:
    def __init__(self):
        # options = Options()
        # options.add_argument('--headless')
        # self.driver = wd.Firefox(options=options)
        self.driver = wd.Chrome(executable_path='/Users/markpopcsev/PycharmProjects/TicketSwap/Ticket-SwapMe/chromedriver')

        self.login()
        self.has_tickets = False

    def login(self):
        """Login to Ticketswap using Facebook credentials"""
        username = ''
        password = ''

        self.driver.get(HOST)
        time.sleep(1)
        consent_button = self.driver.find_element(By.XPATH, "/html/body/ticketswap-portal[4]/ul/li/div/span[2]/div/div/button[2]")
        consent_button.click()
        time.sleep(1)
        login_button = self.driver.find_element(By.XPATH,'//*[@id="__next"]/div[5]/div/nav/ul/li[4]/button')
        login_button.click()
        time.sleep(1)
        facebook_button = self.driver.find_element(By.XPATH, "/html/body/ticketswap-portal[3]/div/div/div/div/div/div/div/button[2]")
        facebook_button.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(1)
        consent_fb = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]")
        consent_fb.click()
        time.sleep(1)
        user_input = self.driver.find_element(By.ID, 'email')
        pass_input = self.driver.find_element(By.ID, 'pass')

        user_input.send_keys(username)
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        self.driver.get(EVENT_URL)
        self.cookies = self.__handle_cookies(self.driver.get_cookies())

        # self.driver.quit()

    def __handle_cookies(self, cookie_list):
        cookies = {}
        for cookie in cookie_list:
            cookies[cookie['name']] = cookie['value']
        return cookies

    def start(self):
        time.sleep(1)
        self.driver.get(EVENT_URL)
        time.sleep(2)
        while True:
            self.driver.get_cookies()
            time.sleep(3)

            letter = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[3]/div/div[1]/span').text
            if (int(letter) > 0):
                print(str(letter)+" are available")
                try:
                    ### TODO check selectors from here
                    self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/ul/li/a/div').click()
                    self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/a[1]/div').click()
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div[3]/button').click()
                except :
                    print("Except error raised: NoSuchElementException")
                    self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/form/button').click()
                try:
                    self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div/a[1]/div').click()
                    time.sleep(3)
                    self.driver.find_element(By.CSS_SELECTOR, 'div.css-uirvwh:nth-child(2) > ul:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1)').click()
                    #
                    time.sleep(3)
                    self.driver.find_element(By.CSS_SELECTOR, '.css-1aros5x').click()
                except NoSuchElementException:
                    print("Except error raised: NoSuchElementException")

                break
            else:
                print("No tickets are available keep trying")
            self.driver.refresh()



        # while self.has_tickets is False:
        #     print('Checking for tickets')
        #     self.get_ticket(event_url)
        #     # if data is not False:
        #     #     self.reserve_ticket(data)
        #     #     self.has_tickets = True
        #     #     webbrowser.open(HOST + '/cart', new=2)
        #     time.sleep(0.5)

    def get_ticket(self, event_url):
        """ Get Cheapest ticket """
        # Getting the cheapest ticket
        self.driver.get(event_url)

        # response = requests.get(event_url, cookies=self.cookies)
        # html = response.content.decode("utf-8")
        # parsed_html = BeautifulSoup(html, "html.parser")
        # not_exist = parsed_html.body.find('div', attrs={'class': "no-tickets"})
        # if not_exist is not None:
        #     print("no tickets")
        #     return False
        # url_object = parsed_html.body.findAll('div', attrs={'class': 'listings-item--title'})
        # if url_object is None:
        #     print("no offers")
        #     return False
        # for item in url_object:
        #     item = item.findAll('a')[0]
        #     attributes = item.attrs
        #     ticket_link = attributes['href']
        #     data = self.explode_ticket(ticket_link)
        #     if data is not False:
        #         return data
        #     print('Possible that you have the wrong event url')
        # return False

    def explode_ticket(self, ticket_link):
        """ Gets tokens from ticket page """
        # Get tokens that you need to have to reserve the ticket and getting the get in cart link
        response = requests.get(HOST + ticket_link, cookies=self.cookies)
        parsed_html = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        token_object = parsed_html.body.find('input', attrs={"name": "reserve[_token]"})
        if token_object is None:
            print("Failed to get token")
            return False
        token_attrs = token_object.attrs
        reserve_token_object = parsed_html.body.find('input', attrs={"name": "reserve[_token]"})

        if reserve_token_object is None:
            return False
        reserve_token_attrs = reserve_token_object.attrs
        # check type of ticket
        add_data = {}
        seats = parsed_html.body.find('input', attrs={'name': 'tickets[]'})
        if seats is not None:
            add_data['tickets[]'] = seats.attrs['value']
        else:
            items = parsed_html.body.find('select', attrs={'name': 'amount'})
            count = len(items.findChildren())
            add_data['amount'] = count
        token = token_attrs['value']
        reserve_token = reserve_token_attrs['value']
        ticket_link_reserve = parsed_html.body.find('form', attrs={"id": "listing-reserve-form"}).attrs
        ticket_reserve_link = ticket_link_reserve['data-endpoint']
        return {"token": token,
                "reserve_token": reserve_token,
                "ticket_link": ticket_reserve_link,
                "more_data": add_data}

    def reserve_ticket(self, content):
        """ Reserve ticket """
        token = content['token']
        reserve_token = content['reserve_token']
        form_data = {"token": token, "reserve[_token]": reserve_token, **content['more_data']}
        # add ticket in cart
        ticket = requests.post(HOST + content['ticket_link'], data=form_data, cookies=self.cookies)
        content = json.loads(ticket.content.decode("utf-8"))
        print('Successfully added ticket to your account')
        return bool(content['success'])


if __name__ == "__main__":
    ROOT = tk.Tk()
    ROOT.withdraw()
    t = TicketSwapMe()
    t.start()