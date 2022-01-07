import os
import json
import datetime

from pprint import pprint
f = open(os.path.dirname(__file__) + '/../opening_hours.json')
data = json.load(f)
def foodInMenu(food):
    f = open(os.path.dirname(__file__) + '/../menu.json')
    data = json.load(f)
    print(food.lower())
    for d in data['items']:
        print(d['name'])
        if d['name'].lower() == food.lower():
            return True
    return False

print(foodInMenu("burger"))