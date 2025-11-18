import json
import time
import sqlite3
import os
from src.core.config import config

class Database_Manager():

    def __init__(self):

        _dir = os.path.dirname(os.path.realpath(__file__))
        try:
            with open(_dir + "/lyrics.db.lock", "r") as f:
                pid = int(f.read().strip())
                if config.os == "Linux":
                    if os.path.exists("/proc/" + str(pid)):
                        with open("/proc/" + str(pid) + "/comm", "r") as _f:
                            comm = _f.read().strip()
                            if not comm == "python3":
                                with open(_dir + "/lyrics.db.lock", "w"):
                                    raise ProcessLookupError
                    else:
                        os.kill(pid, 0) # Check if process exist by sending a test signal
                    
                elif config.os == "Windows":
                    import subprocess
                    _out = subprocess.check_output(["tasklist", "/FI", f"PID eq {pid}"])
                    if str(pid) not in str(_out):
                        raise ProcessLookupError
                elif config.os == "Darwin":
                    os.kill(pid, 0)
                    
                config.offline_storage = False
                if config.terminal_mode == "Default":
                    print("\033[93:1m WARNING \033[0m: database is currently in use by another process. Saving lyrics during this session is disabled.\n")
                    input("Press Enter to continue...\n")
        except (ProcessLookupError, FileNotFoundError):
            config.offline_storage = True
            with open(_dir + "/lyrics.db.lock", "w") as f:
                f.write(str(os.getpid()))

        self.conn = sqlite3.connect(_dir + "/lyrics.db", timeout=10)
        config.offline_usage = True

    def __del__(self):
        self.conn.close()


    def store_lyric_offline(self, artist: str | tuple, title: str, lyric_data: tuple | int, lang_code: str, sql_id: int =-1 ) -> int:
        try:
            cursor = self.conn.cursor()
            current_timestamp = time.time()
            if isinstance(artist, tuple):
                artist = str(artist[0])
            synced_lyric_av = 1 if isinstance(lyric_data, tuple) else 0 if lyric_data == 404 else 2 
            if sql_id == -1:
                cursor.execute("INSERT INTO songs (title, artist, synced_lyric, available_translation, track_duration, timestamp) VALUES (?, ?, ?, ?, ?, ?)",(title, artist, synced_lyric_av, lang_code, lyric_data[2] if isinstance(lyric_data, tuple) else 0, current_timestamp))
                sql_id = cursor.lastrowid if cursor.lastrowid is not None else -1
            else:
                if synced_lyric_av == 1 and lang_code == "orig":
                    cursor.execute("UPDATE songs SET synced_lyric=?, available_translation=?, timestamp=? WHERE id=?",(synced_lyric_av, "orig", time.time(), sql_id))
                else:
                    cursor.execute("UPDATE songs SET timestamp=? WHERE id=?",(time.time(), sql_id))
                
                cursor.execute("SELECT available_translation FROM songs WHERE id=?", (sql_id,))
                cursor_languages = cursor.fetchone()
                if lang_code != "orig":
                    if cursor_languages and "," in cursor_languages[0]:
                        """The row `available_translation` contains multiple values in a pseudo list"""
                        available_languages = json.loads(cursor_languages[0]) # convert pseudo list to list 
                    else:
                        """The row contains just one value."""
                        available_languages = cursor_languages[0].split()
                    
                    if available_languages and lang_code not in available_languages:
                        available_languages.append(lang_code)
                        cursor.execute("UPDATE songs SET synced_lyric=?, available_translation=? WHERE id=?",(synced_lyric_av, json.dumps(available_languages, ensure_ascii=False, indent=4), sql_id))
                    else:
                        return sql_id
                    
            if synced_lyric_av == 1:
                cursor.execute("SELECT id FROM lyrics WHERE song_id=? AND lang_code=?", (sql_id, lang_code))
                lyric_row = cursor.fetchone()
                if lyric_row:
                    cursor.execute("UPDATE lyrics SET lyric=? WHERE id=?",(json.dumps(lyric_data, ensure_ascii=False, indent=4), lyric_row[0]))
                else:
                    cursor.execute("INSERT INTO lyrics (song_id, lang_code, lyric) VALUES (?, ?, ?)",(sql_id, lang_code, json.dumps(lyric_data[0:2], ensure_ascii=False, indent=4))) # type: ignore
                    
                return sql_id
            else:
                return -1
        finally:
            self.conn.commit()
            cursor.close()
        
    def sqlite3_request(self, artist: str | tuple, title: str, lang_code: str, track_len: int | float) -> tuple:
        try:
            cursor = self.conn.cursor()
            if isinstance(artist, tuple):
                artist = str(artist[0])
            cursor.execute("SELECT id, synced_lyric, available_translation, track_duration, timestamp FROM songs WHERE title=? AND artist=?", (title, artist))
            song_row = cursor.fetchone()
            if song_row and "1" in str(song_row[1]):
                if lang_code in song_row[2]:
                    cursor.execute("SELECT lyric, lang_code FROM lyrics WHERE song_id=? AND lang_code=?", (song_row[0], lang_code))
                else:
                    """The Database contains just the origin lyric instead of the requested translation"""
                    cursor.execute("SELECT lyric, lang_code FROM lyrics WHERE song_id=? AND lang_code=?", (song_row[0], "orig"))

                lyric_row = cursor.fetchone()
                if lyric_row:
                    lyric_data = json.loads(lyric_row[0])
                    """delta = abs(float(song_row[3]) - track_len/1000)
                    if delta > 1 or delta < -1:
                        #The duration difference is too high. We consider this as a wrong match.
                        return song_row[0], lyric_row[1], 6, None"""
                        
                    return song_row[0], lyric_row[1], tuple(lyric_data[1]), {int(k): v for k, v in lyric_data[0].items()} # OK


            elif song_row and str(song_row[1]) in ["0", "2"]:
                """It looks like there is no synced lyric available for this song. We will check again after 24 hours to see if lrclib has provided an update for it."""
                if song_row and (time.time() - float(song_row[3]) < 86400): # 86400 seconds = 1 day
                    return -1, song_row[2], 404 if song_row[1] == "0" else 424, None # We use 404/424 as status code
                else:
                    return song_row[0], song_row[2], 400 , None # We use 400 in Row 3 to trigger lrclib_api_request
                
            else:
                return -1, "orig", 400, None
            
            return -1, "orig", 5, None
        
        finally:
            self.conn.commit()
            cursor.close()
        

db_manager = Database_Manager()