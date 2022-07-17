from bs4 import BeautifulSoup
import requests
from telethon.sync import TelegramClient, events
import configparser
import time

job_list1 = []
textfile = open("link_sheet.txt", "r")

with open('link_sheet.txt','r') as f:
    for line in f:
        strip_lines = line.strip()
        listli = strip_lines
        job_list1.append(listli)

filter_links = []
message_list = []

print('Generating Messages, Please Wait...')

for job_links in job_list1:
    html_text = requests.get(job_links).text
    soup = BeautifulSoup(html_text, 'lxml')
    job = soup.find('div', class_='content-third')

    filter_list = []

    job_list = ['p', 'ul']
    try:
        for tags in job.find_all(job_list):
            filter_list.append(tags.text.replace("\xa0", ' '))

        class Place:
            def start(self):
                for text in filter_list:
                    if 'Job Title:' in text:
                        return filter_list.index(text)

            def end(self):
                for end_text in filter_list:
                    if ('Apply here' in end_text or 'Method of Application' in end_text or 'How to Apply' in end_text):
                        return filter_list.index(end_text)

        place = Place()
        start = place.start()
        end = place.end()
        #print(f"[{start},{end}]")

        text = filter_list[start:end+1]

        def send_message(post):
            config = configparser.ConfigParser()
            config.read("config.ini")

            # Setting configuration values
            api_id = config['Telegram']['api_id']
            api_hash = config['Telegram']['api_hash']

            api_hash = str(api_hash)

            phone = config['Telegram']['phone']
            username = config['Telegram']['username']

            # Create the client and connect
            with TelegramClient('name', api_id, api_hash) as client:
                client.send_message('PythonJson', post)
                time.sleep(1)
        messages = []
        if ('Click here to apply online' in text[-1] or 'Apply here' in text[-1] and '2022' in text[start:end]):
            messages.append(job_links)
            send_message(job_links)

        else:
            check_post = '\n'.join(text)
            if not len(check_post) >= 4096:
                messages.append(check_post)
                send_message(check_post)
    except AttributeError:
        continue