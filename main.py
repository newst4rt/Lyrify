#!/usr/bin/env python
import time
import dbus
import requests
import json
import argparse
from rich_argparse import RichHelpFormatter
import asyncio
from googletrans import Translator
import unicodedata

CLIENT_ID = None
CLIENT_SECRET = None
REDIRECT_URI = None
REFRESH_TOKEN = None
access_token = None

max_lyric_line_len = 60
old_text = ""
old_lyric_index = -1
old_terminal_size = -1
old_track_id = -1

def c_print(text):
    global max_lyric_line_len, old_text
    if setting_c_print == "stream":
        if text == old_text:
            return
        print(f'{text}\n')
        old_text = text
    elif setting_c_print == "interactive":
        len_text = len(text)
        if len_text < max_lyric_line_len:
            print(" "*max_lyric_line_len, end="\r", flush=True)
        
        print(f'{text[:max_lyric_line_len]}', end="\r", flush=True)
        max_lyric_line_len = len_text


#highlight_color #17ff17 , passed_color #6c6c6c
def d_print(lyric_data, w_chars, lyric_index, track_id, highlight_color=(23, 255, 23), passed_lyric_color=(108, 108, 108)):
  
    global old_lyric_index, old_terminal_size, old_track_id
    highlight_color = f"\033[38;2;{highlight_color[0]};{highlight_color[1]};{highlight_color[2]}m"
    passed_lyric_color = f"\033[38;2;{passed_lyric_color[0]};{passed_lyric_color[1]};{passed_lyric_color[2]}m"
    terminal_size = shutil.get_terminal_size()
    terminal_columns = terminal_size.columns
    max_lines_in_a_window = terminal_size.lines / 2
    max_range = lyric_index+int(max_lines_in_a_window/2)
    if lyric_index != old_lyric_index or terminal_size != old_terminal_size or track_id != old_track_id:
        old_lyric_index = lyric_index # In order to avoid unnecessary screen refreshes
        old_terminal_size = terminal_size # In order to execute a screen refresh when the terminal size has changed
        max_len = len(lyric_data)
        if terminal_size.lines % 4 == 3 or terminal_size.lines % 4 == 2:
            max_range += 1

        os.system('clear')
        for x in range(lyric_index-int(max_lines_in_a_window/2), max_range):
            if x >= max_len:
                break
            if x < 0:
                print("\n".center(terminal_size.columns))
                continue
            if x in w_chars:
                w_charc = w_chars[x]
            else:
                w_charc = 0

            if x == lyric_index:
                print(f"{highlight_color}{lyric_data[x]["lyric_line"].center(terminal_size.columns-w_charc)}\033[0m")                
            elif x < lyric_index:
                print(f"{passed_lyric_color}{lyric_data[x]["lyric_line"].center(terminal_size.columns-w_charc)}\033[0m")
            else:
                print(lyric_data[x]["lyric_line"].center(terminal_size.columns-w_charc))
            print("\n", end="")

def error_print(text):
    def e_print(text):
        terminal_size = shutil.get_terminal_size()
        os.system('clear')
        for x in range(0, terminal_size.lines-2):
            if x == int(terminal_size.lines/2)+1:
                print(f"{text.center(terminal_size.columns)}")
            else:
                print("")

    if text == 422:
        if setting_c_print == "default":
            e_print("🔴 422 🔴") # There are partial data available at lrclib, but no synced lyrics for this song.
        else:
            c_print("🔴")

    elif text == 404:
        if setting_c_print == "default":
            e_print("❌ 404 ❌") #No lyrics available at lrclib for this song.
        else:
            c_print("❌")
    
    elif text == 400:
        if setting_c_print == "default":
            e_print("❌ 400 ❌") #There are no synced lyrics in our sqlite3 database available.
        else:
            c_print("❌")

    elif text == 200:
        if setting_c_print == "default":
            e_print("🚫 200 🚫") #No internet connection available 
        else:
            c_print("🚫")

    else:
        if setting_c_print == "default":
            e_print(text) #No internet connection available 
        else:
            c_print(text)



