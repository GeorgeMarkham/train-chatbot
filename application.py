import os, sys
from flask import Flask, request
import json
from detect_intent import df_intent_detect
import requests




app = Flask(__name__)
# PAGE_ACCESS_TOKEN_1 = 'EAAf8lGp4TlIBAGo8NVIe4KvecFZCFxI0LXhZAydXZBDCcy7N0veEZBhQu3sMDetSYlGSYSXZCPRZAZAOFsHQnkjENpiYX5ZChMmGvqApZAL83NR0xZCffjw9iru2I2jHfaNUT9hxZCEZCjzKIBexZAxxDhUwQy7X1q38WZBZBDG8JXOXuUl6gZDZD'
PAGE_ACCESS_TOKEN = "EAAgjq581d4UBAGH58G1pakE9sy3DZBOWOgw3pZBUaI2d6PWSEOXqw248Bik8g8ngJZCNhjqOAVQ50XiZAMxn1izXzFIBffhQYILExvwIiC3zc6yOsWdj3tmDpZADnCqWZBLOx9HZBtXRqw8F0rd2F3nAB1ZBD0y5W0B8KKBP00y5a1Dlp9nnEY9i"
VERIFICATION_TOKEN = "9d35b6cb-e4b7-4db8-b0bb-8697122be8ca"
df = df_intent_detect()


@app.route('/', methods=['GET'])
def verify():
    print("Hit the GET /")
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return request.args["hub.challenge"], 200
        return "Incorrect verification token", 403
    return "", 200



@app.route('/', methods=['POST'])
def webhook():
    print("Hit the webhook")
    body = request.get_json()
    entry = body.get('entry')
    print(body)
    for entry in entry:
        messaging_entries = entry['messaging']
        for msg_entry in messaging_entries:
            try:
                s_id = msg_entry['sender']['id']
            except KeyError:
                print("no sender id")
                return "No sender ID given", 400
            if msg_entry.get('message'):
                msg = msg_entry['message']['text']
                print("Got this far 123456789 10")
                reply(s_id, df.detect_intent_and_reply(msg, s_id))
                # return df.detect_intent_and_reply(msg), 200
    return "Recieved the message", 200




# @app.route('/', methods=['POST'])
# def webhook():
#     data = request.get_json()
#     if data != None:
#         if data['object']=='page':
#             for entry in data['entry']:
#                 my_id = entry['id']
#                 for msging_event in entry['messaging']:
#                     print(msging_event)
#                     s_id = msging_event['sender']['id']
#                     if msging_event.get('message'):
#                         if 'text' in msging_event['message']:
#                             msg_text = msging_event['message']['text']
#                             print('111111111')
#                             print(msg_text)
#                             newRply = get_news_elements(wit_response(msg_text,s_id),s_id,msg_text)
#                         else:
#                             msg_text = 'no text'
#                         reply(s_id,newRply)
#     else:
#         return "No data", 400
#     return "ok",200

@app.route('/tos', methods=['GET'])
def tos():
    # Serve terms of service page
    return "Terms of service"

@app.route('/privacy', methods=['GET'])
def privacy():
    # Serve terms of service page
    return "Privacy policy"

@app.route('/help', methods=['GET'])
def help():
    # Serve terms of service page
    return "Help page"

# def log(message):
#     print(message)
    
#     sys.stdout.flush()

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN, json=data)
    # print("https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN, data)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug =True, port=5000)