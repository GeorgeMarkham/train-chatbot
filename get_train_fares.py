from bs4 import BeautifulSoup
from datetime import datetime
import requests
from time import sleep
import csv

def get_train_fares(FROM, TO, DATE, TIME, get_cheapest=True, get_earliest=False):
    
    # Make sure if get_earliest is set then get_cheapest isn't
    if get_cheapest and get_earliest or get_earliest:
        get_cheapest=False

    if len(FROM) > 3:
        FROM = get_station_code(FROM)

    if len(TO) > 3:
        TO = get_station_code(TO)

    DATE = format_date(DATE)
    TIME = format_time(TIME, is_T=True)
    URL = "http://ojp.nationalrail.co.uk/service/timesandfares/" + FROM + "/" + TO + "/" + DATE + "/" + TIME + "/dep"
    
    req_counter = 0

    while(req_counter < 5):
        r = requests.get(URL)

        req_counter = req_counter + 1

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            if soup.find('h1', {'class':'sifr'}) != None and soup.find('h1', {'class':'sifr'}).get_text() == "Oh no! There's been a problem!":
                sleep(0.5)
            else:
                rows = soup.find('div', attrs={'id': 'ctf-results'}).find('table', attrs={'id':'oft'}).find('tbody').find_all('tr')
                tix = []
                for row in rows:
                    from_stn = row.find('td', attrs={'class':'from'})
                    to_stn = row.find('td', attrs={'class':'to'})
                    fare = row.find('td', attrs={'class':'fare'})
                    time = row.find('td', attrs={'class':'dep'})

                    ticket = {}

                    if from_stn != None and len(from_stn) > 2:
                        # print("FROM:\t" + from_stn.text.strip().split(" ")[0])
                        # print("TO:\t" + to_stn.text.strip().split(" ")[0])
                        # print("TIME:\t" + time.text.strip().split(" ")[0])
                        # print("COST:\t" + fare.find('label').text.strip().replace(" ", ""))
                        # print("-"*50)
                        ticket['from'] = from_stn.text.strip().split(" ")[0]
                        ticket['to'] = to_stn.text.strip().split(" ")[0]
                        ticket['time'] = int(format_time(time.text.strip().split(" ")[0]))
                        ticket['cost'] = float(fare.find('label').text.strip().replace(" ", "")[1:])
                        tix.append(ticket)
                if get_cheapest:
                    return get_cheapest_ticket(tix)
                elif get_earliest:
                    return get_earliest_ticket(tix)
                else:
                    return tix
            
def get_cheapest_ticket(tix):
    tix.sort(key=lambda x: x['cost'], reverse=False)
    return tix
def get_earliest_ticket(tix):
    tix.sort(key=lambda x: x['time'], reverse=False)
    return tix[0]

def format_date(date):
    date_string = date.split("T")[0]
    d = datetime.strptime(date_string, "%Y-%m-%d")
    return d.strftime('%d%m%y')

def format_time(time, is_T=False):
    if is_T:
        time_string_arr = time.split("T")[1].split(":")
    else:
        time_string_arr = time.split(":")
    return str(time_string_arr[0] + time_string_arr[1])
def get_station_code(station_name):
        with open('station_codes.csv') as station_codes_file:
            station_reader = csv.reader(station_codes_file, delimiter=',')
            for station in station_reader:
                if station[0].lower() == station_name.lower():
                    return station[1]

if __name__ == "__main__":
    print(get_train_fares("manningtree", "Norwich", "2019-01-16T11:02:56+00:00", "2019-01-07T15:00:00+00:00"))