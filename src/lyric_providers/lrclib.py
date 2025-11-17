import requests
import unicodedata

def lrclib_api_request(artist: str, title: str, track_len: int | float) -> tuple|int:
    """ Prepare for wide characters"""
    def is_cjk(ch) -> bool:
        return unicodedata.east_asian_width(ch) in ("W", "F")

    """ Get Lyrics from lrclib.net """
    url = f"https://lrclib.net/api/get?artist_name={artist}&track_name={title}"
    header = {"User-Agent": "requests/*"}
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            body = response.json()
            if body["syncedLyrics"]:
                """d_delta = abs(body["duration"] - track_len/1000)
                if track_len and d_delta > 9 or d_delta < -9:
                    #The duration difference is too high. We consider this as a wrong match.
                    return 6 """
                lyric_data = []
                w_chars = {0: 0}
                tmp_lyric_data = body["syncedLyrics"].split("\n")
                for x in range(0, len(tmp_lyric_data)):
                    if tmp_lyric_data[x].startswith("["):
                        delimeter = tmp_lyric_data[x].index("]")
                        time = tmp_lyric_data[x][1:delimeter].split(":")
                        lyric_line = tmp_lyric_data[x][delimeter+2:]
                        ms = int(float(time[0])*60*1000 + float(time[1])*1000)
                        if lyric_line == "":
                            lyric_line = "♬"
                        else:
                            if (cjk_count := sum(1 for ch in lyric_line if is_cjk(ch))):
                                w_chars[x + 1] = cjk_count
                            if not w_chars[0] and lyric_line.isascii() == False and lyric_line.isalpha():
                                w_chars[0] = 1

                        lyric_data.append({"startTimeMs": ms, "lyric_line": lyric_line.strip()})

                if 0 != int(lyric_data[0]["startTimeMs"]):
                    lyric_data.insert(0, {"startTimeMs": 0, "lyric_line": "♬"})

                return (w_chars, tuple(lyric_data), body["duration"])
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

def lrclib_api(artist: str | tuple, title: str, track_len: int | float) -> tuple|int:
    if isinstance(artist, tuple) and len(artist) > 1:
        lrclib_request = lrclib_api_request(",".join(artist), title, track_len)
        if isinstance(lrclib_request, tuple):
            return lrclib_request
        else:
            artist = artist[0]
    
    return lrclib_api_request(artist, title, track_len)
    
