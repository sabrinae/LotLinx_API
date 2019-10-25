import json
import requests
import pandas as pd
import csv

originalURL = "https://turnapi-production.lotlinx.com/account.jsp?token"

payload = {
    "user": "my_username",
    "pwd": "my_password",
    "method": "login"
}

response = requests.post(url=originalURL, data=json.dumps(payload))
if response.status_code != 200:
  print(response.status_code)

login_data = json.loads(response.text)
print(login_data)

access_token = login_data['token']
accounts = login_data['dealers']
client_ids = []

for org in accounts:
  clients = org['id']
  client_ids.append(clients)

def grabVINReports(client_ids,access_token):
  api_endpoint = "https://turnapi-production.lotlinx.com/enterprise/vindelivery.jsp"
  print(len(client_ids))
  
  i = 0
  while i < len(client_ids):
    params = {
      "method": "get",
      "id": client_ids[i],
      "timeperiod": "201909",
      "token": access_token
    }
    i+=1
    #print(params)
    columns = ['VIN','Type','Make','Model','Year','Shoppers','Spend']
    rows = []
    
    vin_response = requests.post(url=api_endpoint, data=json.dumps(params), headers={'content-type':'application/json'}).json()
    print(vin_response['vehicles'])
    
    for column in columns:
      if 'error' not in vin_response:
        print(vin_response['vehicles'])
        
        for x in rows:
          for y in x['vehicles']:
            rows.append([vin_response[y]['vin'], vin_response[y]['type'], vin_response[y]['make'], vin_response[y]['model'], vin_response[y]['year'],vin_response[y]['vinDropShoppers'], vin_response[y]['coreSpend']])
      
    eachDF = pd.DataFrame(rows)
    eachDF.columns = columns
    eachDF.index = pd.RangeIndex(len(eachDF.index))
    print(eachDF.sample(2))
  
grabVINReports(client_ids,access_token)
