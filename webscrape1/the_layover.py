import bs4 as bs
import requests
import arrow
import csv
import pandas as pd


def thelayover():
    venue = "The Layover"
    prices = "NaN"
    for i in range(1, 3):
        site_url = "https://www.oaklandlayover.com/calendar?calendar_page="+str(i)
        site = requests.get(site_url)
        soup = bs.BeautifulSoup(site.content, 'lxml')
        urls = soup.find_all(class_="event_details no-pjax")

        year = "2019"

        external_urls = []
        for url in urls:
            url = url.get('href')
            modified_url = site_url.replace("calendar?calendar_page="+str(i), "")
            url = modified_url + url
            external_urls.append(url)

        events = []
        times = []
        dates = []
        for url in external_urls:
            site = requests.get(url)
            soup = bs.BeautifulSoup(site.content, 'lxml')
            try:
                event = (soup.find(class_="event-info event-title heading-tertiary")).text
                event = event.replace(")", "")
                event = event.split("(")
                final_event = event[0]
                events.append(final_event)

                time = event[-1]
                times.append(time)


                date = (soup.find(class_="date")).text
                date = date.split(",")
                date = date[-1]
                date = date.lstrip()
                date = date + " " + year
                try:
                    date = arrow.get(date, "MMMM D YYYY").format("MM/DD/YY")
                    dates.append(date)
                except arrow.parser.ParserError:
                    dates.append("NaN")
            except AttributeError:
                continue

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('thelayover.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('thelayover.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(dates)):
            filewriter.writerow([venue, events[i], dates[i], times[i], prices])


thelayover()