def get_track_data(player_metadata, setting_mode):
    if setting_mode == "dbus":
        player_metadata_track = player_metadata.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        ix = str(player_metadata_track["mpris:trackid"]).rindex("/")
        artist = str(player_metadata_track["xesam:artist"][0])
        title = str(player_metadata_track["xesam:title"])
        track_len = float(player_metadata_track["mpris:length"]) #microseconds
        position_µs = float(player_metadata.Get("org.mpris.MediaPlayer2.Player", "Position")) #microseconds
        if track_len == position_µs:
            raise Exception(f"The current player {dbus_player} is not supported. There is an issue with getting the current track position.")
        return str(player_metadata_track["mpris:trackid"][ix+1:]), artist.replace(" ", "+"), title.replace(" ", "+"), float(position_µs / 1_000.0), float(track_len / 1_000.0)
    
    elif setting_mode == "spotify-api":
        global access_token
        track_data = get_track.get_track_data(access_token)
        if track_data == 101:
            access_token = get_track.get_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
            track_data = get_track.get_track_data(access_token)
            if track_data == 101:
                print("!!! ERROR !!!\n\nCould not refresh the access token. Try again or use --init spotify.")
                exit()
        elif track_data["item"]:
            artist = str(track_data["item"]["artists"][0]["name"])
            title = str(track_data["item"]["name"])
            return str(track_data["item"]["id"]), artist.replace(" ", "+"), title.replace(" ", "+"), float(track_data["progress_ms"]), float(track_data["item"]["duration_ms"])
        elif track_data == 200:
            print("🚫 ERROR 🚫\n\nNo internet connection available.")
            exit()


def lrclib_api_request(artist, title):
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
                            cjk_count = sum(1 for ch in lyric_line if is_cjk(ch))
                            if cjk_count > 0:
                                w_chars[x+1] = cjk_count

                        lyric_data.append({"startTimeMs": ms, "lyric_line": lyric_line})

                if 0 != int(lyric_data[0]["startTimeMs"]):
                    lyric_data.insert(0, {"startTimeMs": 0, "lyric_line": "♬"})

                return [w_chars, lyric_data]
            else:
                return 422 # 422 represent a successful request with some available data but no synced lyric. 
        elif response.status_code == 404:
            return 404 # No data available for the requested track
        
    except requests.exceptions.ConnectionError:
        """It looks like there is no internet connection. We will try it later again."""
        return 200
    
def sqlite3_request(artist, title, lang_code):
        cursor.execute("SELECT id, synced_lyric, available_translation, timestamp FROM songs WHERE title=? AND artist=?", (title, artist))
        song_row = cursor.fetchone()
        if song_row and "1" in str(song_row[1]) and lang_code in song_row[2]:
            cursor.execute("SELECT lyric FROM lyrics WHERE song_id=? AND lang_code=?", (song_row[0], lang_code))
            lyric_row = cursor.fetchone()
            if lyric_row:
                return song_row[0], song_row[2], (json.loads(lyric_row[0]))
        elif song_row and "0" in str(song_row[1]):
            """It looks like there is no synced lyric available for this song. We will check again after 24 hours to see if lrclib has provided an update for it."""
            if song_row and (time.time() - float(song_row[3]) < 86400): # 86400 seconds = 1 day
                return -1, song_row[2], 400
            else:
                lrclib_request = lrclib_api_request(artist, title)
                if offline_storage and lrclib_request not in (200,):
                    cursor.execute("UPDATE songs SET timestamp=? WHERE id=?",(time.time(), song_row[0]))
                    conn.commit()
                    if lrclib_request not in (404, 422):
                        cursor.execute("INSERT INTO lyrics (song_id, lang_code, lyric) VALUES (?, ?, ?, ?)",(song_row[0], "orig", json.dumps(lrclib_request, ensure_ascii=False, indent=4)))
                        conn.commit()

                return song_row[0], "orig", lrclib_request
        else:
            return -1, None, None
    
