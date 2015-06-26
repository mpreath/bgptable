#!/usr/bin/python

# bgptable is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bgptables is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with onstools.  If not, see <http://www.gnu.org/licenses/>.

import tweepy
import re
import sqlite3
from dateutil import parser
import ConfigParser

con_key = "BBJ4wtXpErzYTkZ5K28yc4Ype"
con_secret = "okNbaGjgjAg0txCgTPXbtLwLYNbs3RI2Q6sYqio6JAZNwNpxPW"

config = ConfigParser.RawConfigParser()
config.read('bgptable.cfg')
access_token = config.get('Access Token', 'access_token')
access_token_secret = config.get('Access Token', 'access_token_secret')

auth = tweepy.OAuthHandler(con_key,con_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# open sqlite3 db, query the most recent status_id
conn = sqlite3.connect('bgptable.db')
curs = conn.cursor()

# IPV4 PREFIXES #

# make sure we have a bgp4_statuses table, if we don't create one
curs.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'bgp4_statuses\'')
rows = curs.fetchall()
if not rows:
    curs.execute('''CREATE TABLE bgp4_statuses(status_id INT PRIMARY KEY, prefixes INT, status_date_time TEXT)''')

curs.execute('SELECT * FROM bgp4_statuses ORDER BY status_id DESC LIMIT 1')
rows = curs.fetchall()

if rows:
    status_id = rows[0][0]
    # get all statuses newer than the most recent status_id in the db
    bgp4_statuses = api.user_timeline(screen_name='bgp4_table',since_id=status_id)
else:
    # this should only run the very first time when there are no statuses in the db
    # we'll grab 5 and put them in the database
    bgp4_statuses = api.user_timeline(screen_name='bgp4_table',count=30)


for status in bgp4_statuses:
    numbers = re.findall(' \d+ ', status.text)
    if numbers:
        # store these new statuses in the db
        dt = status.created_at
        print(str(dt)[:-9])
        print(status.id)
        print(numbers[0].strip())
        ins = 'INSERT INTO bgp4_statuses (status_id, prefixes, status_date_time) VALUES (?,?,?)'
        curs.execute(ins, (status.id, numbers[0].strip(), str(dt)[:-9]))

# IPV6 PREFIXES #


curs.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'bgp6_statuses\'')
rows = curs.fetchall()
if not rows:
    curs.execute('''CREATE TABLE bgp6_statuses(status_id INT PRIMARY KEY, prefixes INT, status_date_time TEXT)''')

curs.execute('SELECT * FROM bgp6_statuses ORDER BY status_id DESC LIMIT 1')
rows = curs.fetchall()

if rows:
    status_id = rows[0][0]

    # get all statuses newer than the most recent status_id in the db
    bgp6_statuses = api.user_timeline(screen_name='bgp6_table',since_id=status_id)
else:
    # this should only run the very first time when there are no statuses in the db
    # we'll grab 5 and put them in the database
    bgp6_statuses = api.user_timeline(screen_name='bgp6_table',count=5)


for status in bgp6_statuses:
    numbers = re.findall(' \d+ ', status.text)
    if numbers:
        # store these new statuses in the db
        dt = status.created_at
        print(str(dt)[:-9])
        print(status.id)
        print(numbers[0].strip())
        ins = 'INSERT INTO bgp6_statuses (status_id, prefixes, status_date_time) VALUES (?,?,?)'
        curs.execute(ins, (status.id, numbers[0].strip(), str(dt)[:-9]))

# close shop, we are done collecting
conn.commit()
curs.close()
conn.close()
