import requests
import os
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) 

client_id = os.getenv('id')
client_secret = os.getenv('secret')
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


BASE_URL = 'https://api.spotify.com/v1/browse/new-releases'

r = requests.get(BASE_URL,
                        headers=headers,
                        params=params)
                        
d = r.json()
track = []
for album in d['albums']['items']:
    track.append(album['name'])
    
"""
for i in range(len(d['albums']['items'])):
    track[i] = d[i]['albums']['items']['name']
"""

@app.route('/')
def hello_world():
    print('updated')
    return render_template(
        "index.html",
        len = len(track), track = track,
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)