def store_lyric_offline(artist, title, lyric_data, lang_code, sql_id=-1):
    current_timestamp = time.time()
    if sql_id == -1:
        cursor.execute("INSERT INTO songs (title, artist, synced_lyric, available_translation, timestamp) VALUES (?, ?, ?, ?, ?)",(title, artist, "0" if lyric_data in (404, 422) else "1", lang_code, current_timestamp))
        conn.commit()
        sql_id = cursor.lastrowid
    else:
        cursor.execute("SELECT available_translation FROM songs WHERE id=?", (sql_id,))
        available_languages = cursor.fetchone()[0].split()
        if available_languages and lang_code not in available_languages:
            available_languages.append(lang_code)
            cursor.execute("UPDATE songs SET synced_lyric=?, available_translation=?, timestamp=? WHERE id=?",("0" if lyric_data in (404, 422) else "1", json.dumps(available_languages, ensure_ascii=False, indent=4), current_timestamp, sql_id))
        else:
            return
        
    if lyric_data not in (404, 422):
        cursor.execute("INSERT INTO lyrics (song_id, lang_code, lyric) VALUES (?, ?, ?)",(sql_id, lang_code, json.dumps(lyric_data, ensure_ascii=False, indent=4)))
        conn.commit()
        return sql_id
    else:
        return -1
    
def get_lyric(artist, title, dest_lang):
    if offline_usage:
        sql_id, lang_code, offline_data = sqlite3_request(artist, title, dest_lang)
        if offline_data:
           return sql_id, lang_code, offline_data[1], offline_data[0]
        
    lrclib_request = lrclib_api_request(artist, title)
    if offline_storage and lrclib_request[1] not in (200,):
        sql_id = store_lyric_offline(artist, title, lrclib_request, dest_lang)
        return sql_id, "orig", lrclib_request[1], lrclib_request[0]
    elif lrclib_request not in (404, 400, 422):
        return -1, None, lrclib_request[1], lrclib_request[0]
        
    return -1, None, lrclib_request, None
    
    

def get_syncedlyric_index(lyric_data, time_pos):
    len_ly = len(lyric_data)
    for x in range(0, len_ly):
        if time_pos >= int(lyric_data[x]["startTimeMs"]):
            if x == len_ly-1 or time_pos <= int(lyric_data[x+1]["startTimeMs"]):
                return x
        

def translate_lyric(lyric_data, dest='en'):
    async def googletrans(text, dest='en'):
        async with Translator() as translator:
            result = await translator.translate(text, dest=dest)
            return result
        
    trans_cache = ""
    trans_lyric_data = []
    for x in lyric_data:
        trans_cache += x["lyric_line"] + "\n"

    raw_text = asyncio.run(googletrans(trans_cache, dest=dest))
    trans_tuple = tuple(raw_text.text.split("\n"))
    for x in range(0, len(lyric_data)):
        trans_lyric_data.append({"startTimeMs": lyric_data[x]["startTimeMs"], "lyric_line": trans_tuple[x]})

    return trans_lyric_data

def init_spotify_api():
    with open(".env") as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            value = value.strip().strip('"').strip("'")
            globals()[key.strip()] = value.strip()

    if CLIENT_ID is None or CLIENT_SECRET is None or REDIRECT_URI is None or REFRESH_TOKEN is None:
        print("It looks like you didn't configured the Spotify API credentials yet.")
        from utils.spotify_api import user_authorization

def main():
    while True:
        if setting_mode == "dbus":
            session_bus = dbus.SessionBus()
            if dbus_player is None:
                try:
                    player_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
                except dbus.exceptions.DBusException:
                    error_print("Spotify is not running.")
                    exit()
                player_metadata = dbus.Interface(player_bus, "org.freedesktop.DBus.Properties")
                break
            else:
                dbus_names = session_bus.list_names()
                lf_services = [dbus_names for dbus_names in dbus_names if dbus_names.startswith("org.mpris.MediaPlayer2." + dbus_player)]
                if not lf_services:
                    raise Exception(f"There is no player with the name {dbus_player}.")
                try:
                    player_bus = session_bus.get_object(lf_services[0], "/org/mpris/MediaPlayer2")
                except dbus.exceptions.DBusException:
                    error_print("Something went wrong with the player" + player_bus)
                player_metadata = dbus.Interface(player_bus, "org.freedesktop.DBus.Properties")
                break

        elif setting_mode == "spotify-api":
            global get_track, access_token
            from utils.spotify_api import get_track
            access_token = get_track.get_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
            if access_token != 200:
                player_metadata = ""
                break
            else:
                error_print("To use the spotify-api you have to be online.")
        
        time.sleep(5)
        
    id = "initial"
    delta_time = 0
    while True:

        track_id, artist, title, time_pos, track_len = get_track_data(player_metadata, setting_mode)
        #Fetch lyric only when the track has changed
        if track_id != id:
            c_print("↻")
            id = track_id
            delta_time = 0
            sql_id, lang_code, lyric_data, w_chars = get_lyric(artist, title, dest_lang)      
            if lyric_data not in (404, 422, 400, 200, "None"):
                len_lyric_data = len(lyric_data)
                if translate == True and dest_lang not in lang_code:
                    lyric_data = translate_lyric(lyric_data, dest=dest_lang)
                    if offline_storage:
                        store_lyric_offline(artist, title, lyric_data, dest_lang, sql_id)
                elif translate == True and dest_lang in lang_code:
                    _, _, lyric_data = sqlite3_request(artist, title, dest_lang)
            else:
                delta = 3000
                error_print(lyric_data)
            
        if lyric_data not in (404, 422, 400, 200, "None"):
            sl_index = get_syncedlyric_index(lyric_data, time_pos)
            if len_lyric_data > sl_index+1:
                delta = (lyric_data[sl_index+1]["startTimeMs"] - time_pos)
            else:
                delta = (track_len - time_pos)

            if delta > 3000:
                delta = 3000
            current_time = time.time() * 1000
            delta_time = current_time+delta

            if setting_c_print == "default":
                d_print(lyric_data, w_chars, sl_index, track_id)
            else:
                c_print(f'{lyric_data[sl_index]["lyric_line"]}')

        time.sleep(delta / 1000)

