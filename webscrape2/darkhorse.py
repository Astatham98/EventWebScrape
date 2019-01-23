from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Dark Horse Lounge"

length = monthrange(2019, 1)[1]
dates = []
events = []
prices = []
times = []
fcounter = 0
for i in range(1, length+1):
    dt = f'2019-01-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    year, month, day = (int(x) for x in dt.split('-'))
    answer = datetime.date(year, month, day).weekday()

    if answer == 1:
        events.append("Karaoke with big Mike")
        dates.append(date)
        prices.append("Free")
        times.append("9pm")
    if answer == 3:
        events.append("Ladies Night with DJ Bullo")
        dates.append(date)
        prices.append("Free")
        times.append("9pm")
    if answer == 4 and fcounter != 2:
        fcounter += 1
        events.append("Old School with DJ Branden")
        dates.append(date)
        prices.append("Free")
        times.append("9pm")
    elif answer == 4 and fcounter == 2:
        fcounter += 1
        events.append("Jam Night")
        dates.append(date)
        prices.append("Free")
        times.append("9pm")
    if answer == 5:
        events.append("Live Music TBA")
        dates.append(date)
        prices.append("Free")
        times.append("NaN")
    if answer == 6:
        events.append("Blues and Booze with Rob Briesch")
        dates.append(date)
        prices.append("Free")
        times.append("4pm")



t = ""
try:
    df = pd.read_csv('darkhorse.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('darkhorse.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('darkhorse.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
