from bs4 import BeautifulSoup
from requests import get
import re
from datetime import datetime
from datetime import timedelta
import json
import pytz

# URL for whitby Masjid
url = "http://www.whitbymasjid.ca/"

#Api link for openweathermap
url2="http://api.openweathermap.org/data/2.5/weather?q=whitby&appid=###___API_KEY_HERE___###"

#get response from each webpage
response2 = get(url2)
response2=response2.json()

# print(response['cod'])

#get sunset from api as UNIX type
sunset = response2['sys']['sunset']

#Add 5 minutes to sunset, convert from Universal time to Local time
sunset = datetime.utcfromtimestamp(sunset) + timedelta(seconds=-14100)


# sunset.strftime(("%I:%M %p"))

#print only hour and minute of time
sunset = str(sunset.time().hour-12) + ":" + str(sunset.time().minute)

#regex for stripping out html tags
regex = re.compile(r'<[^>]+>')

#function that takes in argument, and removes html tags
def parse(rej):
    return regex.sub('', rej)

#response for masjid page
response = get(url)
html = response.text

# print(parse(html))


#ask reader which prayer time they want to know

#create prayertime dictionary
prayerTimes = {}

#soup
soup = BeautifulSoup(html, 'html.parser')

#parse through all list tags, find salaah times
for time in soup.find_all('li')[5:10]:
    temparr=[]

    x = parse(str(time))

    y =re.split(' ', x)
    if y[0] == 'Maghrib:':
        prayerTimes[y[0].replace(':', '').lower()] = (sunset)
    else:
        prayerTimes[y[0].replace(':', '').lower()] = y[1]

while True:
    prayer = input("Which prayer would you like to know the time of\n")

    print(prayerTimes[prayer.lower()])
print(prayerTimes)

# times=json.dumps(prayerTimes)
with open('times.json', 'w') as file:
    json.dump(prayerTimes, file)

