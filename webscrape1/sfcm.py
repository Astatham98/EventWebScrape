from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
import requests

def sfcm():
    venue = "SFCM"
    site_url = "https://sfcm.edu/performance-calendar"
    stripped_url = site_url.replace("/performance-calendar", "")
    site = requests.get(site_url)
    soup = bs(site.content, 'lxml')

    dayevents = soup.find_all(class_="mar-b-double unmarked-list bordered-list")

    events = []
    dates = []
    times = []
    prices = []
    for i in dayevents:
        i = i.find_all(class_="flag -align-top--small link-dark")
        for b in i:
            event_urls = b.get('href')
            full_url = stripped_url + event_urls

            site = requests.get(full_url)
            soup = bs(site.content, 'lxml')

            event_title = (soup.find(class_="font-omega color-white line-solid")).text
            event = event_title.lstrip()
            event = event.rstrip()
            events.append(event)

            full_date = (soup.find(class_="first")).text
            date = full_date.split(", ")
            date = date[1]
            dates.append(date)

            time = (soup.find(class_="last")).text
            times.append(time)

            boxes = soup.find_all(class_="column small-6 medium-6 large-4 mar-y-one font-alpha line-text")
            tickets = boxes[1].text
            no_tickets = tickets.replace("Tickets", "")
            no_tickets = no_tickets.replace("\n", "")
            price = no_tickets.split(',')
            price = price[0].replace(" ","")
            prices.append(price)

    t = ""
    # tries to read csv, if not creates or empty them headers are added
    try:
        df = pd.read_csv('timetable.csv')
    except FileNotFoundError:
        t = "NaN"
    except pd.errors.EmptyDataError:
        t = 'NaN'
    if t == 'NaN':
        with open('timetable.csv', 'w') as ttable:
            filewriter = csv.writer(ttable)
            filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('timetable.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])


sfcm()
