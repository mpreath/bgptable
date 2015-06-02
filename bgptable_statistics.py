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

import twitter
import re
import sqlite3
from dateutil import parser
from tabulate import tabulate

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


# lets do some calculations, post results to twitter?, should be once daily
# for each day, week, and month
# % growth
# average
# min, max
print("BGP4 Information")
table = [["Day",day_min,day_max,day_average,"{:3.3f}%".format(day_growth_percent)],
        ["Week",week_min,week_max,week_average,"{:3.3f}%".format(week_growth_percent)],
        ["Month",month_min,month_max,month_average,"{:3.3f}%".format(month_growth_percent)]]

print(tabulate(table, headers=["Min Prefixes","Max Prefixes", "Avg Prefixes", "Growth %"]))

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


# lets do some calculations, post results to twitter?, should be once daily
# for each day, week, and month
# % growth
# average
# min, max
print("")
print("BGP6 Information")
table = [["Day",day_min,day_max,day_average,"{:3.3f}%".format(day_growth_percent)],
        ["Week",week_min,week_max,week_average,"{:3.3f}%".format(week_growth_percent)],
        ["Month",month_min,month_max,month_average,"{:3.3f}%".format(month_growth_percent)]]

print(tabulate(table, headers=["Min Prefixes","Max Prefixes", "Avg Prefixes", "Growth %"]))

curs.close()
conn.close()


