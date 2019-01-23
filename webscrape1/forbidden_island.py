from selenium import webdriver
import arrow
import pandas as pd
import csv
import time


def fisland():
    # Venue name
    venue = "Forbidden Island"
    # No listed prices so NaN
    prices = "NaN"
    # Site url
    url = "http://www.forbiddenislandalameda.com/events-calendar/"
    # Opens a chrome browser and gets the url
    browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
    browser.get(url)
    # waits 3 seconds for the webpage to fully load
    time.sleep(3)
    # finds all elements with the tag 'a'
    urls_find = browser.find_elements_by_tag_name('a')

    # initializes lists
    events = []
    links = []
    # goes through all the tags with a
    for urls in urls_find:
        # looks for the classes
        classname = urls.get_attribute('class')
        # if the classes have this string in them then continue
        if "fc-event fc-event-hori fc-event-start fc-event-end" in classname:
            # finds the links
            link = urls.get_attribute('href')
            links.append(link)

            # splits the events by new line
            event_raw = urls.text.split('\n')
            # only appends the first line
            event = event_raw[0]
            events.append(event)

    # initializes more lists
    times = []
    dates = []
    # searches through links
    for link in links:
        # takes to the link webpage
        browser.get(link)
        # finds the time element and turns it to text
        timee = browser.find_element_by_class_name("ee-event-datetimes-li-timerange").text
        times.append(timee)

        # finds the raw date
        raw_date = browser.find_elements_by_class_name("ee-event-datetimes-li-daterange")
        # turns the last date in the list to text
        wanted_date = raw_date[-1].text
        # replaces , with " for formatting ease
        repdate = wanted_date.replace(",", "")
        # formats into wanted date format and appends
        date = arrow.get(repdate, "MMMM D YYYY").format("MM/DD/YY")
        dates.append(date)
        # browser always waits for 1 second before going onto next link or an error occurs
        browser.implicitly_wait(1)

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('fisland.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('fisland.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('fisland.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices])
    # closes the browser to prevent clutter
    browser.close()


# calls the method
fisland()
