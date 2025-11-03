#!/usr/bin/env python
from time import sleep
from src.lyric_providers.lrclib import *
import src.core.config as config
from src.Commander.com import *

def main():
    id = None
    delta = 3000
    lyric_data = 204

    while True:
        track_data = get_track_data(id)

        if isinstance(track_data, tuple) and track_data[0] != id: 
            id, track_len = track_data[0], track_data[2] # type: ignore
            w_chars, lyric_data = printer.main_gxl(track_data)
        elif isinstance(track_data, int): 
            id = track_data
            lyric_data = track_data

        if isinstance(lyric_data, tuple):
            sl_index = sync_cxe.get_syncedlyric_index(lyric_data, track_data[1]) # type: ignore
            try:
                delta = (lyric_data[sl_index+1]["startTimeMs"] - track_data[1]) # type: ignore
            except IndexError:
                delta = (track_len - track_data[1]) # type: ignore

            if delta > 3000:
                delta = 3000

            printer.ex_print(lyric_data, w_chars, sl_index, id) # type: ignore

        else:
            delta = 3000
            printer.error_print(lyric_data)

        sleep(delta / 1000)

if __name__ == "__main__":
    """ Command line argument parsing """
    style = {"commands_args" :  ("#5898E7", "bold"),
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
            "dxt_options_metavar" : ("#e5e996") ,
            "dxt_options_pipe" : ("#7E7E7E", "bold"),

            "title_args" : ("#67c236", "bold"),
            "title_pipe" : ("#7E7E7E", "bold"),
            "title_req" : "#c77e25", 
            "title_brackets" : "#7E7E7E",
            "title_metavar" :  "#d8892e",
    }
    
    description = """Lyrify - Display synchronized lyrics from your current playback using lrclib.net"""
    com = Commander()
    com.styles.update(style)
    com.com_title = ("Lyrify", description)
    
    com.add_text(" Core Options: \n", "optional_2", 2, index=1)
    com.add_stylegroup("commands")
    com.add_arg("-h", "--help", nargs=1, required=None, help="This is a simple help message")
    com.add_arg("-m", "--mode", nargs=2, required=['dbus', 'spotify'] if config.os == "linux" else ['spotify'], help="Select the mode how lyrics should be received.")
    com.add_arg("-t", "--translate", metavar="language_code", help = "Translate lyrics to your desired language (e.g. 'de' for German, 'en' for English, 'fr' for French, etc.)")
    com.add_arg("-r", "--romanize", help = "Romanize lyrics.")
    com.add_arg("-i", "--init", required=["spotify"], help = "Initialize the API configuration for the target music player.")
    com.add_arg("-o", "--store-offline", help = "Store lyrics for offline usage.")

    com.add_stylegroup("options")
    sub_com = SubCommander(com)
    sub_com.add_com("stream", metavar="[--help]", help="Stream Mode", index=0)
    sub_com.add_com("interactive", metavar="[--help]", help="Interactive Mode", index=0)
    sub_com.add_text("Commands: \n", "commands_args", 1, index=0)
    sub_com.add_text("", index=3)

    a_sub_com = SubCommander(sub_com)
    a_sub_com.add_text("\n  Default:\n", "optional_1", idt=3)
    a_sub_com.add_arg("-c", "--highlight-color", metavar="R,G,B", help="Set the color for highlighting lyrics (default: 23,255,23).")
    a_sub_com.add_arg("-0", "--hide-sourcelyrics", help="Hide source lyrics when using translation.")
    a_sub_com.add_stylegroup("dxt_options")


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
                from src.core.dbus import *  
                dbus_player = args.mode[1] if len(args.mode) > 1 else "spotify"
                init_dbus(dbus_player)
            elif "spotify" in args.mode:
                from src.spotify.api_request import *
        else:
            from src.core.dbus import * 
            init_dbus("spotify")
    elif config.os == "Windows":
        from src.spotify.api_request import *
    

    if args.romanize:
        config.romanize = True
    
    if args.translate:
        config.translate = True
        config.dest_lang = "".join(args.translate)

    if args.store_offline:
        config.offline_storage = True
        config.offline_usage = True

    if args.hide_sourcelyrics:
        if args.translate or args.romanize:
            config.hide_source = True
        else:
            com.raise_error("--hide-sourcelyric option can only be used in default mode in combination with --translate, --romanize, or both.")

    if args.highlight_color:
        try:
            _hc_color = tuple(int(c) for c in args.highlight_color[0].split(","))
            if len(_hc_color) != 3 or any(x > 0 or x < 255 for x in _hc_color):
                config.highlight_rgbcolor = _hc_color # type: ignore
        except ValueError:
            com.raise_error("Highlight color must be in the format R,G,B with values between 0 and 255.")


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
        print('\033[?25h', end="")
        raise(e)
    except BaseException as e:
        print('\033[?25h')
        exit()

        


