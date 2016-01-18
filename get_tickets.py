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
  """Returns a Requests object containing all data from all open tickets"""
  r = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json', headers = headers)
  return r
