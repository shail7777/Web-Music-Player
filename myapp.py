import requests
import os
import random
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) 

client_id = os.getenv('id')
client_secret = os.getenv('secret')
access_token_genius = os.getenv('access_token_genius')
matcher_api_token = os.getenv('matcher_api_token')

artist_id = ['72beYOeW2sb2yfcS4JsRvb',
            '69GGBxA162lTqCwzJG5jLp', 
            '0KNIXlZbeaDBiaKIjNN8Gr']

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
        if artist_name in genius_artist:
            if song_name in title:
                return response['response']['hits'][i]['result']['url']
        else:
            continue
        
    return "none"

def matcher_api(song_name, artist_name):
    URL = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=json&callback=callback'
    
    params={'q_track':song_name,
            'q_artist':artist_name,
            'apikey':matcher_api_token
            }
            
    r = requests.get(URL,
                    params=params
                    )
                
    r = r.json()
    status = r['message']['header']['status_code']
    
    if status == 200:
        return r['message']['body']['lyrics']['lyrics_body'].split("\n")
    else:
        return 'none'


def spotify_api(client_id, client_secret):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    random_artist = random.randint(0,2)
    random_track = random.randint(0, 9)
    auth_response = requests.post(AUTH_URL, {
                                'grant_type': 'client_credentials',
                                'client_id': client_id,
                                'client_secret': client_secret})
    
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
    return track, audio

@app.route('/')
def hello_world():
    track, audio = spotify_api(client_id,client_secret)
    lyrics_url = getlyrics(track['name'], track['artists'][0]['name'])
    lyrics_text = matcher_api(track['name'], track['artists'][0]['name'])
    
    print('updated')
    return render_template(
        "index.html",
        len = len(track), track=track,
        audio=audio,
        lyrics_url=lyrics_url,
        lyrics_text=lyrics_text,
        len_lyrics=len(lyrics_text)
    )
    
app.run(
        port=int(os.getenv('PORT', 8080)),
        host=os.getenv('IP', '0.0.0.0'),
        debug=True
    )