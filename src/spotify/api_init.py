import base64
import requests

CLIENT_ID = None
CLIENT_SECRET = None
REDIRECT_URI = None
REFRESH_TOKEN = None
access_token = None

def get_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET):
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
        return 503
    
def check_credentials():
    global CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, REFRESH_TOKEN, access_token
    try:
        with open(".env") as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=', 1)
                value = value.strip().strip('"').strip("'")
                globals()[key.strip()] = value.strip()
    except FileNotFoundError:
        pass

    if CLIENT_ID is None or CLIENT_SECRET is None or REDIRECT_URI is None or REFRESH_TOKEN is None:
        print("It looks like you didn't configured the Spotify API yet.")
        exit()
    else:
        access_token = get_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)

    
if __name__ == "src.spotify.api_init":
    check_credentials()