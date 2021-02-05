import requests
import os
import random
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) 

client_id = os.getenv('id')
client_secret = os.getenv('secret')
#Drake, Eminime, weekend
#artist_id = ['3TVXtAsR1Inumwj472S9r4', '7dGJo4pcD2V6oG8kP0tJRR', '1Xyo4u8uXC1ZmMpatF05PJ']
artist_id = ['72beYOeW2sb2yfcS4JsRvb','69GGBxA162lTqCwzJG5jLp', '0KNIXlZbeaDBiaKIjNN8Gr']
random_artist = random.randint(0,2)
random_track = random.randint(0, 9)
app = Flask(__name__)


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']
#print(access_token)


headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


params={'limit': 10,
        'country':'US'
        }


BASE_URL = 'https://api.spotify.com/v1/artists/' + artist_id[random_artist] + '/top-tracks'

r = requests.get(BASE_URL,
                        headers=headers,
                        params=params)

d = r.json()
#print(d)

#track = d['tracks'][random_track]['name']
track = d['tracks'][random_track]
track_ids = track['id']
#print("track_ids: " + track_ids)

TRACK_URL = 'https://api.spotify.com/v1/tracks?ids='+track_ids 

ids={'ids':track_ids}

s = requests.get(TRACK_URL,
                headers=headers
                )

#print(s)
audio = s.json()
#print(audio)
audio = audio['tracks'][0]['preview_url']
#print(audio)

"""
for song in d['tracks']:
    track.append(album['name'])
""" 

@app.route('/')
def hello_world():
    print('updated')
    return render_template(
        "index.html",
        len = len(track), track=track,
        audio=audio
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)