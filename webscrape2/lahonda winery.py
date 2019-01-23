import csv

venue = "Lahonda Winery"
date = "11/15/18"
price = "$10"
event = "Public wine tasting"
time = "12-4pm"

with open('timetable2.csv', 'a') as ttable:
    filewriter = csv.writer(ttable)
    filewriter.writerow([venue, event, date, time, price])
