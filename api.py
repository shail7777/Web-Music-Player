from os import environ
from random import choice
from requests import get, post

AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_access_token():
    """Fetch Spotify access token via POST request"""

    spotify_client_id = '718ff348ee184d9ba08c44d01f310e30'
    spotify_client_secret = '3cea5ecc418d40a9926fc32ab2b17072'

    auth_response = post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': spotify_client_id,
        'client_secret': spotify_client_secret,
    })

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']
