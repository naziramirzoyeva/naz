import datetime

date_str1 = input("first date (YYYY-MM-DD HH:MM:SS): ")
date_str2 = input("second date (YYYY-MM-DD HH:MM:SS): ")


date1 = datetime.datetime.strptime(date_str1, "%Y-%m-%d %H:%M:%S")
date2 = datetime.datetime.strptime(date_str2, "%Y-%m-%d %H:%M:%S")


difference = date2 - date1

seconds = difference.total_seconds()

print("Difference ", seconds)