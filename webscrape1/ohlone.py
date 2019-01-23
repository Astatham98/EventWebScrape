import bs4 as bs
import requests
import arrow
import csv
import pandas as pd


def ohlone():
    # Venue name
    venue = "Ohlone College"
    # Parses the site url and finds all the buttons for looking at event dates
    site_url = "https://tix6.centerstageticketing.com/sites/ohlone6/events.php"
    site = requests.get(site_url)
    soup = bs.BeautifulSoup(site.content, 'html.parser')
    event_items = soup.find_all(class_='btn btn-block btn-success btn-flat btn_purchase')

    # strips the link to get a plain link
    plain_link = site_url.replace("events.php", "")

    # Goes through the event items
    purchase_links = []
    for i in event_items:
        # turns to text and strips the spaces
        l = i.text
        l = l.lstrip()
        # Looks for purchases only
        if "Purchase" in l:
            purchase_links.append(i)

    times = []
    dates = []
    events = []
    prices = []
    # Searches through the links
    for link in purchase_links:
        # Gets the url end
        link = link.get('href')
        # adds the ends to the plain link
        full_link = plain_link + link

        # goes through each site and looks for the event details
        site = requests.get(full_link)
        soup = bs.BeautifulSoup(site.content, 'html.parser')
        details_raw = (soup.find_all(class_="performance_table_row"))

        # Looks for the show name
        show_name = (soup.find(class_="lbl_Show")).text
        # Appends cleaned event name to events the amount of times it appears in the webpage
        for num in range(len(details_raw)):
            events.append(show_name.replace("\n", ""))

        # Looks through teh details
        for details in details_raw:
            # Turns to text and splits them by newlines
            details1 = details.text
            details1 = details1.split("\n")
            # Looks for buttons for purchase links and gets the url
            links = soup.find(class_="btn btn-block btn-success btn-flat btn-purchase")
            partial_link = links.get('href')

            # If theres a general admission follow this path
            if "general-admission" in partial_link:
                # Creates a full links
                full_l = plain_link + partial_link
                # Parses the new website and looks for the table rows
                price_site = requests.get(full_l)
                soup = bs.BeautifulSoup(price_site.content, "html.parser")
                even = soup.find_all(class_="tix-even")
                odd = soup.find_all(class_="tix-odd ui-state-default")

                # Joins the table row values into one list and turns it into text
                td_list = even + odd
                td_list = [x.text for x in td_list]

                # Initialize age_list
                age_list = ""
                for ages in td_list:
                    # Splits by new lines
                    ages = ages.split("\n")
                    # Chooses the price and age only
                    ages = ages[-2]
                    # Joins all the prices from a specific website and appends them
                    age_list = age_list + ages + " "
                prices.append(age_list)
            else:
                # If not general admission appends NaN because of too many prices
                prices.append('NaN')

            # Finds the start time
            time = details1[2]
            times.append(time)

            # Splits the dates by ,
            date_raw = details1[1].split(",")
            # Finds the month and year and the day number and joins them
            date1 = date_raw[1].lstrip()
            date2 = date_raw[2]
            date = date1 + date2
            # formats into the right format
            dates.append(arrow.get(date, "MMMM D YYYY").format("MM/DD/YY"))

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('timetable.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('ohlone.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('ohlone.csv', 'a') as ttable:
        filewriter = csv.writer(ttable)
        for i in range(0, len(dates)):
            filewriter.writerow([venue, events[i], dates[i], times[i], prices[i]])


ohlone()
