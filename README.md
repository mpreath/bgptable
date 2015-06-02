bgptable is a small set of Python scripts that scrapes the BGP4 and BGP6 table sizes from the @bgp4_table and @bgp6_table Twitter feeds. It stores the last 365 days of data into a sqlite database file and provides some analytical information regarding the data. It also can post graphs to a Twitter feed.

To use these utilities you must first run bgptable_auth.py
./bgptable_auth.py

Add ./bgptable_collect.py to a cron script that runs daily
Add ./bgptable_graph.py to a cron script that runs weekly, it will post two graphs to Twitter

Run ./bgptable_statistics.py as you desire, it will show statistics of the data stored in the sqlite database


Copyright (c) 2015 Matt Reath
