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
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import os
import codecs
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

# api = twitter.Api(consumer_key=con_key,
#     consumer_secret=con_secret,
#     access_token_key=token_key,
#     access_token_secret=token_secret)

# open sqlite3 db, query the most recent status_id
conn = sqlite3.connect('bgptable.db')
curs = conn.cursor()

# Grab all of the IPv4 information in ascending order
curs.execute('SELECT * FROM bgp4_statuses ORDER BY status_id ASC')
rows = curs.fetchall()

# day variables
day_min = 0
day_max = 0
day_total = 0
day_average = 0
day_count = 0
day_first_value = 0
day_last_value = 0
day_growth_percent = 0

week_min = 0
week_max = 0
week_total = 0
week_average = 0
week_count = 0
week_first_value = 0
week_last_value = 0

month_min = 0
month_max = 0
month_total = 0
month_average = 0
month_count = 0
month_first_value = 0
month_last_value = 0

bgp4_day_list = [0,0,0,0,0,0,0]
bgp4_day_max = [0,0,0,0,0,0,0]
bgp4_day_min = [0,0,0,0,0,0,0]
bgp4_xlabels = ['','','','','','','']

if len(rows) > 1:
    # we have more than 2 records available
    

    
    for row in rows:
        # lets build a couple stats
        dt = parser.parse(row[2])
        year,weeknum,dow = dt.isocalendar()
        c_year,c_weeknum,c_dow = dt.today().isocalendar()
        
        
        # % growth over the last day
        if(dt.date() == dt.today().date()):
            
            if(row[1] > day_max):
                day_max = row[1]
                
            if(row[1] < day_min or day_min == 0):
                day_min = row[1]
            
            day_total += row[1]
            day_count += 1
            
            if(day_count == 1):
                day_first_value = row[1]
                
            day_last_value = row[1]
            
        # % growth over the last week
        if(weeknum == c_weeknum):
            # append to this week's data list
            if(row[1] > week_max):
                week_max = row[1]
                
            if(row[1] < week_min or week_min == 0):
                week_min = row[1]
            
            week_total += row[1]
            week_count += 1
            
            if(week_count == 1):
                week_first_value = row[1]
                
            week_last_value = row[1]
            
            # set the day value to the last value of that day
            bgp4_day_list[dow] = row[1]
            bgp4_xlabels[dow] = str(dt.date())
            if(row[1] > bgp4_day_max[dow]):
                bgp4_day_max[dow] = row[1]
                
            if(row[1] < bgp4_day_min[dow] or bgp4_day_min[dow] == 0):
                bgp4_day_min[dow] = row[1]
   
        # % growth over the last month
        if(dt.month == dt.today().month):
            
            if(row[1] > month_max):
                month_max = row[1]
                
            if(row[1] < month_min or month_min == 0):
                month_min = row[1]
            
            month_total += row[1]
            month_count += 1
            
            if(month_count == 1):
                month_first_value = row[1]
                
            month_last_value = row[1]
                
else:
    # not enough information to run statistics on
    # should probably just exit here
    exit()


day_average = day_total / day_count
day_growth_percent = ((day_last_value - day_first_value)/float(day_first_value))*100

week_average = week_total / week_count
week_growth_percent = ((week_last_value - week_first_value)/float(week_first_value))*100

month_average = month_total / month_count
month_growth_percent = ((month_last_value - month_first_value)/float(month_first_value))*100
    
# # create graph
#
plt.figure(1)
plt.xlabel('Day')
plt.ylabel('Prefixes')
plt.title('BGP4 Weekly Graph')
plt.axis([.75,7.25,((week_min / 10)*10),(((week_max+10)/10)*10)])
blue_line = plt.plot([1,2,3,4,5,6,7],bgp4_day_list,'b--',label='Last Prefixes')
yellow_square = plt.plot([1,2,3,4,5,6,7],bgp4_day_max,'ys',label='Max Prefixes')
green_triangle = plt.plot([1,2,3,4,5,6,7],bgp4_day_min,'g^',label='Min Prefixes')
plt.rcParams['legend.loc'] = 'best'
plt.legend()
locs, labels = plt.xticks([1,2,3,4,5,6,7], bgp4_xlabels)
plt.setp(labels,rotation=90)
#plt.show()
plt.savefig('weekly_bgp4_graph.png', bbox_inches='tight')
file = open('weekly_bgp4_graph.png', 'rb')
data = file.read()
file_name = os.path.realpath(file.name)
status_str = 'Weekly BGP4 Graph [{:3.3f}% Growth]'.format(week_growth_percent)
api.update_with_media(status=status_str,filename=file_name)


