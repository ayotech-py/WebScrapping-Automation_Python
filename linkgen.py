import re
import json
from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days=1)

json_data = json.loads(open('channel_messages.json').read())

rows = []

for record in json_data:
    if yesterday.strftime("%Y"'-'"%m"'-'"%d") in record["date"]:
        try:
            messages = record["message"]
        except KeyError:
            continue
        rows.append(messages)

link_text = ''.join(str(x) for x in rows)


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


string = link_text

textfile = open("link_sheet.txt", "w")
for element in Find(string):
    if 'https://ngtodayjobs.com/' in element:
        textfile.write(element + "\n")
textfile.close()
