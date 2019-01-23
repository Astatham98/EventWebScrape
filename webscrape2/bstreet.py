from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "B Street and vine"

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

    if answer < i:
        if answer == 2:
            events.append("The Neil Kelly Duo")
            dates.append(date)
            prices.append("Free")
            times.append("7pm-10pm")
        if answer == 3:
            events.append("The Larry St Lezin Trio")
            dates.append(date)
            prices.append("Free")
            times.append("7pm-10pm")
        if answer == 4:
            events.append("Dave Badilla")
            dates.append(date)
            prices.append("Free")
            times.append("7pm-10pm")
        if answer == 5:
            events.append("Jazz duo")
            dates.append(date)
            prices.append("Free")
            times.append("7pm-10pm")
t = ""
try:
    df = pd.read_csv('bstreetandvin.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('bstreetandvin.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('bstreetandvin.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
