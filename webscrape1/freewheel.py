import bs4 as bs
import requests
import arrow
import csv
import pandas as pd


def freewheel():
    venue = "Freewheel Brewing Compnay"
    price = "NaN"

    month = input("Please enter the number of the month in the form '1':  ")
    for l in range(1, 13):
      if month == str(l):
          mnum = month
          mnum = mnum.zfill(2)
          break
      elif (l == 12) & (str(month) != l):
          print("Please enter a valid option")
          freewheel()

    year = input("Please enter a year in the form '18'")
    for yr in range(18, 100):
      if year == str(yr):
          year_name = arrow.get(year, 'YY').format('YYYY')
          break
      elif (yr == 99) & (str(yr) != year):
          print("Please enter a valid input")
          freewheel()

    site_url = "http://freewheelbrewing.com/?cid=mc-6bea5a7e02f8f5e2945b6f6b1bbf9266&page_id=524&month="+mnum+"&yr="+year_name
    site = requests.get(site_url)
    soup = bs.BeautifulSoup(site.content, 'lxml')
    main_page = soup.find_all(class_="url summary has-image")

    urls = [x.get('href') for x in main_page]

    events = []
    dates = []
    times = []
    for url in urls:
        site = requests.get(url)
        soup = bs.BeautifulSoup(site.content, 'lxml')
        content = soup.find(class_="summary")
        events.append(content.text)

        date = (soup.find(class_="mc-event-date")).text
        dates.append(date)
        try:
          starttime = (soup.find(class_="event-time dtstart")).text
          endtime = (soup.find(class_="end-time dtend")).text
          time = starttime + " - " + endtime
          times.append(time)
        except AttributeError:
          times.append("NaN")

        times = [i.replace("\n", "") for i in times]
        events = [x.replace('\n', '') for x in events]
        events = [x.lstrip() for x in events]

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #   df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #   t = "NaN"
    # except pd.errors.EmptyDataError:
    #   t = 'NaN'
    # if t == 'NaN':
    with open('freewheel.csv', 'w') as ttable:
      filewriter = csv.writer(ttable)
      filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('freewheel.csv', 'a') as ttable:
      filewriter = csv.writer(ttable)
      for i in range(0, len(dates)):
          filewriter.writerow([venue, events[i], dates[i], times[i], price])
        
freewheel()
