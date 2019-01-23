from bs4 import BeautifulSoup as bs
import arrow
import requests
import csv
import pandas as pd


def angelica():
    month = input("Please enter the number of the month in the form '1':  ")
    for l in range(1, 13):
        if month == str(l):
            mnum = month
            break
        elif (l == 12) & (str(month) != l):
            print("Please enter a valid option")
            angelica()

    year = input("Please enter a year in the form '18'")
    for yr in range(18, 100):
        if year == str(yr):
            year_name = arrow.get(year, 'YY').format('YYYY')
            break
        elif (yr == 99) & (str(yr) != year):
            print("Please enter a valid input")
            angelica()

    site_url = "http://angelicaswm.tunestub.com/calendar.cfm?m="+mnum+"&y="+year_name
    venue = "Angelicas"

    site = requests.get(site_url)
    soup = bs(site.content, 'lxml')
    ticket_link = [x.get('href') for x in soup.find_all('a', class_="btn btn-sm btn-primary get-tickets")]
    details0 = soup.find_all(class_="day-wrapper")
    myear = (soup.find(class_="month")).text
    details = [x.text for x in details0]
    details = [x.replace("\n", " ") for x in details]

    prices = []
    events = []
    for link in ticket_link:
        soup = bs((requests.get(link)).content, 'lxml')

        minp = (soup.find(class_="minTixPrice")).text
        try:
            maxp = (soup.find(class_="maxTixPrice")).text
        except AttributeError:
            maxp = ""
        if maxp != "":
            price = minp + " - " + maxp
        else:
            price = minp
        prices.append(price)

        event = (soup.find(id="title-wrapper-inner")).text
        event = event.lstrip()
        event = event.rstrip()
        event = event.split("\n")
        event = event[0]
        events.append(event)

    bad_button = []
    for detail in details0:
        button = detail.find_all(class_="button")
        if len(button) > 1:
            bad_button.append(details0.index(detail))

    daynum = []
    times = []
    for deet in details:
        if len(deet) > 10:
            if bad_button[0] == details.index(deet):
                multi = deet.split("Get Tickets")
                multi = multi[:2]

                num = multi[0].split("        ")
                num = num[0]
                for i in range(2):
                    daynum.append(num + " " + myear)

                time = [x.split("                                  ") for x in multi]
                time = [z[1].rstrip() for z in time]
                [times.append(t) for t in time]

            else:
                num = deet.split("        ")
                num = num[0]

                time = deet.split("                                  ")
                time = time[1]
                time = time.split("                              ")
                time = time[0]

                daynum.append(num + " " + myear)
                times.append(time)

    dates = []
    for date in daynum:
        dates.append(arrow.get(date, "D MMMM YYYY").format("MM/DD/YY"))

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('angelicas.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':

    pri
    with open('angelicas.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('angelicas.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)-1):
            filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])


angelica()
