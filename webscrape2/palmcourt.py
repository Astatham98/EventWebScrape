from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Orchestria Palm Court Restaurant"

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

    if answer == 31:
        dates.append(date)
        times.append("5:45pm-8:30pm")
        events.append("TBD")
        prices.append("NaN")
    elif answer == 4 or answer == 5:
        dates.append(date)
        times.append("5:45pm-8:30pm")
        events.append("Cover songs - Christmas music")
        prices.append("NaN")


t = ""
try:
    df = pd.read_csv('palmcourt.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('palmcourt.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('palmcourt.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
