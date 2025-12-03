#!/usr/bin/env python
from time import sleep
from src.lyric_providers.lrclib import *
from src.core.config import config
from src.core.com import *

def main():
    id = 0
    lyric_data = 204

    while True:
        track_data = mode.get_track_data(id)
        _id = track_data[0] if isinstance(track_data, tuple) else track_data

        if _id != id:
            if isinstance(track_data, tuple): 
                id, track_len = _id, track_data[2] # type: ignore
                w_chars, lyric_data = printer.main_gxl(track_data)

            elif isinstance(track_data, (int,str)): 
                id = track_data
                lyric_data = track_data

            if isinstance(lyric_data, (int,str)):
                config.delta = 3000
                printer.old_lyric_index = None
                printer.error_print(lyric_data)
            
            continue

        if isinstance(lyric_data, tuple):
            sl_index = sync_cxe.get_syncedlyric_index(lyric_data, track_data[1]) # type: ignore
            try:
                config.delta = (lyric_data[sl_index+1]["startTimeMs"] - track_data[1]) # type: ignore
            except IndexError:
                config.delta = (track_len - track_data[1]) # type: ignore

            if config.delta > 3000:
                config.delta = 3000

            printer.ex_print(lyric_data, w_chars, sl_index, id) # type: ignore

        sleep(config.delta / 1000)

if __name__ == "__main__":
    """ Command line argument parsing """
    style = {"prog_name" : ("#3a99ff", "bold"),
            "usage_prefix": ("#FFFCE7", "bold"),
        
            "commands_args" :  ("#5898E7", "bold"),
            "commands_help" : ("#CBCBCB"),
            "commands_req" : "#88e6fd",
            "commands_metavar" : "#ecbc84",
            "commands_pipe" : ("#7E7E7E", "bold"),

            "options_args" :  ("#FF8B6A", "bold"),
            "options_req" : "#c77e25" ,
            "options_metavar" : "#ecbc84" ,
            "options_pipe" : ("#7E7E7E", "bold"),

            "dxt_options_args" :  ("#e5e996", "bold"),
            "dxt_options_req" : "#e5e996" ,
            "dxt_options_metavar" : ("#d9dd99") ,
            "dxt_options_pipe" : ("#7E7E7E", "bold"),

            "title_args" : ("#67c236", "bold"),
            "title_pipe" : ("#7E7E7E", "bold"),
            "title_req" : "#c77e25", 
            "title_brackets" : "#7E7E7E",
            "title_metavar" :  "#d8892e",
    }

    description = """Lyrify - Display synchronized lyrics from any music player."""
    com = Commander()
    com.styles.update(style)
    com.com_title = ("Lyrify", description)
    
    com.add_text("Core Options: \n", "optional_2")
    com.add_arg("-h", "--help", required=None, help="Display this help message.")
    com.add_arg("-m", "--mode", nargs=[2, 1], required=['dbus', 'spotify'] if config.os == "Linux" else ['wmc', 'spotify'] if config.os == "Windows" else ["ascript", 'spotify'] if config.os == "Darwin" else ["spotify"], help="Select mode.")
    com.add_arg("-t", "--translate", nargs=1, metavar="language_code", help = "Translate lyrics. (Use ISO-639 as language code)")
    com.add_arg("-r", "--romanize", help = "Romanize lyrics.")
    com.add_arg("-i", "--init", required=["spotify"], help = "Initialize the API configuration for the target music player.")
    com.add_arg("-o", "--store-offline", help = "Store lyrics for offline usage.")

    com.add_stylegroup("options", indent=2 , index=1)
    sub_com = SubCommander(com)
    sub_com.add_text("Commands: \n", "commands_args")
    sub_com.add_com("stream", metavar="[--help]", help="Stream Mode")
    sub_com.add_com("interactive", metavar="[--help]", help="Interactive Mode")
    sub_com.add_text("")
    sub_com.add_stylegroup("commands", indent=2, index=0)


    a_sub_com = SubCommander(sub_com)
    a_sub_com.add_text("\nDefault:\n", "optional_1")
    a_sub_com.add_arg("-s", "--style", metavar="<file>", nargs=1, help="Apply a style file.")
    a_sub_com.add_arg("-0", "--hide-sourcelyrics", help="Hide source lyrics when using translation, romanizing or both.")
    a_sub_com.add_stylegroup("dxt_options", index=2, indent=2)


    args = a_sub_com.parse_args()

    if args.help:
        if args.interactive or args.stream:
            com.print_help()
        else:
            a_sub_com.print_help()

    if args.init:
        if "spotify" in args.init:
            from src.spotify import oauth
            oauth.init()

    if config.os == "Linux":
        if args.mode:
            if "dbus" in args.mode:
                config.player = args.mode[1] if len(args.mode) > 1 else "spotify"
                from src.core.dbus import Mpris
                mode = Mpris(config.player)
            elif "spotify" in args.mode:
                from src.spotify.api_request import Spotify_API
                mode = Spotify_API()
        else:
            from src.core.dbus import Mpris
            mode = Mpris(config.player)
    elif config.os == "Windows":
        if args.mode:
            if "wmc" in args.mode:
                import asyncio
                from src.core.winrt_wmc import Wmc
                config.player = args.mode[1] if len(args.mode) > 1 else "Spotify"
                mode = asyncio.run(Wmc.create(config.player))
            elif "spotify" in args.mode:
                from src.spotify.api_request import Spotify_API
                mode = Spotify_API()
        else:
            from src.spotify.api_request import Spotify_API
            mode = Spotify_API()

    elif config.os == "Darwin":
        if args.mode:
            if "ascript" in args.mode:
                config.player = args.mode[1] if len(args.mode) > 1 else "spotify"
                from src.core.mac import AScript
                mode = AScript(config.player)
            elif "spotify" in args.mode:
                from src.spotify.api_request import Spotify_API
                mode = Spotify_API()
        else:
            from src.spotify.api_request import Spotify_API
            mode = Spotify_API()

    
    if args.romanize:
        config.romanize = True
    
    if args.translate:
        config.translate = True
        config.dest_lang = "".join(args.translate)

    if args.store_offline:
        from src.sqlite3 import Database_Manager

    if args.hide_sourcelyrics:
        if args.translate or args.romanize:
            config.hide_source = True
        else:
            com.raise_error("--hide-sourcelyric option can only be used in default mode in combination with --translate, --romanize, or both.")

    if args.style:
        config.read_style(args.style[0])
    else:
        config.read_style()


    if args.interactive:
        config.terminal_mode = "interactive"
        import src.core.print.ias_utils as printer
    elif args.stream:
        config.terminal_mode = "stream"
        import src.core.print.ias_utils as printer
    else:
        from src.core.print.default_print import *
        printer = default_print()
        config.terminal_mode = "default"

    import src.core.__main__ as cxe
    sync_cxe = cxe.Cxe()
    try:
        print('\033[?25l', end="")
        main()
    except Exception as e:
        raise(e)
    except BaseException as e:
        exit()
    finally:
        print('\033[?25h')


        


