from selenium import webdriver
from time import sleep
import selenium.common.exceptions as serrors
import pandas as pd
import csv
import arrow

# Venue and price
venue = "The Alley Oakland"
prices = "NaN"
# Calendar url
url = "https://www.thealleyoakland.com/"
# loads up a chrome window and parses the url and then waits for one second
browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
browser.get(url)
sleep(3)

# finds the iframe for the main calendar and the facebook popup window
mainframe = browser.find_elements_by_tag_name('iframe')[1]
#         popframe = browser.find_elements_by_tag_name('iframe')[-2]
#
#         # switches to the popup window and closes it
#         browser.switch_to.frame(popframe)
#         browser.find_element_by_id("close").click()
#         sleep(1)
# switches to default content then to the mainframe
browser.switch_to.default_content()
browser.switch_to.frame(mainframe)

# buttons = browser.find_elements_by_tag_name("button")
# for button in buttons:
#     if button.get_attribute("class") == "arrow icon icon-arrow-right unselectable":
#         button.click()
#         print("Success")

# finds all the span elements
sleep(1)
to_click = browser.find_elements_by_tag_name('span')

# initializes lsits
events = []
dates = []
times = []
# searches through all spans
for i in to_click:
    # if the event class is the same as the class window then click it
    if "event-title-text ng-binding" == i.get_attribute("class"):
        i.click()
        # searches for all divs after clicked as a new popup window would appear
        divs = browser.find_elements_by_tag_name("div")
        # goes through the divs
        for div in divs:
            # fixes a common timing error
            try:
                # if the start of the popup window is in the class continue
                if "popup ng-scope animation-start" in div.get_attribute("class"):
                    # turn into text and split
                    elements = div.text
                    splitelements = elements.split("\n")
                    # only uses the useful parts
                    useful = splitelements[1:]

                    # appends the event
                    event = useful[0]
                    events.append(event)

                    # finds the raw date and turns it into wanted format
                    date_raw = useful[1]
                    date_split = date_raw.split(",")
                    mday = date_split[1]
                    year = date_split[2]
                    mdyear = mday + year
                    date = arrow.get(mdyear, " MMMM D YYYY").format("MM/DD/YY")
                    dates.append(date)

                    # appends the time
                    time = useful[2]
                    times.append(time)

                    # closes the popup window
                    button = div.find_element_by_tag_name("button").click()

            except serrors.StaleElementReferenceException:
                pass


# t = ""
# # tries to read csv, if not creates or empty them headers are added
# try:
#     pd.read_csv('timetable.csv')
# except FileNotFoundError:
#     t = "NaN"
# except pd.errors.EmptyDataError:
#     t = 'NaN'
# if t == 'NaN':
with open('thealley.csv', 'w') as ttable:
    filewriter = csv.writer(ttable)
    filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
# Appends all of the elements in our lists to the csv
with open('thealley.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices])

browser.close()