import base64
import requests
from .api_init import *

def get_track_data(past_id: str | int | None):
    global access_token
    url = f"https://api.spotify.com/v1/me/player"
    for _ in range(0, 2):
        try:
            header = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                body = response.json()
                id = str(body["item"]["id"])
                if past_id != id:
                    artist = []
                    for x in body["item"]["artists"]:
                        artist.append(str(x["name"]).replace(" ", "+"))
                    title = str(body["item"]["name"])
                    return str(body["item"]["id"]), float(body["progress_ms"]), float(body["item"]["duration_ms"]), tuple(artist), str(title.replace(" ", "+"))
                else:
                    return str(body["item"]["id"]), float(body["progress_ms"])
            elif response.status_code == 204:
                return 204
            else:
                """It could be that we need to refresh the token"""
                access_token = get_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
                if access_token == None: 
                    return 401
                else:
                    continue

        except requests.exceptions.ConnectionError:
            return 503
    
    else:
        return 401