if __name__ == "__main__":
    """ Command line argument parsing """
    descripton = """Lyrify - Display synchronized lyrics from your current song track in Spotify using lrclib.net"""
    RichHelpFormatter.styles.update({
        "argparse.text": "#6cbf7d bold",
        "argparse.args": "#6caabf",
        "argparse.help": "#cbcbcb",
    })
    
    # Initialize parser
    parser = argparse.ArgumentParser(prog="Lyrify", description=descripton, formatter_class=RichHelpFormatter)    
    parser.add_argument("-m", "--mode", default="dbus", choices=['dbus', 'spotify-api'], help = "Set the mode how lyrics should be received.")
    parser.add_argument("-p", "--print", default="default", choices=['stream', 'interactive'], help = "Print the output as stream or interactive (overwrite line)")
    parser.add_argument("-t", "--translate", metavar="language_code", help = "Translate the lyric to your desired language (e.g. 'de' for German, 'en' for English, 'fr' for French, etc.)")
    parser.add_argument("-i", "--init", choices=["spotify"], help = "Initialize the API configuration for the target music player.")
    parser.add_argument("-0", "--store-offline", action='store_true', help = "Write fetched lyrics to a file for offline access (experimental)")
    parser.add_argument("dbus_word", nargs="?", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.init:
        if "spotify" in args.init:
            from utils.spotify_api import user_authorization

    if args.mode:
        if "dbus" in args.mode:
            setting_mode = "dbus"
        elif "spotify-api" in args.mode:
            init_spotify_api()
            setting_mode = "spotify-api"
    
    if args.mode == "dbus" and args.dbus_word:
        if args.dbus_word == "help":
            print("You can use instead of Spotify any other music player. This feature don't work with all players because it depends supporting dynamic refreshment.")
            exit()
        dbus_player = args.dbus_word
    else:
        dbus_player = None

    if args.print:
        if "stream" in args.print:
            setting_c_print = "stream"
        elif "interactive" in args.print:
            setting_c_print = "interactive" 
        else:
            import shutil, os
            setting_c_print = "default"

    if args.translate:
        translate = True
        dest_lang = args.translate
    else:
        translate = False
        dest_lang = "orig"


    if args.store_offline:
        import sqlite3
        import os
        script_dir = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(script_dir + "/lyrics.db.lock"):
            with open(script_dir + "/lyrics.db.lock") as f:
                pid = int(f.read().strip())
                try:
                    os.kill(pid, 0)
                    offline_storage = False
                    print("\033[31m!!! WARNING !!!\033[0m\n\nThe database is currently in use by another process. Lyrics will not be saved to the database during this session.\n")
                    input("Press Enter to continue...")
                except ProcessLookupError:
                    offline_storage = True
        with open(script_dir + "/lyrics.db.lock", "w") as f:
            f.write(str(os.getpid()))
        conn = sqlite3.connect(script_dir + "/lyrics.db")
        cursor = conn.cursor()
        offline_usage = True
    else:
        offline_storage = False
        offline_usage = False

    main()

        


