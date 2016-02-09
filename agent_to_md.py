import sqlite3

fhand = open('agents.md', 'w')
conn = sqlite3.connect('freshdata.db')
curs = conn.cursor()

header = '# Agents\n'
get_agents = 'SELECT * FROM agents'

agents = curs.execute(get_agents)

fhand.write(header)
for agent in agents:
  fhand.write('## ' + agent[3] + '\n')
  for field in agent:
    fhand.write(field +'\n')

fhand.write('test')
fhand.close()
#for agent in agents:
#  print(agent)
