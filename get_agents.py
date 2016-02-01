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

def get_all_agents():
  """Returns json-formatted list of a Requests object containing all agent data
  
  """
  r = requests.get(baseurl + '/agents.json', headers = headers)
  return r.json()

agents  = get_all_agents()

for agent in agents:
  print(agent)
