import requests
from bs4 import BeautifulSoup as bs
import arrow
import csv
import pandas as pd
from time import sleep

def forager():
    venue = "Forager"
    prices = "NaN"

    month = input("Please enter the number of the month in the form '1':  ")
    for l in range(1, 13):
        if month == str(l):
            month_name = arrow.get(month, "M").format("MMMMM")
            month_name = month_name.replace(month, "")
            break
        elif (l == 12) & (str(month) != l):
            print("Please enter a valid option")
            forager()

    year = input("Please enter a year in the form '18'")
    for yr in range(18, 100):
        if year == str(yr):
            year_name = arrow.get(year, 'YY').format('YYYY')
            break
        elif (yr == 99) & (str(yr) != year):
            print("Please enter a valid input")
            forager()



    site_url = "https://www.sjforager.com/new-events/?view=calendar&month=" + month_name + "-" + year_name
    site = requests.get(site_url)
    soup = bs(site.content, 'html.parser')
    events = [x.text for x in soup.find_all('h1')]
    links = soup.find_all('h1')

    base_link = site_url.replace("/new-events/?view=calendar&month=" + month_name + "-" + year_name, "")

    dates = []
    times = []
    for i in links:
        sleep(1)
        a = str(i.find('a'))
        stripped = a.replace('<a href="', '')
        stripped = stripped.split('"')
        stripped = stripped[0]

        full_link = base_link + stripped
        sleep(1)
        site = requests.get(full_link)
        item_info = bs(site.content, 'lxml')

        try:
            event_date = (item_info.find(class_="event-date")).text
            event_date = event_date.split(',')
            year = event_date[-1]
            mday = event_date[1]
            date = mday.lstrip() + year
            dates.append(arrow.get(date, "MMMM D YYYY").format("MM/DD/YY"))
        except AttributeError:
            dates.append('NaN')
        try:
            start_time = (item_info.find(class_="event-time-12hr-start")).text
            end_time = (item_info.find(class_="event-time-12hr-end")).text
            times.append(start_time + " - " + end_time)
        except AttributeError:
            times.append('NaN')


    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #   df = pd.read_csv('forager.csv')
    # except FileNotFoundError:
    #   t = "NaN"
    # except pd.errors.EmptyDataError:
    #   t = 'NaN'
    # if t == 'NaN':
    with open('forager.csv', 'w') as ttable:
      filewriter = csv.writer(ttable)
      filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('forager.csv', 'a') as ttable:
      filewriter = csv.writer(ttable)
      for i in range(0, len(dates)):
          filewriter.writerow([venue, events[i], dates[i], times[i], prices])


forager()


