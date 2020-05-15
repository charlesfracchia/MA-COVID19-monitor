# import libraries
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
import re

LOCATION_NAME="Boston"
PAGE_URL="https://www.boston.gov/news/coronavirus-disease-covid-19-boston"

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

    boston_block = soup.find_all("h4")[0].text.replace("\xa0"," ").split(" cases | ")
    confirmed_cases = int(boston_block[0].replace(",",""))
    recovered_cases = int(boston_block[1].replace(" recovered", "").replace(",",""))
    death_cases = int(soup.find_all("h4")[1].text.replace("\xa0"," ").replace(" deaths","").replace(",",""))

    #Get the year from the published article's date. Let's hope this doesn't drag on into 2021...
    publish_year = int(soup.find("time").text.split(", ")[1])
    confirmed_date = soup.find_all("address")[0].text.replace("\xa0", " ")
    confirmed_date = "%s %s" % (confirmed_date, publish_year)
    confirmed_date = datetime.strptime(confirmed_date, "Boston (as of %A, %B %d) %Y")

    #Get the date from the da

    data = {
        "name" : LOCATION_NAME,
        "date" : confirmed_date,
        "confirmed" : confirmed_cases,
        "recovered" : recovered_cases,
        "deaths" : death_cases
    }

    if debug:
        print(data)

    return data

if __name__ == "__main__":
    pass
    get_data(True)
    