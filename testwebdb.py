import requests
import time
import json
firebase_url = 'https://ramkarde-3348.firebaseio.com/'
#current time and date
time_hhmmss = time.strftime('%H:%M:%S')
date_mmddyyyy = time.strftime('%d/%m/%Y')
temperature_c = '35'    
    #current location name
temperature_location = 'Mumbai-Kandivali';
print temperature_c + ',' + time_hhmmss + ',' + date_mmddyyyy + ',' + temperature_location
    
#insert record

data = {'date':date_mmddyyyy,'time':time_hhmmss,'value':temperature_c}
result = requests.post(firebase_url + '/' + temperature_location + '/temperature.json', data=json.dumps(data))
