#!/usr/bin/python3

import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests
import json

## Upbit REST api
access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)

#print(res.json())

## JSON
tmp = json.loads(res.text)
for dict in tmp:
    print(str(dict['currency']) \
      + ": " + str(dict['balance']) \
      + "\t (@ " + str(dict['avg_buy_price']) + ")")
