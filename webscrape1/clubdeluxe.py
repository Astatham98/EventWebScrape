from selenium import webdriver
import time
import csv
import arrow
import requests
import bs4 as bs
import pandas as pd


def clubdeluxe():
    venue = "Club Deluxe"
    prices = "NaN"
    browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
    browser.get('https://www.clubdeluxe.co/calendar')
    time.sleep(1)

    link = browser.find_elements_by_class_name("item-link")
    href_links = [x.get_attribute('href') for x in link]

    browser.close()

    events = []
    times = []
    dates = []
    for link in href_links:
        site = requests.get(link)
        soup = bs.BeautifulSoup(site.content, 'lxml')

        try:
            event = soup.find(class_="eventitem-title")
            events.append(event.text)
        except AttributeError:
            events.append("NaN")
        try:
            time_end = (soup.find(class_="event-time-12hr-end")).text
            time_start = (soup.find(class_="event-time-12hr-start")).text
            timee = time_start + " - " + time_end
            times.append(timee)
        except AttributeError:
            times.append("NaN")

        try:
            date_raw = (soup.find(class_="event-date")).text
            split_date = date_raw.split(",")
            date_joined = split_date[1] + split_date[2]
            date = arrow.get(date_joined, " MMMM D YYYY").format("MM/DD/YY")
            dates.append(date)
        except AttributeError:
            dates.append("NaN")

        time.sleep(1)

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('clubdeluxe.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('clubdeluxe.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices])




clubdeluxe()

