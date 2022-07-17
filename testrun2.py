from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 1)
print("Yesterday was: ", yesterday)

print(yesterday.strftime("%Y"'-'"%m"'-'"%d"))