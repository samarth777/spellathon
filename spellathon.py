# import all modules
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random
from twilio.rest import Client

app = Flask(__name__)


l=[]
# dictionary to store user words key = number, value = list of words
users=dict()

# todays image
image = 'https://i.imgur.com/sIn58e7.png'

@app.route("/")
def hello():
    return "Hello, World!"

# main function
@app.route("/spell", methods=['POST'])
def spell():
    global l
    # todays answers
    ans = ['gosh', 'song', 'nosh', 'tong', 'host', 'shot', 'snot', 'nous', 'onus', 'gout', 'thou', 'unto', 'oust', 'thong', 'ghost', 'sough', 'ought', 'tough', 'gusto', 'shout', 'south', 'snout', 'shogun', 'nought', 'sought', 'gunshot', 'shotgun']

    # Fetch the message
    msg = request.form.get('Body').lower()
    sender = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    send = resp.message()

    if msg == 'hi':
        send.body('''*Welcome to Spellathon!*

Find words that fulfill these conditions.
See how many you can guess!

 1. Find all the words of four or
    more letters from the letters
    shown in the puzzle.

 2. In making a word, each letter
    may be used once only.
    Each word must contain the
    central letter.

 3. There should be atleast one
    seven letter word.
    Plurals, foreign words and
    proper names are not allowed.

Message 'play' to begin...
        ''')

    elif msg == 'play':

        users[sender] = []

        send.media(image)
        send.body('Start sending the words!  Once you have sent all the words, send "done" to end the game.')

    #append the words to the value list of the sender
    elif msg in ans:
        l.append(msg)
        users[sender].append(msg)

    elif len(msg)<4:
        send.body('Word must be atleast 4 letters long!')

    elif msg.isalpha()==False:
        send.body('Word must be alphabetic!')

    elif msg == 'done':

        send.body('''
*Thanks for playing!*

You got *{}* words right out of *{}*!

The words were: *{}*

The words you got right were: *{}*

Your score is: *{} %*

Created by: Samarth
https://linktr.ee/samarth.p
'''.format(len(set(users[sender])), len(ans), ', '.join(ans), ', '.join(set(users[sender])),round(((len(set(users[sender]))/len(ans))*100))))
        l=[]
        users.pop(sender)

    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)