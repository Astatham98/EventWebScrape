from calendar import monthrange
import datetime
import arrow
import csv
import pandas as pd

venue = "O'Flaherty's Irish Pub"

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

    if answer == 1:
        events.append("Live Irish music")
        dates.append(date)
        prices.append("NaN")
        times.append("6:30pm-10:30pm")
    elif answer == 3:
        events.append("O'Flaherty's Trivia Night")
        dates.append(date)
        prices.append("NaN")
        times.append("8pm")
    elif answer == 0:
        events.append("Karaoke Night")
        dates.append(date)
        prices.append("NaN")
        times.append("9pm-12am")
    elif answer == 6:
        events.append("Karaoke Night")
        dates.append(date)
        prices.append("NaN")
        times.append("9pm-12am")


t = ""
try:
    df = pd.read_csv('oflahertys.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('oflahertys.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('oflahertys.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])
