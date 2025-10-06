import base64
import requests

def get_access_token(REFRESH_TOKEN: str, CLIENT_ID: str, CLIENT_SECRET: str):
    basic_auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("utf-8")
    params = {"grant_type": "refresh_token",
              "refresh_token": REFRESH_TOKEN
              }
    headers = {"Content-Type": "application/x-www-form-urlencoded", 
            "Authorization": f"Basic {basic_auth}"}
    try:
        response = requests.post("https://accounts.spotify.com/api/token", data=params, headers=headers)
        if response.status_code == 200:
            body = response.json()
            return body['access_token']
    except requests.exceptions.ConnectionError:
        return 200

    
def get_track_data(access_token: str):
    url = f"https://api.spotify.com/v1/me/player"
    header = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            body = response.json()
            return body
        else:
            """It could be that we need to refresh the token"""
            return 101
    except requests.exceptions.ConnectionError:
        return 200