# Grab all of the IPv4 information in ascending order
curs.execute('SELECT * FROM bgp6_statuses ORDER BY status_id ASC')
rows = curs.fetchall()

# day variables
day_min = 0
day_max = 0
day_total = 0
day_average = 0
day_count = 0
day_first_value = 0
day_last_value = 0
day_growth_percent = 0

week_min = 0
week_max = 0
week_total = 0
week_average = 0
week_count = 0
week_first_value = 0
week_last_value = 0

month_min = 0
month_max = 0
month_total = 0
month_average = 0
month_count = 0
month_first_value = 0
month_last_value = 0

bgp6_day_list = [0,0,0,0,0,0,0]
bgp6_day_max = [0,0,0,0,0,0,0]
bgp6_day_min = [0,0,0,0,0,0,0]
bgp6_xlabels = ['','','','','','','']

if len(rows) > 1:
    # we have more than 2 records available
    

    
    for row in rows:
        # lets build a couple stats
        dt = parser.parse(row[2])
        year,weeknum,dow = dt.isocalendar()
        c_year,c_weeknum,c_dow = dt.today().isocalendar()
        
        
        # % growth over the last day
        if(dt.date() == dt.today().date()):
            
            if(row[1] > day_max):
                day_max = row[1]
                
            if(row[1] < day_min or day_min == 0):
                day_min = row[1]
            
            day_total += row[1]
            day_count += 1
            
            if(day_count == 1):
                day_first_value = row[1]
                
            day_last_value = row[1]
            
        # % growth over the last week
        if(weeknum == c_weeknum):
            # append to this week's data list
            if(row[1] > week_max):
                week_max = row[1]
                
            if(row[1] < week_min or week_min == 0):
                week_min = row[1]
            
            week_total += row[1]
            week_count += 1
            
            if(week_count == 1):
                week_first_value = row[1]
                
            week_last_value = row[1]
            bgp6_day_list[dow] = row[1]
            bgp6_xlabels[dow] = str(dt.date())
            if(row[1] > bgp6_day_max[dow]):
                bgp6_day_max[dow] = row[1]
                
            if(row[1] < bgp6_day_min[dow] or bgp6_day_min[dow] == 0):
                bgp6_day_min[dow] = row[1]
   
        # % growth over the last month
        if(dt.month == dt.today().month):
            
            if(row[1] > month_max):
                month_max = row[1]
                
            if(row[1] < month_min or month_min == 0):
                month_min = row[1]
            
            month_total += row[1]
            month_count += 1
            
            if(month_count == 1):
                month_first_value = row[1]
                
            month_last_value = row[1]
            

    day_average = day_total / day_count
    day_growth_percent = ((day_last_value - day_first_value)/float(day_first_value))*100

    week_average = week_total / week_count
    week_growth_percent = ((week_last_value - week_first_value)/float(week_first_value))*100
    
    month_average = month_total / month_count
    month_growth_percent = ((month_last_value - month_first_value)/float(month_first_value))*100
    
else:
    # not enough information to run statistics on
    # should probably just exit here
    exit()

# create graph

plt.figure(2)
plt.xlabel('Day')
plt.ylabel('Prefixes')
plt.title('BGP6 Weekly Graph')
plt.axis([.75,7.25,((week_min / 10)*10),(((week_max+10)/10)*10)])
blue_line = plt.plot([1,2,3,4,5,6,7],bgp6_day_list,'b--',label='Last Prefixes')
yellow_square = plt.plot([1,2,3,4,5,6,7],bgp6_day_max,'ys',label='Max Prefixes')
green_triangle = plt.plot([1,2,3,4,5,6,7],bgp6_day_min,'g^',label='Min Prefixes')
plt.rcParams['legend.loc'] = 'best'
plt.legend()
locs, labels = plt.xticks([1,2,3,4,5,6,7], bgp6_xlabels)
plt.setp(labels,rotation=90)
#plt.show()
plt.savefig('weekly_bgp6_graph.png', bbox_inches='tight')
file = open('weekly_bgp6_graph.png', 'rb')
data = file.read()
file_name = os.path.realpath(file.name)
status_str = 'Weekly BGP6 Graph [{:3.3f}% Growth]'.format(week_growth_percent)
api.update_with_media(status=status_str,filename=file_name)

curs.close()
conn.close()


