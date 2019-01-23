from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "San Rafael Joe's"

length = monthrange(2018, 12)[1]
dates = []
events = []
prices = []
times = []
scounter = 0
for i in range(1, length+1):
    dt = f'2018-12-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    year, month, day = (int(x) for x in dt.split('-'))
    answer = datetime.date(year, month, day).weekday()

    if answer == 4:
        events.append("Joanne Smith - musician")
        dates.append(date)
        prices.append("NaN")
        times.append("NaN")
    if answer == 6:
        if scounter < 3:
            scounter += 1
            events.append("Steve Albini - musician")
            dates.append(date)
            prices.append("NaN")
            times.append("NaN")
        else:
            events.append("Swing Society Trio")
            dates.append(date)
            prices.append("NaN")
            times.append("NaN")
    if answer == 5:
        events.append("Philip Percy Williams Trio & Donna Spitz and Benny Watson")
        dates.append(date)
        prices.append("NaN")
        times.append("NaN")

t = ""
try:
    df = pd.read_csv('srjpes.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('srjpes.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('srjpes.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
