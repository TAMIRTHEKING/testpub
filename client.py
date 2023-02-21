import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# a very simple test client

# test the all flighits
url = 'http://localhost:5000/flights'

# GET flights
r = requests.get(url='http://localhost:5000/flights')
# to data frame
df = pd.json_normalize(r.json())
# cluclate sucess
print(df)


# test update flaight
flight_id = 'G86'
success = 'Success'

url = 'http://localhost:5000/flights/{}'.format(flight_id)
response = requests.post(url, json={'success': success})
print(response.json())
