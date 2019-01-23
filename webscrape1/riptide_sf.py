from selenium import webdriver
import csv
import arrow
import pandas as pd
import time


def riptide():
    # Veneue name, price and site url for calender only
    venue = "Riptide San Francisco"
    prices = "Free!"
    url = "http://www.localendar.com/public/riptidesf?style=M4"

    # Open a chrome browser, gets the url and sleeps
    browser = webdriver.Chrome("//Users/alex/Downloads/chromedriver")
    browser.get(url)
    time.sleep(1)
    # Changes to next month
    # browser.find_element_by_xpath("""//*[@id="dayspan"]/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[4]/a""").click()
    # time.sleep(3)
    # Initializes the lists
    events = []
    times = []
    dates = []
    # Finds all the instances where it says week to bring to a list
    week_urls1 = browser.find_elements_by_class_name("wj")
    week_urls = []
    for urlz in week_urls1:
        if urlz.text != '':
            week_urls.append(urlz)
    # Finds the length of the week urls
    for i in range(len(week_urls)):
        # Refinds the weeks as it is a changing javascript element
        week_urls = browser.find_elements_by_class_name("wj")
        # Goes to the week in the range and clicks it
        w = week_urls[i]
        w.click()

        # Finds the tags of a
        popup_find = browser.find_elements_by_tag_name("a")
        # Looks through all the a's
        for p in popup_find:
            # If there is an onclick attribute then continue
            if p.get_attribute("onclick") != None:
                # Clicks on the element
                p.click()
                # waits
                time.sleep(0.5)
                # saves the current window
                main_window_handle = browser.current_window_handle
                # Searches through all the windows
                for handle in browser.window_handles:
                    # If the window is not the main window then save it and break the loop
                    if handle != main_window_handle:
                        pop_up_handle = handle
                        break

                # Switches to the popup window
                browser.switch_to.window(pop_up_handle)
                # Finds the title of the event and appends it to the events
                title = browser.find_element_by_class_name("header-theme")
                events.append(title.text)

                # Finds the datetime element
                datetime = browser.find_element_by_class_name("subheader-theme")
                # turns it to text
                datetime = datetime.text
                # splits by new lines and chooses the first element
                splitdt = datetime.split("\n")
                realdt = splitdt[0]
                # splits by spaces
                splitdt2 = realdt.split("   ")

                # finds the first element and appends it
                timee = splitdt2[0]
                times.append(timee)

                # finds the second element, changes it into desired format and appends it to the date
                raw_date = splitdt2[1]
                date = arrow.get(raw_date, "MMM D, YYYY").format("MM/DD/YY")
                dates.append(date)

                # Sleeps for half a second
                time.sleep(0.5)
                # Switches to the main window and runs through the loop again
                browser.switch_to.window(main_window_handle)
        # waits for 0.5 seconds
        # gets the original page url and waits
        browser.get(url)
        time.sleep(0.5)
        # gets the next month
        # browser.find_element_by_xpath("""//*[@id="dayspan"]/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[4]/a""").click()
        # time.sleep(3)


        print(dates)
    # closes the browser
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
    with open('riptidesf.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('riptidesf.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices])



riptide()