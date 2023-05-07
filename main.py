from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import spotify as sp

credentials = None

if os.path.exists('token.pickle'):
    print('Loading credentials from file ...')
    with open('token.pickle',"rb") as token :
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube'
            ]
        )     
        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)


youtube = build('youtube', 'v3',credentials=credentials)

def create_playlist(name):
    request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet" : {
                "title" : name
            }
        }

    )
    request.execute()

def get_id_every_song(tab_songs):
    tabId = []
    for song in tab_songs:
        print ("song "+song)
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q = song
        )
        reponse = request.execute()
        tabId.append(reponse['items'][0]['id']['videoId'])
    return tabId
    
def add_to_playlist(tab_id,playlistId):
    for ide in tab_id:
         request = youtube.playlistItems().insert(
        body={
          "snippet": {
            "playlistId": "",
            "resourceId": {
              "videoId": ""
            }
          }
        }
    )   
    request.execute()

def main ():
    token = sp.get_token()
    link = "https://open.spotify.com/playlist/37i9dQZF1DZ06evO0A8BTF?si=3465e2eca22b4df2"


    create_playlist(sp.get_playlist_title(token,link))
    playlistId = sp.get_playlist_id(link)
    tabSong = sp.get_all_title(token,link)
    tabId = get_id_every_song(tabSong)
    add_to_playlist(tabId,playlistId)


main()
