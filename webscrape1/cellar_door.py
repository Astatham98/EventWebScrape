import bs4 as bs
import requests
import arrow
import csv
import pandas as pd


def cellardoor():
    venue = "Cellar Door"

    site = requests.get("http://ourcellardoor.com/calendar/")
    soup = bs.BeautifulSoup(site.content, 'lxml')
    daynum = soup.find_all(class_="numbday")
    numtime = soup.find_all(class_="numbtime")
    description = soup.find_all(class_="numbdesc")
    myear = soup.find(class_="caltitle")

    day = []
    for n in daynum:
        day.append(n.text)
    times = []
    for t in numtime:
        times.append(t.text)
    event = []
    for e in description:
        event.append(e.text)

    prices = []
    for i in event:
        if "$" in i:
          i = i.split(' ')
          price = i[0]
          prices.append(price)
        else:
          prices.append('NaN')

    dates = []
    for i in range(len(day)):
        d1 = myear.text + " " + day[i]
        date = arrow.get(d1, "MMMM YYYY D").format("MM/DD/YY")
        dates.append(date)

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #   df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #   t = "NaN"
    # except pd.errors.EmptyDataError:
    #   t = 'NaN'
    # if t == 'NaN':
    with open('cellardoor.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('cellardoor.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(dates)):
            filewriter.writerow([venue, event[i], dates[i], times[i], prices[i]])

cellardoor()