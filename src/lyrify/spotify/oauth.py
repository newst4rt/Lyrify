import http.server
import socketserver
import urllib.parse
import webbrowser
import base64
import requests


class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        if "code" in query:
            SpotifyAuthHandler.auth_code = query["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Successful!</h1><p>You can close the window now.</p>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h1>Error</h1><p>Something went wrong.</p>")
            exit()

def request_user_authorization(CLIENT_ID: str, REDIRECT_URI: str) -> str:
    query_string = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-currently-playing user-read-playback-state"
    }
    auth_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_string)

    port = int(REDIRECT_URI.split(":")[2].split("/")[0])
    with socketserver.TCPServer(("", port), SpotifyAuthHandler) as httpd:
        print(f'Open Spotify Login in the Browser ...')
        #httpd.timeout = 15
        webbrowser.open(auth_url)
        httpd.handle_request()
        return str(SpotifyAuthHandler.auth_code)


def get_tokens(auth_code: str, CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str) -> tuple|int:
    basic_auth = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode("utf-8")
    params = {"code": auth_code,
              "redirect_uri": REDIRECT_URI,
              "grant_type": "authorization_code"}
    headers = {"Content-Type": "application/x-www-form-urlencoded", 
            "Authorization": f'Basic {basic_auth}'}

    response = requests.post("https://accounts.spotify.com/api/token", data=params, headers=headers)
    if response.status_code == 200:
        body = response.json()
        return body["access_token"], body.get("refresh_token")
    else:
        return response.status_code
    
def init():
        print("Follow this instruction:\n")
        print("1. Go to https://developer.spotify.com/dashboard/applications")
        print("2. Create an App (if you haven't already)")
        print("3. Go to your App -> Basic Information\n")
        CLIENT_ID = input("Client ID: ")
        CLIENT_SECRET = input("Client Secret: ")
        REDIRECT_URI = input("Redirect URI (e.g. http://127.0.0.1:8000/callback): ")
        user_auth_token = request_user_authorization(CLIENT_ID, REDIRECT_URI)
        tokens = get_tokens(user_auth_token, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI) # type: ignore
        if isinstance(tokens, tuple):
            access_token, REFRESH_TOKEN = tokens
            if access_token is not None or REFRESH_TOKEN is not None:
                with open(".env", "w") as f:
                    f.write(f'CLIENT_ID = "{CLIENT_ID}"\n')
                    f.write(f'CLIENT_SECRET = "{CLIENT_SECRET}"\n')
                    f.write(f'REDIRECT_URI = "{REDIRECT_URI}"\n')
                    f.write(f'REFRESH_TOKEN = "{REFRESH_TOKEN}"\n')
                    print("Authentication succeeded.")
                    exit()
            else:
                print("Something went wrong. Please try again.")
                exit()
        
        else: # Raise error
            print(f'HTTP Error: {tokens}')
            exit()