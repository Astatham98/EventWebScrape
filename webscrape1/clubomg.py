import requests
import csv
import bs4 as bs
from calendar import monthrange as mr
import pandas as pd
import arrow

# Grabs the url for the selected month and parses it using html
urls = ['http://clubomgsf.com/calendar/month/2019/01/']
for url in urls:
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.content, 'html.parser')
    # Searches for all table rows
    events = soup.find_all('tr')
    # Current venue
    venue = "Club OMG"

    # finds the month and year using the url
    sdate = url.strip('http://clubomgsf.com/calendar/month/')
    # finds the amount of days in the given month
    sdate2 = sdate.split("/")
    mrange = mr(int(sdate2[0]), int(sdate2[1]))[1]

    # Starts to strip events, strips \t and \n first
    event_list = []
    for event in events:
        k = event.text.strip()
        k = k.replace("\t", "")
        k = k.replace("\n", "")
        event_list.append(k)

    # Removes the first table row as its days of the week and gets rid of commonwhitespaces
    another_list2 = []
    for i in event_list[1:]:
        other_events = i
        other_events = other_events.replace('                                                      ', ',')
        other_events = other_events.replace('                                                    ', ',')
        other_events = other_events.replace('   ', ',')
        other_events = other_events.replace('•', '')
        other_events = other_events.replace('                                                      ', ",")
        other_events = other_events.split(',')
        # Concatenates the table rows together
        another_list = []
        another_list = another_list + other_events
        # Parses through the variables and removes any whitespace to the left
        for x in another_list:
            k = x.lstrip()
            another_list2.append(k)

    # Finds the index of the first of the month as even when hidden old events are still embedded in the html
    for i in another_list2:
        try:
            if int(i) == 1:
                start = another_list2.index(i)
                break
        except ValueError:
            continue
    # Resets to the first of the month
    another_list2 = another_list2[start:]
    # Looks for the date of the last of the month
    for i in another_list2:
        try:
            if int(i) == mrange:
                end = another_list2.index(i)

                break
        except ValueError:
            continue
    # rests the main list to end of the month
    another_list2 = another_list2[:end+4]

    # Finds where numbers (days) occurs and then parses them into a list
    number_breaks = []
    for i in another_list2:
        try:
            for j in range(1, mrange+1):
                if int(i) == j:
                    number_breaks.append(another_list2.index(i))
        # If a string is tried to turn into an int then the loop just continues
        except ValueError:
            continue

    # Creates a nested list of the different days and their events, times, etc.
    final_list = []
    # Number breaks being the index of the overall list where a new day occurs
    for index in number_breaks:
        if index != number_breaks[-1]:
            # finds the index of the next number in the list
            next_num = number_breaks.index(index) + 1
            next_num = number_breaks[next_num]
            # Appends the list from current index to next index
            final_list.append(another_list2[index:next_num])
        # The last day goes to the end
        else:
            final_list.append(another_list2[index:])

    # Appending numbers into lists
    num_list = []
    event_list = []
    time_list = []
    price_list = []
    for i in final_list:
        # Appends the num list with numbers of the month
        num_list.append(i[0])
        # If there is data other than the day of the month then parse it into lists
        if len(i) > 1:
            event_list.append(i[1])
            time_list.append(i[2])
            price_list.append(i[3])
        # If no other data replace it with an arbitrary value
        elif len(i) == 1:
            event_list.append('NaN')
            time_list.append('NaN')
            price_list.append('NaN')

    # For finding the date using the num list
    dates = []
    for i in num_list:
        # Replaces the / from the web url with a space
        k = sdate.replace("/", " ")
        # Adds a space and the day number
        k = k + " " + i
        # Reformats the date to american date and parses it to the dates list
        dates.append(arrow.get(k, "YYYY MM D").format("MM/DD/YY"))

    # # Opens a csv and adds a header
    # t = ""
    # try:
    #     pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # if t == 'NaN':
    with open('timetable.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Opens the csv and appends the data points
    with open('timetable.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(event_list)):
            filewriter.writerow([venue, event_list[i], dates[i], time_list[i], price_list[i]])

