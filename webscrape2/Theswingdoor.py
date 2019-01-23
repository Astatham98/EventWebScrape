from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "The Swing Door"

length = monthrange(2019, 1)[1]
dates = []
events = []
prices = []
times = []
for i in range(1, length+1):
    dt = f'2019-01-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    year, month, day = (int(x) for x in dt.split('-'))
    answer = datetime.date(year, month, day).weekday()

    if answer == 2 or answer == 3 or answer == 4 or answer == 5:
        events.append("Karaoke")
        dates.append(date)
        prices.append("Free")
        times.append("9:30pm-1:30am")
    if answer == 4 or answer == 5:
        events.append("Dueling Piano show")
        dates.append(date)
        prices.append("Free")
        times.append("9pm-1am")
    if answer == 6:
        events.append("Trivia night")
        dates.append(date)
        prices.append("Free")
        times.append("7pm-9pm")

t = ""
try:
    df = pd.read_csv('theswingdoor.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('theswingdoor.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('theswingdoor.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
