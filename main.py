from dotenv import load_dotenv
import os
from requests import post, get

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}
    response = (post(url, headers = headers, data=data)).json()
    auth_header = {"Authorization" : "Bearer " + response['access_token']}
    return auth_header

def search_artist(token_response, artist_name):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url+query

    response = (get(query_url,headers=token_response)).json()

    if len(response["artists"]["items"]) == 0:
        print("No artist found")
        return None
    return  response["artists"]["items"][0]["id"]

def get_song_by_artist(token_response, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    response = (get(url,headers=token_response)).json()
    if "items" in response:
        album_names = [item["name"] for item in response["items"]]
        return album_names
    else:
        print("No 'items' key found in the response.")
        return None

artist_name = input("Enter the artist name: ")

token_response = get_token()
artist_id = search_artist(token_response, artist_name)
albums = get_song_by_artist(token_response, artist_id)
if albums:
    print("Album Names:")
    for name in albums:
        print(name)
        print("k")