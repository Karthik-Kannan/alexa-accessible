#!/usr/bin/python

import urllib2
import json
import os

actions = ['clockwise', 'counterclockwise', 'vertical swipe', 'horizontal swipe', 'tap']

response = urllib2.urlopen('http://656305d5.ngrok.io/get_json/')
data = json.load(response)
alexa_map = {}
for action in actions:
  if action in data.keys():
    alexa_map[action] = data[action]
  else:
    alexa_map[action] = None
print json.dumps(alexa_map)
with open("alexa_actions.json" , 'w') as f:
  f.write(json.dumps(alexa_map))
