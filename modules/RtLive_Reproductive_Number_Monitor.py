# import libraries
import csv
from urllib import request
from datetime import datetime

STATE_OF_INTEREST = "MA"
URL = 'https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv'

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def get_rt():
    req = request.Request(URL)
    csv_file = request.urlopen(req).read().decode("utf-8").splitlines()

    cr = csv.DictReader(csv_file)

    # Keep only the last 2 values of the R number
    last_two = []
    for idx, row in enumerate(cr):
        if row["region"] == STATE_OF_INTEREST:
            if len(last_two) < 2:
                last_two.append(row)
            else:
                last_two.pop(0)
                last_two.append(row)

    # Calculate the R number difference. Mostly interested in whether it's negative or positive
    delta = float(truncate(float(last_two[1]["mean"]) - float(last_two[0]["mean"]), 2))
    
    data = {
        "latest_rt" : {
            "date" : datetime.strptime(last_two[1]["date"], "%Y-%m-%d"),
            "value" : float(last_two[1]["mean"])
        },
        "delta" : delta
    }

    return data

if __name__ == "__main__":
    pass
    print(get_rt())