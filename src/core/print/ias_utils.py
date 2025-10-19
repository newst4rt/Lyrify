# Utilities for interactive and stream print 
import src.core.config as config
if config.terminal_mode == "stream":
    from src.core.print.stream_print import *
elif config.terminal_mode == "interactive":
    from src.core.print.interactive_print import *
from src.core.__main__ import get_lyric
if config.translate is True:
    from src.translator.googletrans import translate_lyric
    if config.offline_storage is True:
        from src.sqlite3 import store_lyric_offline
def main_gxl(track_data: tuple):
        ex_print("↻")
        id, _, track_len, artist, title = track_data # type: ignore
        sql_id, lang_code, lyric_data, w_chars = get_lyric(artist, title, config.dest_lang, track_len) # type: ignore
        if isinstance(lyric_data, tuple):      
            if config.translate == True:
                if config.dest_lang not in lang_code:
                    w_chars, lyric_data = translate_lyric(lyric_data, dest=config.dest_lang)
                    if config.offline_storage:
                        sql_id = store_lyric_offline(artist, title, (w_chars, lyric_data), config.dest_lang, sql_id) # type: ignore

        return None if w_chars is None else w_chars, lyric_data