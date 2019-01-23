import requests
from bs4 import BeautifulSoup as bs
import arrow
from selenium import webdriver
import csv
import pandas as pd

def templesf():
    venue = "Temple San Francisco"
    site_url = "https://templesf.com/event-calendar/"
    site = requests.get(site_url)
    soup = bs(site.content, 'lxml')
    actual_events = [x.find(class_="gcelllink") for x in soup.find_all(class_="uv-event")]
    urls = [i.get('href') for i in actual_events]

    prices = []
    dates = []
    events = []
    times = []
    for url in urls:
        site = requests.get(url)
        soup = bs(site.content, 'lxml')

        event = (soup.find('h1')).text
        events.append(event)

        raw_date = (soup.find('h2')).text
        split_dates = raw_date.split(',')
        mday = split_dates[1]
        year = split_dates[-1]
        joined_date = mday + year
        date = arrow.get(joined_date, " MMMM D YYYY").format("MM/DD/YY")
        dates.append(date)

        browser = webdriver.Chrome('//Users/alex/Downloads/chromedriver')
        browser.get(url)
        iframe = browser.find_element_by_xpath('//*[@id="eventbrite-widget-iframe-div"]/iframe')
        external_url = iframe.get_attribute("src")

        browser.get(external_url)
        datetime = browser.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div/header/div/span/span""")
        pricepoints = browser.find_elements_by_xpath("""//*[@id="root"]/div/div/div[1]/div/main/div/div[1]/div/form/div/ul/li[2]/div/div""")
        pricepoints2 = browser.find_elements_by_xpath("""//*[@id="root"]/div/div/div[1]/div/main/div/div[1]/div/form/div/ul/li/div/div""")

        raw_prices = []
        for p in pricepoints:
            raw_prices.append(p.text)

        try:
            stringprices = raw_prices[0]
            split = stringprices.split('\n')
            eb = split[0]
            rprice = split[2] + " " + split[3]
            price = eb + " " + rprice
            prices.append(price)
        except IndexError:
            raw_prices2 = []
            for p in pricepoints2:
                raw_prices2.append(p.text)
            try:
                stringprices = raw_prices2[0]
                split = stringprices.split('\n')
                eb = split[0]
                rprice = split[1] + " " + split[2]
                price = eb + " " + rprice
                prices.append(price)
            except IndexError:
                prices.append('NaN')

        datetime = datetime.text
        datetime = datetime.split("2019")

        start = datetime[1]
        start = start.split("-")
        start = start[0]
        start = start.lstrip()
        start = start.rstrip()
        try:
            end = datetime[2]
            end = end.lstrip()
        except IndexError:
            end = ""

        timee = start + " - " + end
        times.append(timee)

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('templesf.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('templesf.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])


templesf()