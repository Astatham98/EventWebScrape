from selenium import webdriver
import arrow
import csv
import pandas as pd
from time import sleep


def luckyhorseshoe():
    venue = "The Lucky Horseshoe"
    prices = "NaN"
    url = "https://www.theluckyhorseshoebar.com/calendar"
    browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
    browser.get(url)
    sleep(2)

    browser.switch_to.frame(0)
    spans = browser.find_elements_by_tag_name("span")

    events = []
    dates = []
    times = []
    for span in spans:
        if span.get_attribute('class') == "event-title-text ng-binding":
            events.append(span.text)
            span.click()
            sleep(0.25)
            raw_date = browser.find_elements_by_xpath("""//*[@class="popup-when material-icon ng-binding"]""")
            full_dates = [x.text for x in raw_date]
            for d in full_dates:
                d = d.split(',')
                mday = d[1].lstrip()
                year = d[2]
                ddate = mday + year
                date = arrow.get(ddate, "MMMM D YYYY").format("MM/DD/YY")
                dates.append(date)

            raw_time = browser.find_elements_by_xpath("""//*[@class="popup-time material-icon ng-binding ng-scope"]""")
            for time in raw_time:
                times.append(time.text)
            browser.find_element_by_xpath("""//*[@class="popup-close"]""").click()
            sleep(0.25)

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('lhorseshoe.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('lhorseshoe.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices])
    # closes the browser to prevent clutter
    browser.close()


luckyhorseshoe()
