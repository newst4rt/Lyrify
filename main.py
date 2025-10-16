#!/usr/bin/env python
from time import sleep
import argparse
from rich_argparse import RichHelpFormatter
from src.lyric_providers.lrclib import *

def get_lyric(artist: str | tuple | None, title: str | None, dest_lang: str):
    if artist is None or title is None:
        return -1, dest_lang, 6, None
    
    sql_id = -1
    if offline_usage:
        sql_id, lang_code, lyric_data, w_chars = sqlite3_request(artist, title, dest_lang)
        #if lyric_data and not isinstance(lyric_data, int):
        if lyric_data not in (400,):
           return sql_id, lang_code, lyric_data, w_chars
        
    lrclib_request = lrclib_api(artist, title)
    if offline_storage and lrclib_request not in (503,):
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
    
def main():
    id = None
    track_id = -1
    delta = 3000
    lyric_data = 204
    sql_id = -1

    while True:
        #track_data = track_id, time_pos, track_len, artist, title
        track_data = get_track_data(id)

        if isinstance(track_data, tuple) and track_data[0] != id: 
            ex_print("↻")
            id = track_data[0]
            sql_id, lang_code, lyric_data, w_chars = get_lyric(track_data[3], track_data[4], dest_lang) # type: ignore
            if isinstance(lyric_data, tuple):      
                len_lyric_data = len(lyric_data)
                track_len = track_data[2] # type: ignore
                if translate == True:
                    if dest_lang not in lang_code:
                        w_chars, lyric_data = translate_lyric(lyric_data, dest=dest_lang)
                        if offline_storage:
                            sql_id = store_lyric_offline(track_data[3], track_data[4], (w_chars, lyric_data), dest_lang, sql_id) # type: ignore

        elif isinstance(track_data, int): 
            id = track_data
            lyric_data = track_data

        if isinstance(lyric_data, tuple):
            sl_index = get_syncedlyric_index(lyric_data, track_data[1]) # type: ignore
            if sl_index is not None and len_lyric_data > sl_index+1: # type: ignore
                delta = (lyric_data[sl_index+1]["startTimeMs"] - track_data[1]) # type: ignore
            elif sl_index is not None:
                delta = (track_len - track_data[1]) # type: ignore

            if delta > 3000:
                delta = 3000

            ex_print(lyric_data, w_chars, sl_index, id) # type: ignore

        else:
            delta = 3000
            error_print(lyric_data)

        sleep(delta / 1000)

if __name__ == "__main__":
    """ Command line argument parsing """
    descripton = """Lyrify - Display synchronized lyrics from your current playback using lrclib.net"""
    RichHelpFormatter.styles.update({
        "argparse.text": "#6cbf7d bold",
        "argparse.args": "#6caabf",
        "argparse.help": "#cbcbcb",
    })
    
    # Initialize parser

    p_base = argparse.ArgumentParser(add_help=False)
    p_base.add_argument("-m", "--mode", default="dbus", choices=['dbus', 'spotify'], help = "Select the mode how lyrics should be received.")
    p_base.add_argument("-t", "--translate", metavar="language_code", help = "Translate lyrics to your desired language (e.g. 'de' for German, 'en' for English, 'fr' for French, etc.)")
    p_base.add_argument("-i", "--init", choices=["spotify"], help = "Initialize the API configuration for the target music player.")
    p_base.add_argument("-0", "--store-offline", action='store_true', help = "Write fetched lyrics to a file for offline access (experimental)")
    p_base.add_argument("dbus_word", nargs="?", help=argparse.SUPPRESS)

    p_mdef = argparse.ArgumentParser(prog="Lyrify", description=descripton, parents=[p_base], formatter_class=RichHelpFormatter)        
    p_sub = p_mdef.add_subparsers(dest="sub_arg", metavar="", title="Commands")
    p_mstr = p_sub.add_parser("stream", help="Print as stream to stdout.", parents=[p_base], formatter_class=RichHelpFormatter)
    p_int = p_sub.add_parser("interactive", help="Print as one liner with dynamic refreshment.", parents=[p_base], formatter_class=RichHelpFormatter)

    args = p_mdef.parse_args()

    

    if args.init:
        if "spotify" in args.init:
            from src.spotify import oauth
            oauth.init()

    if args.mode:
        """if args.dbus_word:

            dbus_player = args.dbus_word
        else:
            dbus_player = None"""

        if "dbus" in args.mode:
            if args.dbus_word == "help":
                print("You can use instead of Spotify any other player by passing the name of the player as argument.")
                exit()
            from src.core.dbus import *  
            dbus_player = args.dbus_word if args.dbus_word else "spotify"
            init_dbus(dbus_player)
        elif "spotify" in args.mode:
            from src.spotify.api_request import *
    
    if args.sub_arg == "stream":
        from src.core.print.stream_print import *
    elif args.sub_arg == "interactive":
        from src.core.print.interactive_print import *
    else:
        from src.core.print.default_print import *

    if args.translate:
        from src.translator.googletrans import *
        dest_lang = args.translate
    else:
        translate = False
        dest_lang = "orig"

    if args.store_offline:
        from src.sqlite3 import *
    else:
        offline_storage = False
        offline_usage = False

    main()

        


