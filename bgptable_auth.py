#!/usr/bin/env python

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
import codecs
import sys
import webbrowser
import ConfigParser

consumer_key = "BBJ4wtXpErzYTkZ5K28yc4Ype"
consumer_secret = "okNbaGjgjAg0txCgTPXbtLwLYNbs3RI2Q6sYqio6JAZNwNpxPW"

# create the auth object
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)

# need to get a request object
try:
    redirect_url = auth.get_authorization_url(signin_with_twitter=True)
except:
    print ('Error! Failed to get request token')

webbrowser.open(redirect_url)
verifier = raw_input('Verifier:')
auth.get_access_token(verifier)
print(auth.access_token)
print(auth.access_token_secret)
#save the access_token and access_token_secrets

config = ConfigParser.RawConfigParser()
config.add_section('Access Token')
config.set('Access Token', 'access_token', auth.access_token)
config.set('Access Token', 'access_token_secret', auth.access_token_secret)

with open('bgptable.cfg', 'wb') as configfile:
    config.write(configfile)






