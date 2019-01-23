import bs4 as bs
import requests
import arrow
import csv
import pandas as pd
import xml.etree.ElementTree as ET


def lark():
    # Venue and siteurl in xml format
    venue = "Lark Theater"
    site_url = "https://prod1.agileticketing.net/websales/feed.ashx?guid=fb90deda-265e-4618-8289-7268bfb70ada&&start=1543449600&end=1546214400"

    # gets site url
    response = requests.get(site_url)
    # Opens a new file and parses the contents of the webpge
    with open('feed.xml', 'wb') as file:
      file.write(response.content)

    # opens the xml file
    tree = ET.parse('feed.xml')
    # finds the first root
    root = tree.getroot()

    roots = []
    for child in root:
      #Appends the children in the root
      roots.append(child)

    #Uses the last element which
    root = roots[-1]
    rooted = []
    #Finds the final root to the events
    for child in root:
      rooted.append(child)

    #Initializes the lists
    names = []
    stime = []
    etime = []
    prices_site = []
    for root in rooted:
      for child in root:
        #Finds the tags for events and deletes the website
        child_tag = child.tag
        child_tag = child_tag.replace("{https://www.agiletix.com}", "")
        #If the tag is of type name it appends the name to a list
        if child_tag == "Name":
          names.append(child.text)
        #if the tag is of the needed type it appends the needed type to its specific list
        elif child_tag == "StartDate":
          stime.append(child.text)
        elif child_tag == "EndDate":
          etime.append(child.text)
        elif child_tag == "BuyLink":
          prices_site.append(child.text)

    date = []
    starttime = []
    endtime = []
    #Searches through the starttimes
    for i in stime:
      #Splits at T (time delimeter)
      i = i.split('T')
      #Appends the date only
      date.append(i[0])

      #The start time
      start = i[-1]
      #Replaces useless :00
      start = start.replace(":00", "")
      starttime.append(start)

    #Searches through end times
    for i in etime:
      #Splits at T
      i = i.split('T')
      end = i[-1]
      end = end.replace(":00", "")
      endtime.append(end)

    times = []
    #Joins the starttimes and endtimes using the length of the lists
    for i in range(len(starttime)):
      times.append(starttime[i] + " - " + endtime[i])

    dates = []
    #formats dates
    for d in date:
      dd = arrow.get(d, "YYYY-MM-D").format("MM/DD/YY")
      dates.append(dd)

    print("This may take some time...")
    #Start of counter for printing
    counter = 0
    prices = []
    for site in prices_site:
      counter += 1
      #Prints counter
      print(str(counter) + "/" + str(len(prices_site)) + " prices found")
      #Searches through sites
      site = requests.get(site)
      soup = bs.BeautifulSoup(site.content, 'html.parser')
      try:
        #Looks for prices
        price = (soup.find(id="TTSelection2_Repeater_ctl00_lblPrice")).text
        #replaces useless symbols
        price = price.replace(" - ", "")
      #If it can't find a price change it to NaN
      except AttributeError:
        price = "NaN"
      prices.append(price)

    print(len(names), len(dates), len(times), len(prices))


    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     pd.read_csv('lark.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('lark.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('lark.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(dates)):
            filewriter.writerow([venue, names[i], dates[i], times[i], prices[i]])


lark()