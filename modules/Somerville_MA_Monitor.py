# import libraries
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
import re

LOCATION_NAME="Somerville"
PAGE_URL="https://www.somervillema.gov/departments/programs/novel-coronavirus-preparedness-and-information"

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

    counts_row = soup.find_all('tr')[3].find_all("td")
    # confirmed_date = datetime.strptime(somerville_row[0].text.replace("\n",""), "%m/%d/%y")
    confirmed_cases = int(counts_row[0].text.replace("Tested Positive","").split("\n")[0])
    recovered = int(counts_row[1].text.replace("Recovered","").split("\n")[0])
    deaths = int(counts_row[2].text.replace("Deaths","").split("\n")[0])

    # Get last updated date
    somerville_date = soup.find_all("span", {"style": "color:#df3114;"})[1].find("em").text.split(" as of ")[1].replace("\xa0","").replace(".","")#[:-4]#.split(" at ")[0]
    confirmed_date = datetime.strptime(somerville_date, "%m/%d/%y at %H:%M%p")

    data = {
        "name" : LOCATION_NAME,
        "date" : confirmed_date,
        "confirmed" : confirmed_cases,
        "recovered" : recovered,
        "deaths" : deaths
    }

    if debug:
        print(data)

    return data

if __name__ == "__main__":
    pass
    get_data(True)
    