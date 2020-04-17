# import libraries
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
import re

LOCATION_NAME="Cambridge"
PAGE_URL="https://www.cambridgema.gov/covid19"

def get_data(debug=False):

    # make request using user agent, otherwise page returns 403
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.2.1371.7 Safari/537.36"
    req = request.Request(PAGE_URL, headers={'User-Agent' : user_agent})
    
    # query the website and return the html to the variable ‘page’
    page = request.urlopen(req).read()

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    if debug:
        debug_write = open('temp.html','wb')
        debug_write.write(page)
        debug_write.close()
        print("DEBUG: Wrote HTML file of obtained page to: temp.html")

    # Get confirmed and death numbers
    confirmed = soup.find_all('p', {"class": "count"})[0].text
    deaths = soup.find_all('p', {"class": "count"})[1].text

    # Get last updated date
    last_updated = soup.find("div", {"class":"lastUpdated"}).text
    last_updated = datetime.strptime(last_updated, "Last Updated at %B %d, %I:%M %p")
    last_updated = last_updated.replace(year=2020)

    if debug:
        print(confirmed, deaths)
        print(last_updated)

    data = {
        "name" : LOCATION_NAME,
        "date" : last_updated,
        "confirmed" : confirmed,
        "recovered" : "NaN",
        "deaths" : deaths
    }

    if debug:
        print(data)

    return data

if __name__ == "__main__":
    pass
    get_data(True)
    