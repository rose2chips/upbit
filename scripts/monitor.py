#!/usr/bin/python3

import json
import os
import requests
import sys
import time

def log(logfile, msg):
  logfile.write(msg + os.linesep)

def getInitialCandle(logfile):
  global currency
  global margin_rate
  global high_price
  global threshold_price 

  ## Upbit REST api
  url = "https://api.upbit.com/v1/candles/days"
  querystring = {"market":"KRW-"+currency,"count":"2"}

  res = requests.request("GET", url, params=querystring)
  #print(res.text)

  ## JSON
  candle_date_time_kst=""
  tmp = json.loads(res.text)
  for dict in tmp:
   if high_price < dict['high_price']:
     candle_date_time_kst=dict['candle_date_time_kst']
     high_price = dict['high_price']

  log(logfile, "High Price: " + str(high_price) + " at candle " + str(candle_date_time_kst).replace("T", " "))
  threshold_price = high_price * (1.0 - margin_rate)
  log(logfile, "Threshold Price: " + str(threshold_price))
  logfile.flush()

def monitor(logfile):
  global currency
  global margin_rate
  global high_price
  global threshold_price 
  global last_low_price

  ## Upbit REST api
  url = "https://api.upbit.com/v1/candles/minutes/1"
  querystring = {"market":"KRW-"+currency,"count":"2"}

  res = requests.request("GET", url, params=querystring)
  #print(res.text)

  ## JSON
  tmp = json.loads(res.text)
  #print(type(tmp))
  #print(len(tmp))
  found = False
  for dict in tmp:
    if threshold_price > dict['low_price']:
      low_price = dict['low_price']
      if last_low_price == 0.0 or last_low_price != low_price:
        last_low_price = low_price
        log(logfile, str(dict['candle_date_time_kst']).replace("T", " ") \
  	      + ": " + str(dict['low_price']) + " (" + str(1.0 - (low_price / high_price)) + ")")
        found = True
    if high_price < dict['high_price']:
      candle_date_time_kst=dict['candle_date_time_kst']
      high_price = dict['high_price']
      threshold_price = high_price * (1.0 - margin_rate)
      log(logfile, "High Price: " + str(high_price) + " at candle " + str(candle_date_time_kst).replace("T", " "))
      log(logfile, "Threshold Price: " + str(threshold_price))
      found = True

  if found:
    logfile.flush()

## Main
TIMEOUT_1MIN = 60
TIMEOUT_3MIN = 180

currency='ETH';
margin_rate = 0.05

high_price = 0.0
threshold_price = 0.0

last_low_price = 0.0

if len(sys.argv) < 3:
  exit

margin_rate=float(sys.argv[1])
currency=str(sys.argv[2])

with open("./logs/" + currency + ".log", "a") as logfile:

  log(logfile, "")
  log(logfile, "###")
  log(logfile, "Margin rate: " + str(margin_rate))

  getInitialCandle(logfile)
  time.sleep(TIMEOUT_3MIN)

  try:
    while True:
      monitor(logfile)
      time.sleep(TIMEOUT_1MIN)
  except KeyboardInterrupt:
    print("Quitting the program.")
  except:
    print("Unexpected error: "+sys.exc_info()[0])
    raise  
