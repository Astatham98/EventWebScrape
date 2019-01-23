from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "Del Mar"

length = monthrange(2018, 12)[1]
dates = []
events = []
prices = []
times = []
for i in range(1, length+1):
    dt = f'2018-12-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    year, month, day = (int(x) for x in dt.split('-'))
    answer = datetime.date(year, month, day).weekday()

    if answer == 2:
        events.append("What do you meme")
        dates.append(date)
        prices.append("Free")
        times.append("5pm-close")
    elif answer == 3:
        events.append("The best of the 90's-2000's - DJ @ 9")
        dates.append(date)
        prices.append("Free")
        times.append("5pm-close")
    elif answer == 4:
        events.append("Sunset series - DJ methpd")
        dates.append(date)
        prices.append("Free before 11, $5 after")
        times.append("5pm-2am")
    elif date == "12/08/18":
        events.append("Santacon at the beach")
        dates.append(date)
        prices.append("NaN")
        times.append("3pm-close")
    elif answer == 5:
        events.append("Sunset series")
        dates.append(date)
        prices.append("Free before 11, $5 after")
        times.append("2pm-2am")
    elif answer == 6:
        events.append("Slushie Sundays")
        dates.append(date)
        prices.append("$6")
        times.append("2pm-10pm")


t = ""
try:
    df = pd.read_csv('timetable2.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('timetable2.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('timetable2.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
