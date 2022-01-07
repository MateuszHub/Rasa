# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import os 
from datetime import datetime
import calendar
from pprint import pprint

class ActionReset(Action):

     def name(self) -> Text:
            return "action_reset"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("Your order was cleared")

         return [AllSlotsReset()]

class ActionSelectMenu(Action):

    def name(self) -> Text:
        return "select_menu"

    def validDate(self, _date, _time):
        f = open(os.path.dirname(__file__) + '/../opening_hours.json')
        data = json.load(f)
        date = datetime.strptime(_date, '%d.%m.%Y')
        hour, min = _time.split(":")
        dayName = calendar.day_name[date.weekday()]
        for key, value in data['items'].items():
            if key.lower() == dayName.lower():
                return int(value["open"]) <= int(hour) and (int(value["close"]) > int(hour) or (int(value["close"]) == int(hour) and int(min) == 0)) 
        return False

    def foodInMenu(self, food):
        f = open(os.path.dirname(__file__) + '/../menu.json')
        data = json.load(f)
        for d in data['items']:
            if d['name'].lower() == food.lower():
                return True
        return False

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food = tracker.get_slot('food')
        adt = tracker.get_slot('additional')
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        
        if self.foodInMenu(food) and self.validDate(date, time) and adt:
            orderText = "You oredered " + food + " with additioan message: " + adt +".\n Pickup in restaurant in " + date + " at " + time
            dispatcher.utter_message(text= orderText)
        else:
            dispatcher.utter_message(text= "Your order is invalid")
        return [AllSlotsReset()]

class ActionMenuInfo(Action):

    def name(self) -> Text:
        return "menu_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        f = open(os.path.dirname(__file__) + '/../menu.json')
        data = json.load(f)
        dispatcher.utter_message(text="Our menu: " + json.dumps(data['items'], indent=4))

        return []

class ActionOpenInfo(Action):

    def name(self) -> Text:
        return "open_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        f = open(os.path.dirname(__file__) + '/../opening_hours.json')
        data = json.load(f)
        dispatcher.utter_message(text="Restaurant opening hours: " + json.dumps(data['items'], indent=4) )

        return []