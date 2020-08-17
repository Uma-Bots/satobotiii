from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/', methods=['GET'])
def bot_iii():
    return 'Ok'

@app.route('/bot', methods=['GET'])
def bot_i():
    incoming_msg = request.values.get('message', '').lower()
    var_i = {
        "sender": "Rasa",
        "message": incoming_msg
    }
    webhook = 'http://web1:5005/webhooks/rest/webhook'
    requests_post = requests.post(webhook, json=var_i)
    json = requests_post.json()
    app.logger.info('requests_post, webhook, var_i:', json, webhook, var_i)
    cliente = MongoClient('mongo', 27017,username='root', password='(boquito&selma321)')
    print(cliente['sato_tracker_store']['talks'].insert_one({'i':var_i, 'o': json}).inserted_id)
    r = '<pre>'
    for j in json:
        print(j)
        text = 'text'
        if text in j:
            j_text_ = j[text]
            r += j_text_ + '\n'
        # image = 'image'
        # if image in j:
        #     r += j[image] + '\n'
    return r + '<pre>'


@app.route('/bot', methods=['POST'])
def bot_ii():
    app.logger.info(request.values)
    incoming_msg = request.values.get('Body', '').lower()
    incoming_MediaUrl0 = request.values.get('MediaUrl0', '')
    rinfo = None
    if incoming_MediaUrl0: 
        url = incoming_MediaUrl0
        r = requests.get(url, allow_redirects=True)
        response = r
        file = open("x.ogg", "wb")
        file.write(response.content)
        file.close()
        watson_url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/e3339fb6-d487-4e92-877b-68a6e8e1edb6/v1/recognize?model=pt-BR_BroadbandModel'
        headers = {'content-type': 'audio/ogg'}
        with open('x.ogg', 'rb') as f:
            audio = f.read()
            ri = requests.post(watson_url, auth=('apikey', 'TXbraU4SuBCuAvcAIAoXUg0WdO96nTwmNnqAdZo4umfN'), headers=headers, data=audio)
        app.logger.info(ri.json()['results'][0]['alternatives'][0]['transcript'])
        rinfo = ri.json()['results'][0]['alternatives'][0]['transcript']
    if rinfo:
        incoming_msg = rinfo
    resp = MessagingResponse()
    msg = resp.message()
    var_i = {
        "sender": "Rasa",
        "message": incoming_msg
    }
    app.logger.info(var_i)
    webhook = 'http://web1:5005/webhooks/rest/webhook'
    requests_post = requests.post(webhook, json=var_i)
    json = requests_post.json()
    app.logger.info([json, var_i])
    cliente = MongoClient('mongo', 27017,username='root', password='(boquito&selma321)')
    print(cliente['sato_tracker_store']['talks'].insert_one({'i':request.values,'o': json}).inserted_id)
    for j in json:
        print(j)
        text = 'text'
        if text in j:
            j_text_ = j[text]
            msg.body(j_text_)
        # image = 'image'
        # if image in j:
        #     msg.media(image)  # não funfa ainda TODO
    return str(resp)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
