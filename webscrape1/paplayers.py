from selenium import webdriver
import arrow
import selenium.common.exceptions as serrors
import pandas as pd
import csv

venue = "Palo Alto Players"
url = "http://siteline.vendini.com/site/paplayers.org/buy-individual-tickets"
browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
browser.get(url)

a = browser.find_elements_by_tag_name('a')

links = []
for i in a:
    if i.get_attribute("class") == "button tickets":
        links.append(i.get_attribute('href'))

events = []
times = []
dates = []
prices = []
for link in links:
    browser.get(link)

    frames = browser.find_elements_by_tag_name('iframe')
    for frame in frames:
        if frame.get_attribute("id") == "salesFrame":
            mainframe = frame
    browser.switch_to.frame(mainframe)

    event = browser.find_element_by_xpath("""//*[@id="selectPerformance"]/div/div[1]/div/div/div[2]/div[1]/div""")

    for div in browser.find_elements_by_tag_name("div"):
        try:
            if div.get_attribute("class") == "col-12 col-md-5 vnd-wltl-font-weight-semibold":
                raw_date = div.text
                find_day = raw_date.split(" ")
                find_day = find_day[0]

                removed_date = raw_date.replace(find_day+" ", "")
                remove_extra = removed_date.split("(")
                just_date = remove_extra[0]
                just_date = just_date.rstrip()
                date = arrow.get(just_date, "MMM D, YYYY").format("MM/DD/YY")
                dates.append(date)

            if div.get_attribute("class") == "col-12 col-md-2 mt-2 mt-md-0":
                times.append(div.text)
                events.append(event.text)
            if div.get_attribute("class") == "col-12 col-md-3 text-md-center pt-3 pt-md-0":
                prices.append(div.text)
        except serrors.StaleElementReferenceException:
            pass

# t = ""
# # tries to read csv, if not creates or empty them headers are added
# try:
#     pd.read_csv('paplayers.csv')
# except FileNotFoundError:
#     t = "NaN"
# except pd.errors.EmptyDataError:
#     t = 'NaN'
# if t == 'NaN':
with open('paplayers.csv', 'w') as ttable:
    filewriter = csv.writer(ttable)
    filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
# Appends all of the elements in our lists to the csv
with open('paplayers.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(dates)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])

browser.close()