#!/usr/bin/env python3
import json
import requests
import base64
import configparser
import sqlite3

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

connect = sqlite3.connect('freshdata.db')
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS agents
                  (agent_id text,
                  email text,
                  name text,
                  user_id text)''')

for agent in agents:
  agent_id = agent['agent']['id']
  email = agent['agent']['user']['email']
  name = agent['agent']['user']['name']
  user_id = agent['agent']['user']['id']
  a = (agent_id, email, name, user_id)
  cursor.execute('INSERT INTO agents (agent_id, email, name, user_id) VALUES (?,?,?,?)', a)

connect.commit()
