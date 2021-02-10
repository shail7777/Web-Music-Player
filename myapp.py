import requests
import os
import random
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) 

client_id = os.getenv('id')
client_secret = os.getenv('secret')
client_id_genius = os.getenv('client_id_genius')
client_secret_genius = os.getenv('client_secret_genius')
access_token_genius = os.getenv('access_token_genius')

artist_id = [
            '72beYOeW2sb2yfcS4JsRvb',
            '69GGBxA162lTqCwzJG5jLp', 
            '0KNIXlZbeaDBiaKIjNN8Gr']

random_artist = random.randint(0,2)
random_track = random.randint(0, 9)
app = Flask(__name__)

def getlyrics(song_name, artist_name):
    GENIUS_URL = "https://api.genius.com/search?q=" + song_name
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token_genius)
        
    }  
    response = requests.get(GENIUS_URL,
                      headers=headers
                      )
    response = response.json()
    length = len(response['response']['hits'])
    
    
    for i in range(length):
        genius_artist = response['response']['hits'][i]['result']['primary_artist']['name']
        title = response['response']['hits'][i]['result']['title']
        #print("title: " + title)
        #print("genius_artist: " + genius_artist)
        
        if artist_name in genius_artist:
            if song_name in title:
                return response['response']['hits'][i]['result']['url']
        else:
            continue
    return "none"



AUTH_URL = 'https://accounts.spotify.com/api/token'

"""
GENIUS_AUTH_URL = "https://api.genius.com/oauth/token"
auth_genius = requests.get(GENIUS_AUTH_URL,{
                            'client_id': client_id_genius,
                            'client_secret': client_secret_genius,
                            #'response_type': 'code',
                            'grant_type': 'authorization_code'
                            })
token_genius = auth_genius.json()
print(token_genius)
access_token_genius = token_genius['access_token']
"""

# POST
auth_response = requests.post(AUTH_URL, {
                                'grant_type': 'client_credentials',
                                'client_id': client_id,
                                'client_secret': client_secret,})


auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

params={'limit': 10,
        'country':'US'
        }

BASE_URL = 'https://api.spotify.com/v1/artists/' + artist_id[random_artist] + '/top-tracks'

r = requests.get(BASE_URL,
                    headers=headers,
                    params=params
                    )

d = r.json()
track = d['tracks'][random_track]
track_ids = track['id']

TRACK_URL = 'https://api.spotify.com/v1/tracks?ids='+track_ids 

s = requests.get(TRACK_URL,
                headers=headers
                )

audio = s.json()
audio = audio['tracks'][0]['preview_url']

#print("track_name: " + track['name'] )
#print("artist_name: " + track['artists'][0]['name'])
lyrics_url = getlyrics(track['name'], track['artists'][0]['name'])


@app.route('/')
def hello_world():
    print('updated')
    return render_template(
        "index.html",
        len = len(track), track=track,
        audio=audio,
        lyrics_url=lyrics_url
    )
    
app.run(
        port=int(os.getenv('PORT', 8080)),
        host=os.getenv('IP', '0.0.0.0'),
        debug=True
    )