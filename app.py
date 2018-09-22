from flask import Flask, request
from pymessenger.bot import Bot
from enum import Enum
import pyowm
import json
import requests
import random


app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
# PAT = Page Access Token (for facebook)
PAT='EAACzPZAstSV0BAFiILURPFTFDfWKdmwgKPUfQM81EAQZBH47brlOuZCTWTCZBSitvVOTQTqGbALuEPsBKZApsLOwiEcSe9dY2sCpTqDZCIJidFSambbC9egJ5wG8qFGnK8ZAne35pnaMiMZApfqxJc75dqz6QeDZA13mmyNcM494kQwZDZD'
#weather api key
api_key = 'e548b4a25364c8e4b5ba829dac160f82'

#bot from pymessenger
bot = Bot(PAT)
#openweathermap [wrapper] object
owm = pyowm.OWM(api_key)

#τα γρηγορόκουμπα
quickButtons = [{
        'content_type': 'text',
        'title': 'Αθήνα',
        'payload': 'Στην αθήνα δεν έχω φίλους, μόνο γνωστούς'
    },
    {
        'content_type': 'text',
        'title': 'Σαλονίκη',
        'payload': 'Μου αρέσει να μυρίζω Θερμαικό Περπατώντας'
    }]
#Μια κλάση στα γρήγορα για το NotificationType
class NotificationType(Enum):
    regular = "REGULAR"
    silent_push = "SILENT_PUSH"
    no_push = "NO_PUSH"

@app.route('/', methods=['GET'])
def handle_verification():
    print ("Handling Verification.")
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        print ("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print ("Verification failed!")
        return ('Error, wrong validation token')

@app.route('/', methods=['POST'])
def handle_messages():
    print ("Handling Messages")
    #Παίρνει το μήνυμα που έστειλε ο χρήστης στο μποτ
    output = request.get_json()
    #data = json.loads(request.data.decode())
    print (output)
    send_quick_reply(bot, recipient_id, "Διαλέξτε πόλη ή μοιραστείται τοπ")
    #                    send_quick_reply(bot, recipient_id, "Διαλέξτε πόλη ή μοιραστείται τοποθεσία", quickButtons, notification_type = NotificationType.regular)

    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                #παίρνουμε το ID του χρήστη, έτσι ώστε να γνωρίζουμε που να στείλει μήνυμα πίσω το μποτάκι
                recipient_id = message['sender']['id']
                #το παρακάτω if είναι περιττό
                if message['message'].get('text'):
                    if str(output['entry'][0]['messaging'][0]['message']['text']) == 'Αθήνα':
                        print("Αλητεία εδώ ")
                        response_sent_text = get_message('Athens,GR')
                        send_message(recipient_id, response_sent_text)
                    elif output['entry'][0]['messaging'][0]['message']['text'] == 'Σαλονίκη':
                        print("Θερμαικό λιμάνι")
                        response_sent_text = get_message('Thessaloniki,GR')
                        send_message(recipient_id, response_sent_text)

                    #response_sent_text = get_message()
                    #send_message(recipient_id, response_sent_text)
                #μπορούμε να κάνουμε ένα έξτρα if, σε περπτωση όπου δεν στείλει απλώς κείμενο ο χρήστης :  .get('attachments') )

    ################
    return "Message Processed"

#παλιά μέθοδος
#def get_message():
#    sample_responses = ["Ο άνθρωπος δεν πάτησε πραγματικά στο φεγγάρι", "Το φορτηγό ήταν το καλύτερο αλμπουμ σου"]
#    return random.choice(sample_responses)

#Θα το κάνουμε να παίρνει τα στοιχεία του καιρού
def get_message(city):
    observation = owm.weather_at_place(city)
    weather_object = observation.get_weather()
    #print("Ο καιρός είναι = " , weather_object)

    temperatureJson = weather_object.get_temperature('celsius')

    #print("Ο καιρός σε βαθμούς κελσίου = " , temperatureJson)
    #print(temperatureJson['temp'])
    response = "Η θερμοκρασία αύτη την στιγμή είναι " + str(temperatureJson['temp']) + " . "
    return response


def send_quick_reply(Bot, recipient_id, message, buttons, notification_type = NotificationType.regular):
    #πρέπει το self να αναφέρεται στην κλάση bot / απλώς αλλάξε το self σε Bot
    return Bot.send_message(recipient_id, {
        'text': message,
        'quick_replies': buttons
        })



def send_message(recipient_id, response):
    #requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + PAT, json=payload)
    bot.send_text_message(recipient_id, response)
    return "success"


def send_get_started(bot, recipient_id):
    button = {
        "get_started":{
            "payload" : "first hand shake"
        }
    }

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run()
