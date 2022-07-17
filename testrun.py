import self as self
from bs4 import BeautifulSoup
import requests
from telethon.sync import TelegramClient, events
import configparser
import re
import json
import time

self.send_header('Content-Type', 'blabla')

self.end_headers()

job_list1 = []
textfile = open("link_sheet.txt", "r")

with open('link_sheet.txt','r') as f:
    for line in f:
        strip_lines = line.strip()
        listli = strip_lines
        m = job_list1.append(listli)

filter_links = []
message_list = []
print(job_list1)
print('Generating Messages, Please Wait...')

for job_links in job_list1:
    html_text = requests.get(job_links).text
    soup = BeautifulSoup(html_text, 'lxml')
    job = soup.find('div', class_='content-third')

    filter_list = []

    job_list = ['p', 'ul']
    for tags in job.find_all(job_list):
        filter_list.append(tags.text.replace("\xa0", ' '))

    for text in filter_list:
        if 'Job Title:' in text:
            start = filter_list.index(text)

        ending = ['Method of Application', 'How to Apply']

        for end in ending:
            if end in text:
                end = filter_list.index(text)

                filter_con = filter_list[end]

                if 'Click here to apply online' in filter_con:
                    json_data = json.loads(open('channel_messages.json').read())

                    rows = []
                    filter = []

                    for record in json_data:
                        try:
                            messages = record['message']
                        except KeyError:
                            continue
                        rows.append(messages)

                    # remove all tags from the elements in row list and add them to filter list
                    for tag_text in rows:
                        filter.append(tag_text.rstrip().replace('\n', ' '))
                    for filtered in filter:
                        try:
                            link = re.search("(?P<url>https?://[^\s]+)", filtered).group("url")
                        except:
                            link = re.search("(?P<url>https?://[^\s]+)", filtered)
                            continue
                        line_1 = job_links[1:-20]
                        if line_1 in link:
                            post1 = filtered
                            if not len(post1) >= 4096:
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
                                    client.send_message('PythonJson', post1)
                                    time.sleep(1)
                else:
                    message = filter_list[start:end + 1]
                    post = '\n'.join(message)
                    if not len(post) >= 4096:
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
print('done')

