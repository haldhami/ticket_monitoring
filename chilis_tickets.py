import requests
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('PO_API_KEY')
USER_KEY = os.getenv('PO_USER_KEY')

url = 'https://www.twickets.live/event/1599769182730199040'
browser = webdriver.Chrome()
browser.get(url)

prev_cheapest_tickets = []

try:
    while True:
        
        time.sleep(60)
        browser.refresh()
        time.sleep(2.5)
        page = browser.page_source
        
        soup = BeautifulSoup(page, 'html.parser')

        tickets = soup.find_all('twickets-g2-listing')

        cheapest_tickets = []
        max_price = 90
        
        for ticket in tickets:
            if 'Standing' not in ticket.text:
                continue
            price = re.findall('£\d{1,2}.\d{1,2}', ticket.text)[0]
            number_of_tickets = re.findall('\d tickets|1 ticket', ticket.text)[0]
            float_price = float(price[1:])
            if float_price > max_price:
                continue
            if len(cheapest_tickets) != 3:
                cheapest_tickets.append((number_of_tickets, price))
            else:
                break
            
        if cheapest_tickets == prev_cheapest_tickets:
            continue
            
        message = ''
        for cheapest_ticket in cheapest_tickets:
            message += f'\n{cheapest_ticket[0]} @ {cheapest_ticket[1]} each'

        message = message.strip()
        message += '\nhttps://www.twickets.live/event/1599769182730199040'

        url = 'https://api.pushover.net/1/messages.json'

        payload = {'token': API_KEY, 'user': USER_KEY, 'message': message}

        r = requests.post(url, data=payload)
        prev_cheapest_tickets = cheapest_tickets
                
except KeyboardInterrupt:
    print('Program has stopped.')