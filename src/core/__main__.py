from src.lyric_providers.lrclib import *
import src.core.config as config
if config.offline_storage is True:
        from src.sqlite3 import store_lyric_offline
if config.offline_usage is True:
        from src.sqlite3 import sqlite3_request


def get_lyric(artist: str | tuple | None, title: str | None, dest_lang: str, track_len: int | float):
    if artist is None or title is None:
        return -1, dest_lang, 6, None
    
    sql_id = -1
    if config.offline_usage:
        sql_id, lang_code, lyric_data, w_chars = sqlite3_request(artist, title, dest_lang, track_len)
        #if lyric_data and not isinstance(lyric_data, int):
        if lyric_data not in (400,):
           return sql_id, lang_code, lyric_data, w_chars
        
    # lyric_data = lrclib_request[1], w_chars = lrclib_request[0], duration = lrclib_request[2]
    lrclib_request = lrclib_api(artist, title, track_len)
    if config.offline_storage and lrclib_request not in (503,):
        sql_id = store_lyric_offline(artist, title, lrclib_request, "orig", sql_id if sql_id else -1)

    if isinstance(lrclib_request, tuple):
        return sql_id, "orig", lrclib_request[1], lrclib_request[0]
            
    return -1, "orig", lrclib_request, None
    
def get_syncedlyric_index(lyric_data: tuple, time_pos: float):
    len_ly = len(lyric_data)
    for x in range(0, len_ly):
        if time_pos >= int(lyric_data[x]["startTimeMs"]):
            if x == len_ly-1 or time_pos <= int(lyric_data[x+1]["startTimeMs"]):
                return x