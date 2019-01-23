import csv
import arrow
from selenium import webdriver
import selenium.common.exceptions as serrors
import pandas as pd
import time
from calendar import monthrange as mr


year = time.strftime("%Y")
month = time.strftime("%m")
mrange = mr(int(year), int(month))[1]
venue = "Make out room"

# for current month
url = ("http://www.calendarwiz.com/calendars/calendar.php?crd=makeoutroom#")
urldec = "http://www.calendarwiz.com/calendars/calendar.php?crd=makeoutroom&op=cal&month=01&year=2019"
browser = webdriver.Chrome('/Users/alex/Development/chromedriver')
site = browser.get(urldec)
time.sleep(2)
click = browser.find_elements_by_class_name("cw-e-a")


dt = []
event = []
used_handles = []
for i in click:
    main_window = browser.current_window_handle
    i.click()
    for handle in browser.window_handles:
        if (handle != main_window) & (handle not in used_handles):
            click_window = handle
            used_handles.append(handle)
            break
    browser.switch_to.window(click_window)
    datetime = browser.find_element_by_id("event_date")
    event_details = browser.find_element_by_id("titletag")
    dt.append(datetime.text)
    event.append(event_details.text)
    try:
        time.sleep(0.5)
        browser.switch_to.window(main_window)
    except serrors.StaleElementReferenceException:
        pass

events = []
price = []
for eve in event:
    eve = eve.split("~")
    evef = eve[0]
    events.append(evef)
    try:
        prices = eve[-2]
        if "$" in prices:
            price.append(prices)
        elif "FREE!" in prices:
            price.append(prices)
        else:
            price.append("NaN")
    except IndexError:
        price.append("NaN")

time = []
dates = []
for date in dt:
    date1 = date.split(",")
    date = date1[1]
    date = date + " " + year
    adates = arrow.get(date, "MMM D YYYY").format("MM/DD/YY")
    dates.append(adates)

    t = date1[-1]
    tt = t.replace(year + " ", "")
    time.append(tt)

# try:
#     df = pd.read_csv('timetable.csv')
# except FileNotFoundError:
#     t = "NaN"
# except pd.errors.EmptyDataError:
#     t = 'NaN'
# if t == 'NaN':
with open('makeoutroom.csv', 'w') as ttable:
    filewriter = csv.writer(ttable)
    filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
with open('makeoutroom.csv', 'a') as ttable:
    filewriter = csv.writer(ttable)
    for i in range(0, len(events)):
        filewriter.writerow([venue, events[i], dates[i], time[i], price[i]])

browser.close()





