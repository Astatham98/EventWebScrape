from bs4 import BeautifulSoup as bs
import requests
import csv
import arrow
from datetime import datetime
import pandas as pd


def mainstbrew():
    month = input("Please enter the number of the month in the form '1':  ")
    for l in range(1, 13):
        if month == str(l):
            mnum = month
            mnum = mnum.zfill(2)
            break
        elif (l == 12) & (str(month) != l):
            print("Please enter a valid option")
            if __name__ == '__main__':
                mainstbrew()

    year = input("Please enter a year in the form '18'")
    for yr in range(18, 100):
        if year == str(yr):
            year_name = arrow.get(year, 'YY').format('YYYY')
            break
        elif (yr == 99) & (str(yr) != year):
            print("Please enter a valid input")
            mainstbrew()

    venue = "Main St. Brewery"
    plain_url = "http://www.mainstbrewery.com"
    # url with the current month
    url = "http://www.mainstbrewery.com/index.php/music-events/month.calendar/"+year_name+"/"+mnum+"/06/"
    prices = "NaN"
    # prases the website url to lxml
    site = requests.get(url)
    soup = bs(site.content, 'lxml')
    # finds all the links for pages in the calender
    urls = [x.get('href') for x in soup.find_all(class_="cal_titlelink")]
    # adds the plain url to the partial url to make a full url
    full_urls = [plain_url + x for x in urls]

    # initializes lists
    events = []
    times = []
    dates = []
    # goes through all the full urls
    for url in full_urls:
        # parses websites through lxml
        site = requests.get(url)
        soup = bs(site.content, 'lxml')
        # searches for h2 and uses the second one
        all_h2 = soup.find_all('h2')
        event = all_h2[1].text
        # appends to events
        events.append(event)

        # finds the datetimes
        datetimes = (soup.find(class_="ev_detail repeat")).text
        # splits the datetimes
        splitdt = datetimes.split(",")
        # finds the time adn replaces spaces
        time = splitdt[-1].lstrip()
        # replaces common html attribibute for - and replaces a text -
        time = time.replace("\xa0-\xa0", "-")
        # appends time
        times.append(time)

        # finds the raw date, removes spaces and adds the year
        raw_date = splitdt[1].lstrip() + " " + str(year_name)
        # formats to wanted type and appends it to the dates list
        date = arrow.get(raw_date, "MMMM DD YYYY").format("MM/DD/YY")
        dates.append(date)

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('mainstbrew.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('mainstbrew.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices])


# calls mainstbrew method
mainstbrew()
