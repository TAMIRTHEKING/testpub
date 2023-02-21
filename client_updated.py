import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from home_test_bondit_updeted import get_Sucsess

# a very simple test client

# test the all flighits


def test_flights():
    url = 'http://localhost:5000/flights'

# GET flights
    r = requests.get(url)
# to data frame
    df = pd.json_normalize(r.json())
# cluclate sucess
    print(df)
    return df


df = test_flights()


# test update flight by id
flight_id = 'C235'
success = 'success'

url1 = 'http://localhost:5000/flights/{}'.format(
    flight_id)+'/{}'.format(success)
response = requests.post(url1)
print(response.json())
test_flights()

# test update flight by id with not valid sccess
flight_id = 'G86'
success = 'not valid :)'

url1 = 'http://localhost:5000/flights/{}'.format(
    flight_id)+'/{}'.format(success)
response = requests.post(url1)
print(response.json())


test_flights()


# get the sucesess rate and test Q1
df_new = get_Sucsess(df)

print(df_new)
# extra test batch update by id
payload = {
    "updates": df_new[["flight ID", "success"]].rename(columns={"flight ID": "flight_id"}).to_dict(orient="records")
}

r = requests.post("http://localhost:5000/update_flights",
                  json=(payload['updates']))

r.json()


test_flights()


# get non server flights for testing batch and test Q1 on a bigger csv

df_new = get_Sucsess(pd.read_csv("bigger_sample.csv"))
df_new

payload = {
    "updates": df_new[["flight ID", "success"]].rename(columns={"flight ID": "flight_id"}).to_dict(orient="records")
}


r = requests.post("http://localhost:5000/update_flights",
                  json=(payload['updates']))
# see responce with not found and na
r.json()


test_flights()
