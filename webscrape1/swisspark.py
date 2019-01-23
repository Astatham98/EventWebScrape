from bs4 import BeautifulSoup as bs
import requests
import arrow
import pandas as pd
import csv


def swisspark(link):
    # Venue name and prices
    venue = "Swiss Park"
    prices = "NaN"
    # uses input link as url and shows the plain url
    url = link
    plain_url = "http://swissparknewark.com/"

    # parsers the site and finds classes of the names
    site = requests.get(url)
    soup = bs(site.content, 'lxml')
    urls = soup.find_all(class_="text-left")

    # finds the month and year
    myear = (soup.find(class_="full_calendar_month_name text_regular text-uppercase")).text
    # splits it and formats the year to desired format
    split_myear = myear.split(" ")
    year_long = split_myear[1]
    year = arrow.get(year_long, "YYYY").format("/YY")

    # finds the link for next month calender and adds it to the plain link
    next_month = (soup.find('a', class_="em-calnav full-link em-calnav-next color_red")).get('href')
    full_next_link = plain_url + next_month

    # initializes lists
    events = []
    times = []
    dates = []
    for url in urls:
        # finds the child
        url = url.find('a')
        # tries to get a href of the event, if not continues
        try:
            url = url.get('href')
        except AttributeError:
            continue
        # parses the site to BeautifulSoup
        site = requests.get(url)
        soup = bs(site.content, 'lxml')

        # finds the event, turns it to text and appends it
        event = (soup.find(class_="text_bold color_red")).text
        events.append(event)

        # finds the raw date
        raw_date = (soup.find(class_="text_bold color_dark")).text
        # splits it at the ,
        split_date = raw_date.split(",")
        # selects only the date, not the day name and removes spaces
        only_date = split_date[1].lstrip()
        # adds the date to the year and appends it to dates
        date = only_date + year
        dates.append(date)

        # converts the time to text and appends it
        time = (soup.find(class_="text_regular color_light")).text
        times.append(time)

    # # initializes t
    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
        # If any errors occurred the headers are added to the csv
    with open('swisspark.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('swisspark.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        # loops through the list and adds them to the csv
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices])
    # if the amount of events in the month is more than 0 the swisspark method is called again
    # it uses the link of the next full month
    # if len(events) > 0:
    #     swisspark(full_next_link)


# starts the loop with the default link
def start_loop():
    swisspark("http://swissparknewark.com/event/")


# calls start_loop
start_loop()
