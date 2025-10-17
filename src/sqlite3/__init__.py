import json
import time

def store_lyric_offline(artist: str | tuple, title: str, lyric_data: tuple | int, lang_code: str, sql_id: int =-1 ):
    current_timestamp = time.time()
    if isinstance(artist, tuple):
        artist = str(artist[0])
    synced_lyric_av = 1 if isinstance(lyric_data, tuple) else 0 if lyric_data == "404" else 2 
    if sql_id == -1:
        cursor.execute("INSERT INTO songs (title, artist, synced_lyric, available_translation, timestamp) VALUES (?, ?, ?, ?, ?)",(title, artist, synced_lyric_av, lang_code, current_timestamp))
        conn.commit()
        sql_id = cursor.lastrowid if cursor.lastrowid is not None else -1
    else:
        if synced_lyric_av == 1 and lang_code == "orig":
            cursor.execute("UPDATE songs SET synced_lyric=?, available_translation=?, timestamp=? WHERE id=?",(synced_lyric_av, "orig", time.time(), sql_id))
        else:
            cursor.execute("UPDATE songs SET timestamp=? WHERE id=?",(time.time(), sql_id))
        
        conn.commit()
        cursor.execute("SELECT available_translation FROM songs WHERE id=?", (sql_id,))
        cursor_languages = cursor.fetchone()
        if lang_code is not "orig":
            try:
                available_languages = json.loads(cursor_languages[0])
            except json.JSONDecodeError:
                """This error occurs when the column only contains a string. """
                available_languages = cursor_languages[0].split()
            if available_languages and lang_code not in available_languages:
                available_languages.append(lang_code)
                cursor.execute("UPDATE songs SET synced_lyric=?, available_translation=? WHERE id=?",(synced_lyric_av, json.dumps(available_languages, ensure_ascii=False, indent=4), sql_id))
                conn.commit()
            else:
                return sql_id
        
    if synced_lyric_av == 1:
        cursor.execute("SELECT id FROM lyrics WHERE song_id=? AND lang_code=?", (sql_id, lang_code))
        lyric_row = cursor.fetchone()
        if lyric_row:
            cursor.execute("UPDATE lyrics SET lyric=? WHERE id=?",(json.dumps(lyric_data, ensure_ascii=False, indent=4), lyric_row[0]))
            conn.commit()
        else:
            cursor.execute("INSERT INTO lyrics (song_id, lang_code, lyric) VALUES (?, ?, ?)",(sql_id, lang_code, json.dumps(lyric_data, ensure_ascii=False, indent=4)))
            conn.commit()
            
        return sql_id
    else:
        return -1
    
def sqlite3_request(artist: str | tuple, title: str, lang_code: str):
    if isinstance(artist, tuple):
        artist = str(artist[0])
    cursor.execute("SELECT id, synced_lyric, available_translation, timestamp FROM songs WHERE title=? AND artist=?", (title, artist))
    song_row = cursor.fetchone()
    if song_row and "1" in str(song_row[1]):
        if lang_code in song_row[2]:
            cursor.execute("SELECT lyric, lang_code FROM lyrics WHERE song_id=? AND lang_code=?", (song_row[0], lang_code))
        else:
            """The Database contains just the origin lyric instead of the requested translation"""
            cursor.execute("SELECT lyric, lang_code FROM lyrics WHERE song_id=? AND lang_code=?", (song_row[0], "orig"))

        conn.commit()
        lyric_row = cursor.fetchone()
        if lyric_row:
            lyric_data = json.loads(lyric_row[0])
            return song_row[0], lyric_row[1], tuple(lyric_data[1]), lyric_data[0] # OK


    elif song_row and str(song_row[1]) in ["0", "2"]:
        """It looks like there is no synced lyric available for this song. We will check again after 24 hours to see if lrclib has provided an update for it."""
        if song_row and (time.time() - float(song_row[3]) < 86400): # 86400 seconds = 1 day
            return -1, song_row[2], 404 if song_row[1] == "0" else 424, None # We use 404/424 as status code
        else:
            return song_row[0], song_row[2], 400 , None #We use 400 in Row 3 to trigger lrclib_api_request
        
    else:
        return -1, "orig", 400, None
    
    return -1, "orig", 5, None
        

if __name__ == "src.sqlite3":
    import sqlite3
    import os
    script_dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(script_dir + "/lyrics.db.lock"):
        with open(script_dir + "/lyrics.db.lock") as f:
            pid = int(f.read().strip())
            try:
                os.kill(pid, 0)
                offline_storage = False
                print("\033[31m!!! WARNING !!!\033[0m\n\nDatabase is currently in use by another process. Saving lyrics during this session is disabled.\n")
                input("Press Enter to continue...")
            except ProcessLookupError:
                offline_storage = True
    with open(script_dir + "/lyrics.db.lock", "w") as f:
        f.write(str(os.getpid()))
    conn = sqlite3.connect(script_dir + "/lyrics.db", timeout=10)
    cursor = conn.cursor()
    offline_usage = True