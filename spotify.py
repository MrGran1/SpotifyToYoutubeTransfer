from dotenv import load_dotenv
from requests import post, get 
import os
import base64
import json

load_dotenv()

playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DZ06evO0A8BTF?si=3465e2eca22b4df2"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    "ask for the spotify token and return it"
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}

    result = post(url,headers=headers,data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0 :
        print("No artist found")
        return None
    else :
        return (json_result[0]["id"])

def get_song_by_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=FR"
    headers = get_auth_headers(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
    

def get_playlist_id(link):
    link_token = link.split('/')
    playlist_id = link_token[4].split('?')[0]

    return (playlist_id)

def get_every_song(token,playlist_id):
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_headers(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)

    return(json_result)

def get_all_title(token, playlist_link):
    song_list = []
    playlist_id = get_playlist_id(playlist_link)
    songs = get_every_song(token,playlist_id)["items"]

    for song in songs : 
        string = song['track']['name'] + " - " + song['track']["artists"][0]['name']
        song_list.append(string)
    
    return song_list

def get_playlist_title(token,link):
    playlist_id = get_playlist_id(link)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_headers(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)
    return json_result['name']


token = get_token()

"""Tout les titres de la playlist """

print (get_playlist_title(token,playlist_link))

