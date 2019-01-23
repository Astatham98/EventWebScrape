from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Loft Bar and Bistro"

length = monthrange(2019, 1)[1]
dates = []
events = []
prices = []
times = []
scounter = 0
for i in range(1, length+1):
    dt = f'2019-01-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    year, month, day = (int(x) for x in dt.split('-'))
    answer = datetime.date(year, month, day).weekday()

    if answer == 4:
        events.append("DJ")
        dates.append(date)
        prices.append("Free")
        times.append("11am-1:30am next day")
    if answer == 5:
        events.append("DJ")
        dates.append(date)
        prices.append("Free")
        times.append("11am-1:30am next day")



t = ""
try:
    df = pd.read_csv('loftbarandbistro.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('loftbarandbistro.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('loftbarandbistro.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
