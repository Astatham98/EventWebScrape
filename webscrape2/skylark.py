from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Skylark Bar"

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

    if answer == 0:
        events.append("Skylarking - reggae and dancehall")
        dates.append(date)
        prices.append("NaN")
        times.append("10pm-2am")
    elif answer == 1:
        events.append("Rewind Tuesdays")
        dates.append(date)
        prices.append("NaN")
        times.append("NaN")
    elif answer == 2:
        events.append("Wild Wednesday Night Hip-hop")
        dates.append(date)
        prices.append("Free before 11, $5 after")
        times.append("NaN")
    elif answer == 4:
        events.append("Hunny Bunny Burlesque, Rotating Hip-Hop DJ's")
        dates.append(date)
        prices.append("NaN")
        times.append("8pm-close")
    elif answer == 5:
        events.append("Rotating Hip-Hop DJ's")
        dates.append(date)
        prices.append("NaN")
        times.append("10pm-close")


t = ""
try:
    df = pd.read_csv('skylark.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('skylark.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('skylark.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
