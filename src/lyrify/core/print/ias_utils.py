# Utilities for interactive and stream print 
from lyrify.core.config import config
if config.terminal_mode == "stream":
    from lyrify.core.print.stream_print import *
elif config.terminal_mode == "interactive":
    from lyrify.core.print.interactive_print import *
from lyrify.core.__main__ import get_lyric
if config.translate:
    from lyrify.translator.googletrans import translate_lyric
    if config.offline_storage:
        from lyrify.db_sqlite import db_manager

if config.romanize is True:
    from lyrify.utils.romanizer_uroman import *
    rom = Uroman()

def main_gxl(track_data: tuple) -> tuple:
        ex_print("↻") # type: ignore
        id, _, track_len, artist, title = track_data # type: ignore
        sql_id, lang_code, lyric_data, w_chars = get_lyric(artist, title, config.dest_lang, track_len) # type: ignore
        if isinstance(lyric_data, tuple):      
            if config.translate and config.dest_lang not in lang_code:
                w_chars, lyric_data = translate_lyric(lyric_data, dest=config.dest_lang) # type: ignore
                if config.offline_storage:
                    sql_id = db_manager.store_lyric_offline(artist, title, (w_chars, lyric_data), config.dest_lang, sql_id) # type: ignore

            if config.romanize:
                 lyric_data, w_chars = rom.romanize_lyric(lyric_data, w_chars) # type: ignore

        return None if w_chars is None else w_chars, lyric_data