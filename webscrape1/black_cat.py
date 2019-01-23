import bs4 as bs
import requests
import arrow
import csv


def blackcat():
    venue = "Black cat"

    pages = []
    for i in ["%.2d" % i for i in range(1, 32)]:
        # calender date for december
        site = requests.get("https://blackcatsf.com/calendar/2019-01-"+i+"/")
        soup = bs.BeautifulSoup(site.content, 'lxml')
        pages.append(soup)

    price2 = []
    event = []
    timess = []
    dates = []
    for page in pages:
        price = page.find_all(class_="ticket-cost")
        temp = []
        for i in price:
            i = i.text
            if i not in temp:
                temp.append(i)
        try:
            if temp[-1] != " ":
                price2.append(temp)
            else:
                price2.append("NaN")
        except IndexError:
            continue

        act = page.find_all(class_="url")
        tmp = []
        for i in act:
            i = i.text
            if i not in tmp:
                tmp.append(i)
        try:
            if tmp[0] != " ":
                event.append(tmp)
        except IndexError:
            continue

        start_times = page.find_all(class_="tribe-events-day-time-slot-heading")
        end_times = page.find_all(class_="tribe-event-time")
        start = []
        end = []

        for i in start_times:
            tmp = []
            if i not in start:
                tmp.append(i.text)
        try:
            if tmp[0] != " ":
                start.append(tmp)
        except IndexError:
            continue

        for i in end_times:
            tmp = []
            if i not in end:
                tmp.append(i.text)
        try:
            if tmp[0] != " ":
                end.append(tmp)
        except IndexError:
            continue

        times = []
        for day in range(0, len(end)):
            stmp = start[day]
            etmp = end[day]
            join = stmp[0] + " - " + etmp[0]
            times.append(join)
        timess.append(times)


        year = page.find(class_="tribe-events-title-bar")
        year = year.text
        year = year.split(",")
        year = year[-1]
        year.replace(" ", "")

        dates_raw = page.find(class_="tribe-event-date-start")
        try:
            dates_raw = dates_raw.text
            dates_raw = dates_raw.split("@")
            dates_raw = dates_raw[0].split(",")
            dates_raw = dates_raw[1:2]
            dates_raw = dates_raw[0]
            dates_raw = dates_raw + year
            try:
                date = arrow.get(dates_raw, "MMMM D  YYYY").format("MM/DD/YY")
                dates.append(date)
            except arrow.parser.ParserError:
                date = arrow.get(dates_raw, "MMMM D YYYY").format("MM/DD/YY")
                dates.append(date)
        except AttributeError:
            continue

    # # holder for t
    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('blackcat.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('blackcat.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(len(event)):
            filewriter.writerow([venue, event[i], dates[i], timess[i], price2[i]])


blackcat()