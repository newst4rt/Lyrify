import requests
import unicodedata

def lrclib_api_request(artist: str, title: str):
    """ Prepare for wide characters"""
    def is_cjk(ch):
        return unicodedata.east_asian_width(ch) in ("W", "F")

    """ Get Lyrics from lrclib.net """
    url = f"https://lrclib.net/api/get?artist_name={artist}&track_name={title}"
    header = {"User-Agent": "requests/*"}
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            body = response.json()
            if body["syncedLyrics"]:
                lyric_data = []
                w_chars = {0: 0}
                tmp_lyric_data = body["syncedLyrics"].split("\n")
                for x in range(0, len(tmp_lyric_data)):
                    if tmp_lyric_data[x].startswith("["):
                        sep_between_time_and_lyric = tmp_lyric_data[x].index("]")
                        time = tmp_lyric_data[x][0+1:sep_between_time_and_lyric].split(":")
                        lyric_line = tmp_lyric_data[x][sep_between_time_and_lyric+2:]
                        ms = int(float(time[0])*60*1000 + float(time[1])*1000)
                        if lyric_line == "":
                            lyric_line = "♬"
                        else:
                            if (cjk_count := sum(1 for ch in lyric_line if is_cjk(ch))):
                                w_chars[x + 1] = cjk_count

                        lyric_data.append({"startTimeMs": ms, "lyric_line": lyric_line.strip()})

                if 0 != int(lyric_data[0]["startTimeMs"]):
                    lyric_data.insert(0, {"startTimeMs": 0, "lyric_line": "♬"})

                return (w_chars, tuple(lyric_data))
            else:
                return 422 # 422 represent a successful request with some available data but no synced lyric. 
        else: #404
            if response.status_code:
                return response.status_code # No data available for the requested track
            else:
                return 4
            
    except requests.exceptions.ConnectionError:
        """It looks like there is no internet connection. We will try it later again."""
        return 503

def lrclib_api(artist: str | tuple, title: str):
    if isinstance(artist, tuple) and len(artist) > 1:
        lrclib_request = lrclib_api_request(",".join(artist), title)
        if isinstance(lrclib_request, tuple):
            return lrclib_request
        else:
            artist = str(artist[0])
            
    
    return lrclib_api_request(artist, title)
    
