import selenium.webdriver as webdriver
import csv
import time

venue = "Ohlone College - G.Craig Jackson Theatre"
prices = "NaN"

broswer = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
broswer.get('https://calendar.ohlone.edu/MasterCalendar/MasterCalendar.aspx')
uncheck = broswer.find_element_by_xpath("""//*[@id="page"]/section/div[3]/div[3]/section[3]/div/div[3]/ul/li[1]/div[1]""").click()
time.sleep(0.5)
check = broswer.find_element_by_xpath("""//*[@id="page"]/section/div[3]/div[3]/section[3]/div/div[3]/ul/li[7]/div[2]""").click()
time.sleep(1)

events = []
times = []
dates = []

find_events = broswer.find_elements_by_tag_name("p")
for p in find_events:
    if p.text != "":

        events.append(p.text)

find_times = broswer.find_elements_by_tag_name("div")
for div in find_times:
    if div.get_attribute("class") == "font-weight-bold event-list-datetime-label":
        time_raw = div.text
        time_split = time_raw.split(" ")
        time = time_split[0]
        times.append(time)

    elif div.get_attribute("class") == "three column po":
        date = div.text
        dates.append(date)

broswer.close()

with open('ohlone.csv', 'w') as ttable:
    filewriter = csv.writer(ttable)
    filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
# Appends all of the elements in our lists to the csv
with open('ohlone.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices])

