#!/usr/bin/env python
from time import sleep
import argparse
from rich_argparse import RichHelpFormatter
from src.lyric_providers.lrclib import *
import src.core.config as config

def main():
    id = None
    delta = 3000
    lyric_data = 204

    while True:
        track_data = get_track_data(id)

        if isinstance(track_data, tuple) and track_data[0] != id: 
            id, track_len = track_data[0], track_data[2] # type: ignore
            w_chars, lyric_data = main_gxl(track_data)
        elif isinstance(track_data, int): 
            id = track_data
            lyric_data = track_data

        if isinstance(lyric_data, tuple):
            sl_index = cxe.get_syncedlyric_index(lyric_data, track_data[1]) # type: ignore
            try:
                delta = (lyric_data[sl_index+1]["startTimeMs"] - track_data[1]) # type: ignore
            except IndexError:
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
        "argparse.help": "#E0E0E0",
    })
    
    # Initialize parser

    p_base = argparse.ArgumentParser(add_help=False)
    p_base.add_argument("-m", "--mode", default=None, choices=['dbus', 'spotify'], help = "Select the mode how lyrics should be received.")
    p_base.add_argument("-t", "--translate", metavar="language_code", help = "Translate lyrics to your desired language (e.g. 'de' for German, 'en' for English, 'fr' for French, etc.)")
    p_base.add_argument("-i", "--init", choices=["spotify"], help = "Initialize the API configuration for the target music player.")
    p_base.add_argument("-0", "--store-offline", action='store_true', help = "Write fetched lyrics to a file for offline access (experimental)")
    p_base.add_argument("dbus_word", nargs="?", help=argparse.SUPPRESS)

    p_core = argparse.ArgumentParser(prog="Lyrify", description=descripton, parents=[p_base], formatter_class=RichHelpFormatter)    
    p_default = p_core.add_argument_group(description="Additional Options:")
    p_default.add_argument("-c", "--highlight-color", metavar="R,G,B", default="23,255,23", help = "Set the color for highlighting lyrics (default: 23,255,23).")    
    p_sub = p_core.add_subparsers(dest="sub_arg", metavar="", title="Print Modes", help='Use „stream|interactive --help" for more info.\n')
    p_mstr = p_sub.add_parser("stream", help="Print as stream to stdout.", parents=[p_base], formatter_class=RichHelpFormatter)
    p_int = p_sub.add_parser("interactive", help="Print as one liner and dynamic refreshment.", parents=[p_base], formatter_class=RichHelpFormatter)

    args = p_core.parse_args()

    

    if args.init:
        if "spotify" in args.init:
            from src.spotify import oauth
            oauth.init()

    if args.mode:
        if "dbus" in args.mode:
            if args.dbus_word == "help":
                print("You can use instead of Spotify any other player by passing the name of the player as argument.")
                exit()
            from src.core.dbus import *  
            dbus_player = args.dbus_word if args.dbus_word else "spotify"
            init_dbus(dbus_player)
        elif "spotify" in args.mode:
            from src.spotify.api_request import *
    elif args.dbus_word:
        p_core.error(f'Bad Argument {args.dbus_word}.')
    else:
        from src.core.dbus import * 
        init_dbus("spotify")
    


    if args.translate:
        #from src.translator.googletrans import *
        config.translate = True
        config.dest_lang = args.translate

    if args.store_offline:
        #from src.sqlite3 import *
        config.offline_storage = True
        config.offline_usage = True

    if args.highlight_color:
        try:
            _hc_color = tuple(int(c) for c in args.highlight_color.split(","))
            if len(_hc_color) != 3 or any(x > 0 or x < 255 for x in _hc_color):
                config.highlight_rgbcolor = _hc_color # type: ignore
        except ValueError:
            p_core.error("Highlight color must be in the format R,G,B with values between 0 and 255.")


    if args.sub_arg in ("stream", "interactive"):
        config.terminal_mode = args.sub_arg
        from src.core.print.ias_utils import * 
    else:
        from src.core.print.default_print import *  
        config.terminal_mode = "default"

    import src.core.__main__ as cxe
    main()

        


