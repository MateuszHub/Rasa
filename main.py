from slackeventsapi import SlackEventAdapter
from slack import WebClient
import requests
import json
import threading
import re
VERIFICATION_TOKEN = "xoxb-2894089613382-2894097435046-lhb89IobqRGlMXQ9vDsKwGz0" 

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = "63e2cb3f5999e45f9b572dd6435247ab"
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")
slack_client = WebClient(VERIFICATION_TOKEN)



def get_resp(user, sentence):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {'message':sentence, "sender": user}
    response = requests.post(url,json=payload)
    print(response.json())
    return response.json()

def action_after_msg(msg):
    txt = msg.get('text')
    print(msg)
    user = msg.get('user')
    txt = re.sub('<@.+>', '', txt)
    _ts = msg.get('ts')
    resp = get_resp(user, txt)
    channel = msg["channel"]
    if len(resp) > 0:
        message = "<@" + user + "> " + resp[0]["text"]
    else:
        message = "<@" + user + "> " + " i dont understand."
    slack_client.chat_postMessage(channel=channel, text=message, thread_ts=_ts)


# Example responder to greetings
@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]
    threading.Thread(target=action_after_msg, args=(message,)).start()
    return "OK"

slack_events_adapter.start(port=80)