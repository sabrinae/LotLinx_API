import json
import requests
from datetime import date, timedelta

USER = 'username'
PWD = 'password'
METHOD = 'login'

headers = {
    'method':METHOD,
    'user':USER,
    'pwd':PWD
}

login_url = 'https://turnapi-production.lotlinx.com/account.jsp'

login_response = requests.post(login_url, json=headers)
data = json.loads(login_response.content)
print(data)

token = data['token']
print(token)

"""
account_ids = []
for x in data['dealers']:
  all_ids = x['id']
  account_ids.append(str(all_ids))
  print(account_ids)
"""

import pandas as pd

def dataGrab(token):
  last_month = date.strftime(date.today() - timedelta(1),"%Y%m") #timeperiod needs to be formatted as YYYYMM in request
  api_url = 'https://turnapi-production.lotlinx.com/reseller.jsp'

  payload = {
      'token': token,
      'timeperiod': last_month,
      'method': 'summaryReport'
  }

  data_response = requests.post(api_url, json=payload)
  print(data_response)

  client_data = json.loads(data_response.content)

  def parseData(client_data):
    month = date.strftime(date.today() - timedelta(1),"%YY-%m-%d")

    # first df is lotlinx totals
    lotlinx_totals = []
    lotlinx_totals_columns = ['Month','Dealer','Total Budget Delivered','Total Shoppers','Percent New to Site','Total VINs Reached','Total VINs Sold']

    for x in client_data['dealers']:
      dealer = [x]['dealerName']
      total_budg_delivered = [x]['totalBudgetDelivered']
      total_shoppers = [x]['totalShoppersDelivered']
      percent_new_to_site = [x]['percentNewToSite']
      total_vins_reached = [x]['totalVinsReached']
      total_vins_sold = [x]['totalVinsSold']

      lotlinx_totals.append([month, dealer, total_budg_delivered, total_shoppers, percent_new_to_site, total_vins_reached, total_vins_sold])
      lotlinx_totals_df = pd.DataFrame(lotlinx_totals,columns=lotlinx_totals_columns)
    
    # second df is lotlinx campaigns for each client
    lotlinx_campaigns = []
    lotlinx_campaigns_columns = ['Month','Dealer','Campaign','Budget Delivered','Shoppers Delivered','VINs Delivered','Shoppers per VINs Delivered','VINs Sold']

    for y in client_data['dealers']:
      dealer_name = [y]['dealerName']
      campaign = [y]['campaignName']
      budget_delivered = [y]['budgetDelivered']
      shoppers_delivered = [y]['shoppersDelivered']
      vins_delivered = [y]['vinsReached']
      shoppers_per_vin = [y]['shoppersPerVin']
      vins_sold = [y]['vinsSold']

      lotlinx_campaigns.append([month, dealer_name, campaign, budget_delivered, shoppers_delivered, vins_delivered, shoppers_per_vin, vins_sold])
      lotlinx_campaigns_df = pd.DataFrame(lotlinx_campaigns,columns=lotlinx_campaigns_columns)

    print(lotlinx_totals_df)
    print(lotlinx_campaigns_df)

  parseData(client_data)
dataGrab(token)
