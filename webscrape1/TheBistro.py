import bs4 as bs
import requests
import arrow
import datetime as dt
import calendar
import csv
import re
import pandas as pd
from arrow import parser


def the_bistro():
    # List of months of the year
    moy = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Importing the website
    site = requests.get('http://the-bistro.com/')
    soup = bs.BeautifulSoup(site.content, 'lxml')
    content = soup.find_all(class_="CalBoxEmpty")
    month = soup.find_all('td', class_='BodyTxt20pxblue')
    venue = "The Bistro"
    # Looks for the current month
    month_list = []
    for i in month:
        k = i.text.strip()
        month_list.append(k)
    month = month_list[0]
    # Gives a number to the month (e.g. Nov = 11)
    for x in range(0, len(moy)):
        if moy[x] in month:
            mnum = x + 1
    # Finds the current year
    for x in moy:
        if x in month:
            year = month.replace(" ", ",")
            year = year.split(',')
            year = year[1]

    # strips into plain text
    days = []
    for i in content:
        k = i.text.strip()
        days.append(k)
    days2 = []
    # Replaces spaces
    for i in days:
        j = i.replace('\n\n', ',')
        j = j.replace('\n', ",",)
        days2.append(j)

    # adds the current month if needed as well as adding the events to a list
    dates = []
    event = []
    try:
        for i in days2:
            # If in the month before it adds just the year and appends it to dates
            if moy[mnum - 2] in i:
                spl = i.split(',')
                dates.append(spl[0] + " " + year)
                # deletes the date then appends the events
                del spl[0]
                event.append(spl)
            # If month is current month adds the month and year and appends it to dates
            elif (moy[mnum - 2] not in i) & (i != ""):
                spl = i.split(',')
                dates.append(moy[mnum-1] + " " + spl[0] + " " + year)
                # deletes the date then appends the events
                del spl[0]
                event.append(spl)
    # Checks for index errors
    except IndexError:
        # If in January
        if moy == 1:
            for i in days2:
                if moy[12] in i:
                    spl = i.split(',')
                    dates.append(spl[0] + " " + year)
                    # deletes the date then appends the events
                    del spl[0]
                    event.append(spl)
                elif (moy[12] not in i) & (i != ""):
                    spl = i.split(',')
                    dates.append(moy[mnum-1] + " " + spl[0] + " " + year)
                    # deletes the date then appends the events
                    del spl[0]
                    event.append(spl)
        # If in febuary
        elif moy == 2:
            for i in days2:
                if moy[1] in i:
                    spl = i.split(',')
                    dates.append(spl[0] + " " + year)
                    # deletes the date then appends the events
                    del spl[0]
                    event.append(spl)
                elif (moy[1] not in i) & (i != ""):
                    spl = i.split(',')
                    dates.append(moy[mnum-1] + " " + spl[0] + " " + year)
                    # deletes the date then appends the events
                    del spl[0]
                    event.append(spl)
    # Cleans up the events
    event2 = []
    for i in event:
        if len(i) > 1:
            temp = []
            for u in i:
                k = u.lstrip()
                temp.append(k)
            event2.append(temp)
        else:
            for u in i:
                k = u.lstrip()
            event2.append(k)

    # Gives date for the day of the year
    number_date = []
    test_date = []
    for i in dates:
        try:
            number_date.append(arrow.get(i, 'MMM D YYYY').format('MM/DD/YY'))
            test_date.append(arrow.get(i, 'MMM D YYYY').format('YYYY,MM,DD'))
        except parser.ParserError:
            number_date.append(arrow.get(i, "MMM. D YYYY").format("MM/DD/YY"))
            test_date.append(arrow.get(i, "MMM. D YYYY").format('YYYY,MM,DD'))
    #Finds the weekday depending on the date
    weekdays = []
    for j in test_date:
        k = j.split(',')
        kl = []
        for i in k:
            kl.append(int(i))
        # Converts date to day
        dday = dt.datetime(kl[0], kl[1], kl[2])
        pp = calendar.day_name[dday.weekday()]
        weekdays.append(pp)
    # Sets the opening times to NaN's
    open_time = []
    for i in range(0,34):
        open_time.append('NaN')
    # Finds the days where there is an event with a time
    good_nums = []
    for i in range(len(event2)):
        for x in event2[i]:
            am = re.compile(("([A-Z]|[a-z]|[-]|[ ])*([1-9]|1[0-2])am([A-Z]|[a-z]|[-]|[ ])*"))
            pm = re.compile(("([A-Z]|[a-z]|[-]|[ ])*([1-9]|1[0-2])pm([A-Z]|[a-z]|[-]|[ ])*"))
            if am.match(x):
                good_nums.append(i)
            if pm.match(x):
                good_nums.append(i)
    # replaces NaN's with times when there is an event on
    for i in good_nums:
        open_time[i] = event2[i]
    # Replaces NaN with weekday and then weekday with normal opening hours
    for i in range(0, len(open_time)):
        if open_time[i] == 'NaN':
            open_time[i] = weekdays[i]
        if open_time[i] == 'Monday':
            open_time[i] = '8pm'
        elif open_time[i] == 'Tuesday':
            open_time[i] = '8pm'
        elif open_time[i] == 'Wednesday':
            open_time[i] = '8pm'
        elif open_time[i] == 'Thursday':
            open_time[i] = '8pm'
        elif open_time[i] == 'Friday':
            open_time[i] = '9pm'
        elif open_time[i] == 'Saturday':
            open_time[i] = '9pm'
        elif open_time[i] == 'Sunday':
            open_time[i] = '4pm'
    # Opens a csv and adds a header
    with open('thebistro.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(['Venue', 'Event', 'Date', 'Time', 'price'])
    # Opens the csv and checks if the even is the same as the top row, if not then it adds more artists
    # try:
    #     df = pd.read_csv('timetable.csv')
    #     t = df['Event']
    #     t = t[0]
    # except IndexError:
    #     t = "NaN"
    # if t != event2[0]:
    with open('thebistro.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(open_time)):
            filewriter.writerow([venue, event2[i], number_date[i], open_time[i], "NaN"])


the_bistro()

