from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Caffe Frascati"

length = monthrange(2019, 1)[1]
dates = []
events = []
prices = []
times = []
fcounter = 0
scounter = 0
for i in range(1, length+1):
    dt = f'2019-01-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    year, month, day = (int(x) for x in dt.split('-'))
    answer = datetime.date(year, month, day).weekday()

    if answer == 1:
        events.append("Open mic night.")
        dates.append(date)
        prices.append("Free")
        times.append("7pm-10pm")
    if answer == 2:
        events.append("Commedia! Open mic comedy night.")
        dates.append(date)
        prices.append("Free")
        times.append("7:30pm-10pm")
    if answer == 3:
        events.append("Live Lit Writers' Open Mic! Poetry, Stories and humor.")
        dates.append(date)
        prices.append("Free")
        times.append("7pm-10pm")
    if scounter < 1 and answer == 5:
        events.append("Kavanaugh Brothers Celtic Experience!")
        dates.append(date)
        prices.append("Free")
        times.append("8pm-12am")
        scounter += 1
    if fcounter < 1 and answer == 4:
        events.append("South First Friday Art Walk and Opera Night")
        dates.append(date)
        prices.append("Free")
        times.append("8pm-10:30pm")
        fcounter += 1
    elif answer == 4 and fcounter == 1:
        fcounter += 1
    elif answer == 4 and fcounter == 2:
        events.append("Bossa Blue -- Brazilian Music Night!")
        dates.append(date)
        prices.append("Free")
        times.append("8pm-12am")
        fcounter += 1

t = ""
try:
    df = pd.read_csv('caffeefrascati.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('caffeefrascati.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('caffeefrascati.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
