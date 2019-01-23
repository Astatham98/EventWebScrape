import csv
import bs4
import requests
import arrow
import pandas as pd


def hotelutah():
    # Venue name
    venue = "Hotel Utah"
    # main calender side
    site =("https://www.hotelutah.com/calendar")
    site = requests.get(site)
    soup = bs4.BeautifulSoup(site.content, "lxml")
    # finds all urls on the webpage that take you to an event
    urls = soup.find_all(class_="url")

    # Initializing holding lists
    event_raw = []
    raw_date = []
    time_raw = []
    price = []
    urlss = []
    # Deletes link duplicates
    for i in urls:
        if i.get('href') not in urlss:
             urlss.append(i.get('href'))

    # For the first 90 results do
    # (It is very slow to do all of them as it opens every webpage)
    for url in urlss[:90]:
        # turn to readable format
        site = requests.get("http://www.hotelutah.com"+url)
        soup = bs4.BeautifulSoup(site.content, "lxml")
        # Finds the acts playing
        event_raw.append(soup.find(class_="headliners").text)
        # finds the date
        raw_date.append(soup.find(class_="dates").text)
        # finds the start time
        time_raw.append(soup.find(class_="start dtstart").text)
        # Finds the ticket prices and cleans them up
        prices = soup.find(class_="ticket-price").text
        prices = prices.replace("\t", "")
        prices = prices.replace("\n", "")
        prices = prices.replace("       ", " ")
        price.append(prices)

    # List of days of the week so we can strip them from dates
    dow = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday']

    date = []
    # Finds dates
    for dates in raw_date:
        # replaces any ,
        dates = dates.replace(",", "")
        for i in dow:
            # if it finds a day of the week it will strip it
            if i in dates:
                # Tries to convert date into American format
                try:
                    dates = dates.replace(i+" ", "")
                    dates = arrow.get(dates, "MMMM D YYYY").format("MM/D/YY")
                    date.append(dates)
                # If the date is in a different format try that
                except arrow.parser.ParserError:
                    dates = arrow.get(dates, "MMMM  D YYYY").format("MM/DD/YY")
                    date.append(dates)

    # # holder for t
    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('hotelutah.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('hotelutah.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(date)):
            filewriter.writerow([venue, event_raw[i], date[i], time_raw[i], price[i]])


hotelutah()
