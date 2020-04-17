# import libraries
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
import re

PAGE_URL = "https://www.mass.gov/info-details/covid-19-cases-quarantine-and-monitoring"

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

    # Take out the <table> elements
    ma_tables = soup.find_all('table')
    
    # Find quanrantine table update date
    quarantine_date_elem = soup.find('p', text = re.compile('^\*Data are accurate as of'))
    quarantine_date = quarantine_date_elem.text.split("*Data are accurate as of ")[1].split(" at ")[0]
    quarantine_date = datetime.strptime(quarantine_date, "%m/%d/%Y")

    (confirmed_date, confirmed_cases, quarantine_total, quarantine_released, quarantine_current) = parse_tables(ma_tables)

    data = {
        "confirmed_date" : confirmed_date,
        "confirmed_cases" : confirmed_cases,
        "quarantine_date" : quarantine_date,
        "quarantine_total" : quarantine_total,
        "quarantine_released" : quarantine_released,
        "quarantine_current" : quarantine_current
    }

    if debug:
        print(data)

    return data

def parse_tables(tables_list):
    pass

    confirmed_date = datetime.strptime(tables_list[0].find("th").text.split("as of ",)[1], "%B %d, %Y")
    confirmed_cases = int(tables_list[0].find("td").text.replace(",",""))
    #quarantine_date is not in the tables, retrieving it one level up
    quarantine_rows = tables_list[1].find_all("tr")
    quarantine_total = int(quarantine_rows[1].find("td").text.replace(",",""))
    quarantine_released = int(quarantine_rows[2].find("td").text.replace(",",""))
    quarantine_current = int(quarantine_rows[3].find("td").text.replace(",",""))
    
    return (confirmed_date, confirmed_cases, quarantine_total, quarantine_released, quarantine_current)

if __name__ == "__main__":
    pass
    get_data(True)