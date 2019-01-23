from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "The patio"

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

    if answer != 5 and answer != 6:
        events.append("Happy hour")
        dates.append(date)
        prices.append("Free")
        times.append("4pm-7pm")
    if answer == 1 or answer == 2:
        events.append("karaoke Night")
        dates.append(date)
        prices.append("NaN")
        times.append("10pm-12am")
    if answer == 2:
        events.append("Trivia night")
        dates.append(date)
        prices.append("NaN")
        times.append("7pm-9pm")

t = ""
try:
    df = pd.read_csv('thepatio.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('thepatio.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('thepatio.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
