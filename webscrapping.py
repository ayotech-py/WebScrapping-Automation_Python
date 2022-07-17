from bs4 import BeautifulSoup
import requests

job_list1 = []
textfile = open("link_sheet.txt", "r")

with open('link_sheet.txt','r') as f:
    for line in f:
        strip_lines = line.strip()
        listli = strip_lines
        m = job_list1.append(listli)

filter_links = []
message_list = []

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
                    filter_links.append(job_links)
                else:
                    message = filter_list[start:end + 1]
                    message_list.append(message)

textfile = open("filter_sheet.txt", "w")
for element in filter_links:
    textfile.write(element + "\n")
textfile.close()

textfile = open("messages.txt", "w")
for element in message_list:
    textfile.write("%s\n" % element)
textfile.close()

print('Message sucessfully saved')
