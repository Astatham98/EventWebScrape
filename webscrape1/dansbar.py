from bs4 import BeautifulSoup as bs
import requests
import csv
import arrow
import pandas as pd
from selenium import webdriver


# calls the method dansbar with a link parameter
def dansbar(link):
    # sets up window of chrome ready for late ron
    browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")

    # venue name
    venue = "Dan's bar"
    # site url being parsed into lxml format
    url = link
    site = requests.get(url)
    soup = bs(site.content, 'lxml')

    # finds all the urls in the table
    urls = [x.get('href') for x in soup.find_all(class_="url")]
    # finds all the events names and puts them as text
    events = [x.text for x in soup.find_all(class_="url")]

    # finds all the month year and splits them to find the year
    myear = (soup.find(class_="tribe-events-page-title")).text
    splitmyear = myear.split(" ")
    year = splitmyear[-1]

    # finds the link for next month calender
    nextm_link = soup.find(rel="next").get('href')

    # initializes the needed lists
    dates = []
    times = []
    prices = []
    # searches through the urls
    for url in urls:
        # parses to lxml format
        site = requests.get(url)
        soup = bs(site.content, 'lxml')

        # Searches for the date and times on the webpages
        datetime = (soup.find(class_="tribe-event-date-start")).text
        # replaces common date attribute that causes an error
        datetime = datetime.replace(", 2018", "")
        # Splits the datetime
        splitdt = datetime.split("@")

        # adds the date to year and changes it into wanted format
        raw_date = splitdt[0] + year
        print(raw_date)
        date = arrow.get(raw_date, "MMMM D YYYY").format("MM/DD/YY")
        dates.append(date)

        # finds the time and removes spaces
        time = splitdt[1].lstrip()
        times.append(time)

        # tries to find a ticket link, if not appends the price as NaN
        try:
            # Searches for href
            ticket_link = soup.find(class_="tribe-events-single-event-description tribe-events-content").find('a').get('href')
            # Opens a browser page with the found link and looks for the price
            # This didn't work with soup as it needed to fully load javascript
            browser.get(ticket_link)
            price = browser.find_element_by_id("price-range").text
            prices.append(price)
            # closes the browswer
        except AttributeError:
            prices.append("NaN")

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('dansbar.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('dansbar.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])

    # if the length of events in more than 1(there is 1 artist who has the same time every month for 2019)
    # then the next month is put through the loop
    # if len(events) > 1:
    # #     dansbar(nextm_link)
    # # browser.close()

# starts the dansbar method with the current months calender
def startloop():
    dansbar("http://dansbar.com/events/")


startloop()
