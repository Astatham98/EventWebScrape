import requests
import csv
import bs4 as bs
import pandas as pd
import arrow


def poorhb():
    # Venue name and price holder if price not found
    venue = "The Poorhouse Bistro"
    price = "NaN"
    # url and changing to useable format
    url = requests.get("https://poorhousebistro.com/calendar/")
    soup = bs.BeautifulSoup(url.content, 'lxml')
    # Finds event titles
    event_name = soup.find_all(class_="evcal_desc2 evcal_event_title")
    # finds dates, time
    date = soup.find_all(class_="date")
    time = soup.find_all(class_="time")
    # Finds month and year and then cleans it up
    monyear = soup.find(class_="evo_month_title")
    monyear = monyear.text
    monyear = monyear.replace(",", "")

    # Turns month events into readable texts
    month_events = []
    for i in event_name:
        month_events.append(i.text)
    event_date = []
    # Creates a date by appending month and year to dates the nay number
    for i in date:
        k = monyear + " " + i.text
        dt = arrow.get(k, "MMMM YYYY D").format("MM/D/YY")
        event_date.append(dt)
    # turns event times into readable text
    et = []
    for i in time:
        et.append(i.text)
    # creates a open and close by joining 2 elements together
    event_times = [x+" - "+y for x,y in zip(et[0::2], et[1::2])]

    # # holder for t
    # t = ""
    # # trues to open a timetable, if the file is not found or
    # #  the file is empty the heading are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('poorhousebistro.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('poorhousebistro.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(month_events)):
            filewriter.writerow([venue, month_events[i], event_date[i], event_times[i], price])


poorhb()