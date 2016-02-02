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

def get_all_open_tickets():
  """Returns a Requests object containing all data from all open tickets
  
  currently only gets up to 60 tickets
  """
  r = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json', headers = headers)
  r1 = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json&page=2', headers = headers)
  r2 = requests.get(baseurl + '/helpdesk/tickets/filter/open?format=json&page=3', headers = headers)
  return (r.json(), r1.json())

tickets, tickets1 = get_all_open_tickets()

db_connect = sqlite3.connect('freshdata.db')
cursor = db_connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tickets
                  (created_at text,
                  agent text,
                  ticket_number text,
                  subject text,
                  due_by text,
                  requester text,
                  priority text)''')

def add_tickets_to_db():
  for ticket in tickets:
    ticket_number = ticket['id']
    ticket_id = cursor.execute('''SELECT * FROM tickets WHERE
        ticket_number=?''', (ticket_number,))
    if ticket_id.fetchall() != []:
      print('already there')
    else:
      data = []
      data.append(ticket['created_at'])
      data.append(ticket['responder_id'])
      data.append(ticket['id'])
      data.append(ticket['subject'])
      data.append(ticket['due_by'])
      data.append(ticket['requester_name'])
      data.append(ticket['priority'])
      cursor.execute('''INSERT INTO tickets (created_at, agent, ticket_number,
      subject, due_by, requester, priority) VALUES (?, ?, ?, ?, ?, ?, ?)''', data)
  for ticket in tickets1:
    ticket_id = cursor.execute('''SELECT * FROM tickets WHERE ticket_number=?''',
        (ticket['id'],))
    if ticket_id.fetchall() != []:
      print('already there')
    else:
      data = []
      data.append(ticket['created_at'])
      data.append(ticket['responder_id'])
      data.append(ticket['id'])
      data.append(ticket['subject'])
      data.append(ticket['due_by'])
      data.append(ticket['requester_name'])
      data.append(ticket['priority'])
      cursor.execute('''INSERT INTO tickets (created_at, agent, ticket_number,
      subject, due_by, requester, priority) VALUES (?, ?, ?, ?, ?, ?, ?)''', data)
    #print(ticket['created_at'],ticket['responder_id'],ticket['id'],ticket['subject'],ticket['due_by'],ticket['requester_name'],ticket['priority'])
add_tickets_to_db()
db_connect.commit()
#for stuff in tickets[1]:
#  print(stuff)
#for ticket in tickets:
#  print(ticket['display_id'],ticket['requester_name'], ticket['subject'])
#for ticket in tickets1:
#  print(ticket['display_id'],ticket['requester_name'], ticket['subject'])
