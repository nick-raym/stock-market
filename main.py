import requests
import json

from flask import Flask, make_response, jsonify, request, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin
import string, datetime

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

# use your own account number, password and appid to authenticate 
account = "701913"
password = "7DFE8BAB"
appid = "76bc8dba-43dc-4f76-bc6a-98488651a243"

# Build auth url
authurl = f"https://ftl.fasttrack.net/v1/auth/login?account={account}&pass={password}&appid={appid}"
print(authurl)
# make authentication request
authresponse = requests.get(authurl)

# parse result and extract token
token = authresponse.json()['token']

tickers = ["AMZN"]

# construct a header object containing your credentials. 
headers = {
    'appid': appid,
    'token': token
}

# Initialize an empty list to hold all details
all_details = []
date_range_data=[]
date_index=0

datesURL="https://ftl.fasttrack.net/v1/data/dates"
dates_response=requests.get(datesURL,headers=headers)
allDates=dates_response.json()
# print(allDates['dtes'])
wanted_date_str="19981211"
# print(allDates['dtes'][3])
for date in allDates['dtes']:
    if(str(date['yyyymmdd'])==str(wanted_date_str)):
        print(date['marketdate'])
        date_index=date['marketdate']
        date_index=int(date_index)
        break

for ticker in tickers:
    dateRangeURL = f"https://ftl.fasttrack.net/v1/data/{ticker}"
    dateResp = requests.get(dateRangeURL, headers=headers)
    if dateResp.status_code==200:
        dateData = dateResp.json()
        date_range_data.append(dateData)
    else:
        print("failed")


# prints amazon (first stock in list) price for 2 days ago
# print(date_range_data[0]['prices'][date_index])
# print(date_range_data[0]['name'])
# print(date_range_data[0]['startdate'])
# print(date_range_data[0]['ticker'])



for ticker in tickers:
    # Build URL for each ticker/stock abbreviation
    url = f"https://ftl.fasttrack.net/v1/stats/{ticker}"

    # Make GET request for each ticker
    response = requests.get(url, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        detail = response.json()
        # Append the detail to the all_details list
        all_details.append(detail)
        
    else:
        print(f"Failed to get data for ticker: {ticker}")

# Print all items in all_details
print("Ticker, Price, Low 52, high 52, Prev day")
for detail in all_details:
    # print(detail)
    print(
        detail['ticker'],
        ",",
        float(detail['describe']["price"]),
        ",",
        detail["describe"]["low_52"],
        ",",
        detail["describe"]['high_52'],
        ",",
        date_range_data[0]['prices'][0]
    )