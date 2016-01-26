#!/usr/bin/env python3
import json
import requests
import base64
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

baseurl = config['FreshDesk']['base_url']
api_key = config['FreshDesk']['api_key']
b64string = base64.b64encode(api_key.encode()).decode('ascii')
auth = "Basic %s" % b64string
headers = {"Authorization": auth}

def get_all_open_tickets():
  """Returns a Requests object containing all data from all open tickets
  
  currently only gets up to 60 tickets
  """
  r = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json', headers = headers)
  r1 = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json&page=2', headers = headers)
  r2 = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json&page=3', headers = headers)
  return (r.json(), r1.json())

tickets, tickets1 = get_all_open_tickets()

#for stuff in tickets[1]:
#  print(stuff)
#for ticket in tickets:
#  print(ticket['display_id'],ticket['requester_name'], ticket['subject'])
#for ticket in tickets1:
#  print(ticket['display_id'],ticket['requester_name'], ticket['subject'])
