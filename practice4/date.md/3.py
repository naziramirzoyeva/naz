import datetime


now = datetime.datetime.now()
print(now)


without_microseconds = now.replace(microsecond=0)
print( without_microseconds)