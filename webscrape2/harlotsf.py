from bs4 import BeautifulSoup as bs
import requests
import arrow
from calendar import monthrange
from datetime import datetime
import datetime as datet
import csv
import pandas as pd

venue = "Harlot San Francisco"

site = requests.get("http://www.harlotsf.com/category/events")
soup1 = bs(site.content, 'lxml')
tickets = soup1.find_all(class_="tickets")
events1 = soup1.find_all(class_="events-desc")

prices = []
events = []
dates = []
times = []
other_links = []
olinkcounter = 0
# for i in tickets:
#     links = i.find('a')['href']
#
#     if "eventbrite" in links:
#
#         site = requests.get(links)
#         soup = bs(site.content, 'lxml')
#         try:
#             ticket_prices = soup.find_all(class_="ticket_row")
#
#             ticket_prices = [x.text for x in ticket_prices]
#             cleaned_prices = [x.replace("\n", "").replace(" ", "") for x in ticket_prices]
#             cut_price = [x.split("$") for x in cleaned_prices]
#             final_price = "$" + cut_price[0][1]
#             prices.append(final_price)
#
#             events.append(soup.find(class_="summary").text)
#
#             all_headers = soup.find_all('h2')
#             datetimes = all_headers[1].text.lstrip()
#             splitdt = datetimes.split(",")
#
#             monthday = splitdt[1]
#             yeartime = splitdt[2].split(" at ")
#             year = yeartime[0]
#
#             time_raw = splitdt[-1].rstrip()
#             endtimetimesplit = time_raw.split(" at ")
#             endtime = endtimetimesplit[-1]
#             starttime = yeartime[1].split("-")[0]
#             time = starttime + "- " + endtime
#             times.append(time)
#
#
#             date_raw = monthday.lstrip() + year
#             dates.append(arrow.get(date_raw, "MMMM D YYYY").format("MM/DD/YY"))
#         except IndexError:
#             if not None:
#                 ticket_prices = soup.find(class_="js-display-price").text
#
#                 final_price = ticket_prices.replace("\n", "").lstrip().rstrip()
#                 prices.append(final_price)
#
#                 events.append(soup.find(class_="listing-hero-title").text)
#
#                 datee = soup.find(class_="event-details__data").find("p")
#                 raw_date = datee.text.split(",")
#                 final_date = raw_date[1].lstrip() + raw_date[2]
#                 try:
#                     dates.append(arrow.get(final_date, "MMMM D YYYY").format("MM/DD/YY"))
#                 except arrow.parser.ParserError:
#                     dates.append(arrow.get(final_date, "MMM D YYYY").format("MM/DD/YY"))
#
#                 dateandtime = soup.find(class_="event-details__data").text
#                 raw_time = dateandtime.split("\n")[5]
#                 splittime = raw_time.split(",")
#                 if len(splittime) > 1:
#                     time = splittime[-1].lstrip()
#                 else:
#                     time = raw_time.lstrip()
#                 times.append(time)
#     elif "eventbrite" not in links:
#         if tickets.index(i) not in other_links:
#             other_links.append(tickets.index(i))
#             olinkcounter += 1
#         else:
#             other_links.append(tickets.index(i)+olinkcounter)
#             olinkcounter += 1


# events2 = events1[other_links[0]:other_links[-1]+1]
for x in events1[2:-3]:
    header = x.find('h5').text
    print(header)
    datentime = header.split("th")
    if len(datentime) < 2:
        datentime = header.split("nd")

    time_raw = datentime[1].split("–")
    time = time_raw[0].lstrip()
    times.append(time)

    date_raw = datentime[0]
    dates_split = date_raw.split(" ")
    try:
        date_noyear = dates_split[1] + dates_split[2]

        now = datetime.now()
        year = now.year
        date_noformat = date_noyear + " " + str(year)
        date = arrow.get(date_noformat, "MMMMD YYYY").format("MM/DD/YY")
        dates.append(date)
    except IndexError:
        dates.append("NaN")

    prices.append("Free with reservation")

    event = x.find(class_="big-title").text
    events.append(event)


length = monthrange(2019, 1)[1]
tcounter = 0
for i in range(1, length+1):
    dt = f'2019-01-%s' % i
    date = arrow.get(dt, "YYYY-MM-D").format("MM/DD/YY")

    h1= [int(x) for x in dt.split('-')]
    answer = datet.date(h1[0], h1[1], h1[2]).weekday()

    if tcounter == 1 and answer == 1:
        events.append("Tutu Tuesday")
        times.append("10pm-late")
        prices.append("$10 or $2 in a tutu before 11pm")
        dates.append(date)
    elif answer == 1 and tcounter != 1:
        tcounter += 1

    if answer == 4:
        events.append("Motown Fridays Happy hour | Tacos from Maifoso Catering - DJ")
        times.append("5pm-9pm")
        prices.append("Free")
        dates.append(date)

    if answer == 2 or answer == 3:
        events.append("Happy hour")
        times.append("5pm-9pm")
        prices.append("Free")
        dates.append(date)

t = ""
try:
    df = pd.read_csv('harlotsf.csv')
except FileNotFoundError:
    t = "NaN"
except pd.errors.EmptyDataError:
    t = 'NaN'
if t == 'NaN':
    with open('harlotsftest.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "times", "Price"])
with open('harlotsftest.csv', 'a', encoding='utf-8') as ttable:
    filewriter = csv.writer(ttable)
    for b in range(0, len(events)):
        filewriter.writerow([venue, events[b], dates[b], times[b], prices[b]])


