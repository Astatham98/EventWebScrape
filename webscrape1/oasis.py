from selenium import webdriver
import selenium.common.exceptions as serrors
import arrow.parser as arrowperror
import arrow
import csv
import time
import requests
from bs4 import BeautifulSoup as bs
import selenium.common.exceptions as selex
import pandas as pd


def oasis():
    venue = "Oasis San Francisco"
    browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
    browser.get("https://sfoasis.com/calendar")
    time.sleep(1)
    search_a = browser.find_elements_by_tag_name('a')

    # Changes to next month
    # for x in search_a:
    #     if x.get_attribute("class") == "next clndr-next-button":
    #         x.click()
    #         break
    # time.sleep(3)

    search_a = browser.find_elements_by_tag_name('a')
    links = []
    for look in search_a:
        try:
            if look.get_attribute('class') == "cal-link button button-primary":
                link = look.get_attribute('href')
                links.append(link)
        except serrors.StaleElementReferenceException:
            pass

    events = []
    dates = []
    times = []
    prices = []
    for link in links:
        site = requests.get(link)
        soup = bs(site.content, 'lxml')

        try:
            event = soup.find(class_="summary hero-title hug").text
            events.append(event)
        except AttributeError:
            browser.get(link)
            time.sleep(0.5)
            event = browser.find_element_by_tag_name("h1")
            events.append(event.text)

        try:
            raw_date = soup.find(class_="fancy_date_with_day_name hug").text
            splitdate = raw_date.split(",")
            joined_date = splitdate[1] + splitdate[2]
            try:
                date = arrow.get(joined_date, " MMMM D YYYY").format("MM/DD/YY")
                dates.append(date)
            except arrowperror.ParserError:
                dates.append(joined_date)

            datetime = soup.find(class_="event_dates").text
            raw_time = datetime.replace(raw_date, "")
            cleaned_time = raw_time.split("\n")
            timee = cleaned_time[2] + cleaned_time[3] + cleaned_time[4]
            times.append(timee)
        except AttributeError:
            browser.get(link)
            time.sleep(0.5)
            try:
                datetime = browser.find_element_by_xpath("""/html/body/div[1]/div[4]/div[1]/div[2]/div[4]/div/div[1]/div[2]/div/div[2]/div/h3""").text
                splitdt = datetime.split(",")

                splitdate = splitdt
                joined_date = splitdate[1] + splitdate[2]
            except selex.NoSuchElementException:
                joined_date = "NaN"
            try:
                date = arrow.get(joined_date, " MMMM D YYYY").format("MM/DD/YY")
                dates.append(date)
            except arrowperror.ParserError:
                dates.append(joined_date)

            time_raw = splitdt[1]
            timee_split = time_raw.split(" PST")
            timee = timee_split[0]
            times.append(timee)

        try:
            ticket_title = soup.find(class_="ticket-title").text
            ticket_title = ticket_title.replace("\n", "")

            item_price = soup.find(class_="ticket-item-price").text

            fee_price = soup.find(class_="col-fee-number decorate").text
            fee_price = fee_price.replace("\n", "")

            price = ticket_title + " - " + item_price + fee_price
            prices.append(price)
        except AttributeError:
            prices.append("NaN")


    browser.close()

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('oasis.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('oasis.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])

oasis()