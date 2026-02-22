import datetime

x = datetime.datetime.now()
new_date = x - datetime.timedelta(days=5)
print( new_date.date())