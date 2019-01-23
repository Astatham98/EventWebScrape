from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Audium San Francisco"

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

    if answer == 4 or (answer == 5 and i != 8):
        events.append("Audium")
        dates.append(date)
        prices.append("$20")
        times.append("8:15pm")
    if answer == 3:
        events.append("Audium")
        dates.append(date)
        prices.append("$20 or $15 for students")
        times.append("8:15pm")

t = ""
try:
    df = pd.read_csv('audiumsf.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('audiumsf.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('audiumsf.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
