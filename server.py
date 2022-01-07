from flask import Flask, request
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)
@app.route("/slack/events",methods=['GET','POST'])
def authorize():
  output = request.get_json()
  return output["challenge"]

slack_events_adapter = SlackEventAdapter(VERIFICATION_TOKEN, 
                                         "/slack/events", app)

@slack_events_adapter.on("reaction_added")
def reaction_added(event):
 print("Hello")
 emoji = event.get("event").get("reaction")
 print(emoji)

if __name__ == "__main__":
  app.run(port=3000)