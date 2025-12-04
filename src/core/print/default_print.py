import os
import shutil
from src.core.config import config
from src.core.__main__ import get_lyric
if config.translate is True:
    from src.translator.googletrans import translate_lyric
    if config.offline_storage is True:
        from src.sqlite3 import db_manager
if config.romanize is True:
    from src.utils.romanizer_uroman import *
    rom = Uroman()

class default_print:

    def __init__(self):
        self.STYLE_MAP = {
                "bold": 1,
                "italic": 3,
                "underline": 4,
                "normal": 0
        }
        
        self.old_lyric_index = -1
        self.old_terminal_size = -1
        self.old_track_id = -1
        self.cls = config.cls
        if self.check_truecolor():
            self.highlight_aescolor = f'\033[{0 if len(config.highlight_color) <= 1 else self.STYLE_MAP.get(config.highlight_color[1], 0)};38;2;{";".join(str(int(config.highlight_color[0][i:i + 2], 16)) for i in range(1, 7, 2))}m'
            self.passed_aescolor = f'\033[{0 if len(config.passed_color) <= 1 else self.STYLE_MAP.get(config.passed_color[1], 0)};38;2;{";".join(str(int(config.passed_color[0][i:i + 2], 16)) for i in range(1, 7, 2))}m'
            self.future_aescolor = f'\033[{0 if len(config.future_color) <= 1 else self.STYLE_MAP.get(config.future_color[1], 0)};38;2;{";".join(str(int(config.future_color[0][i:i + 2], 16)) for i in range(1, 7, 2))}m'

        else:
            # 256-color mode 
            self.highlight_aescolor = f'\033[{0 if len(config.highlight_color) <= 1 else self.STYLE_MAP.get(config.highlight_color[1], 0)};38;5;{self.conv_rgb_to_256(tuple(int(config.highlight_color[0][i:i + 2], 16) for i in range(1, 7, 2)))}m'
            self.passed_aescolor = f'\033[{0 if len(config.passed_color) <= 1 else self.STYLE_MAP.get(config.passed_color[1], 0)};38;5;{self.conv_rgb_to_256(tuple(int(config.passed_color[0][i:i + 2], 16) for i in range(1, 7, 2)))}m'
            self.future_aescolor = f'\033[{0 if len(config.future_color) <= 1 else self.STYLE_MAP.get(config.future_color[1], 0)};38;5;{self.conv_rgb_to_256(tuple(int(config.future_color[0][i:i + 2], 16) for i in range(1, 7, 2)))}m'

        if (config.translate or config.romanize) and config.hide_source == False:
            self.multi_line = True
        else:
            self.multi_line = False
        
    def check_truecolor(self):
        colorterm = os.environ.get("COLORTERM", "").lower()
        if colorterm in ("truecolor", "24bit"):
            return True
        term = os.environ.get("TERM_PROGRAM")
        if term and "Apple_Terminal" in term:
            return False
        else:
            return True
        
    def conv_rgb_to_256(self, rgb: tuple):
        #convert rgb to 256 color mode
        r, g, b = rgb

        R = min(5, round(r * 6 / 256))
        G = min(5, round(g * 6 / 256))
        B = min(5, round(b * 6 / 256))

        return 16 + 36*R + 6*G + B


    def get_terminal_size(self) -> tuple:
        terminal_size = shutil.get_terminal_size()
        return terminal_size.columns, terminal_size.lines

    def center_print(self, text: str) -> None:
        terminal_size = shutil.get_terminal_size()
        os.system(self.cls)
        for x in range(0, terminal_size.lines-2):
            if x == int(terminal_size.lines/2):
                print(f'{text.center(terminal_size.columns)}')
            else:
                print("")
                
    def error_print(self, text: str | int) -> None:
        if isinstance(text, int):
            self.center_print(f'🚫 {text} 🚫') 
        else:
            self.center_print(text) 

    def ex_print(self, lyric_data: tuple | str | int, w_chars: dict = {0:0}, lyric_index: int | None = None, track_id: str | int | None = None) -> None:
        if isinstance(lyric_data, tuple) and lyric_index is not None:
            terminal_columns, terminal_lines = self.get_terminal_size()
            sum_terminal_size = terminal_columns+terminal_lines
            terminal_columns, terminal_lines = self.get_terminal_size()
            if lyric_index != self.old_lyric_index or sum_terminal_size != self.old_terminal_size or track_id != self.old_track_id:
                self.old_lyric_index = lyric_index # In order to avoid unnecessary screen refreshes
                self.old_terminal_size = sum_terminal_size # In order to execute a screen refresh when the terminal size has changed
                self.old_track_id = track_id

                fxd_lyrics = self.fxt_helper(lyric_data, lyric_index, w_chars, terminal_lines, terminal_columns)
                os.system(self.cls)
                print(fxd_lyrics, end="")
        else:
            self.center_print(str(lyric_data))


    def center_text(self, text: str, terminal_columns: int, w_chars: int) -> str:
        padding = (terminal_columns-len(text)-w_chars) // 2
        return str(" "*padding + text)

    def fxt_helper(self, lyric_data: tuple, lyric_index: int, w_chars: dict, terminal_lines: int, terminal_columns: int) -> str:


        lxe_total = 2 if lyric_data[lyric_index]["lyric_line"] != "♬" and self.multi_line == True else 1
        it_lxe = 0

        """Precalculation how many lines fit in the terminal."""
        while True:
            lxe_pos = 3 if lyric_index+it_lxe >= len(lyric_data) and self.multi_line else 2 if lyric_index+it_lxe >= len(lyric_data) or lyric_data[lyric_index+it_lxe]["lyric_line"] == "♬" or self.multi_line == False else 3
            lxe_neg = 3 if lyric_index+((it_lxe+1)*-1) < 0 and self.multi_line else 2 if lyric_index+((it_lxe+1)*-1) < 0 or lyric_data[lyric_index+((it_lxe+1)*-1)]["lyric_line"] == "♬" or self.multi_line == False else 3
            if (lxe_total+lxe_pos+lxe_neg) < terminal_lines:
                lxe_total += lxe_pos + lxe_neg
                it_lxe += 1
            else:
                lxc_data = []
                w_charc = 0 if lyric_index not in w_chars else w_chars[lyric_index]
                lxc_data.append(f'{self.highlight_aescolor}{self.center_text(lyric_data[lyric_index]["lyric_line"], terminal_columns, w_charc)}\033[0m')
                if lyric_data[lyric_index]["lyric_line"] != "♬" and self.multi_line == True:
                    w_charc = 0 if lyric_index not in self.trans_w_chars else self.trans_w_chars[lyric_index]
                    _line = self.center_text(f'({self.trans_lyric_data[lyric_index]["lyric_line"]})', terminal_columns, w_charc)
                    lxc_data.append(f'{self.highlight_aescolor}{_line}\033[0m')
                    #lxc_data.append(f'{highlight_aescolor}{f'({self.trans_lyric_data[lyric_index]["lyric_line"]})'.center(terminal_columns-w_charc)}\033[0m')

                break

        for x in range(1, it_lxe+1):
            for y in range (1, -2, -2):
                lxe_ix = lyric_index+(x*y)
                w_charc = 0 if lxe_ix not in w_chars else w_chars[lxe_ix]
                if y > 0:
                    lxc_data.append("")
                    if lxe_ix < len(lyric_data):
                        lxc_data.append(f'{self.future_aescolor}{self.center_text(lyric_data[lxe_ix]["lyric_line"], terminal_columns, w_charc)}\033[0m')
                        if lyric_data[lxe_ix]["lyric_line"] != "♬" and self.multi_line == True:
                            w_charc = 0 if lxe_ix not in self.trans_w_chars else self.trans_w_chars[lxe_ix]
                            _line = self.center_text(f'({self.trans_lyric_data[lxe_ix]["lyric_line"]})', terminal_columns, w_charc)
                            lxc_data.append(f'{self.future_aescolor}{_line}\033[0m')
                    else:
                        lxc_data.append("")
                        if lyric_data[lyric_index+(x*-1)]["lyric_line"] != "♬" and self.multi_line == True:
                            lxc_data.append("")

                else:
                    lxc_data.insert(0, "")
                    if lxe_ix >= 0:
                        lxc_data.insert(0, f'{self.passed_aescolor}{self.center_text(lyric_data[lxe_ix]["lyric_line"], terminal_columns, w_charc)}\033[0m')
                        if lyric_data[lxe_ix]["lyric_line"] != "♬" and self.multi_line == True:
                            w_charc = 0 if lxe_ix not in self.trans_w_chars else self.trans_w_chars[lxe_ix]
                            _line = self.center_text(f'({self.trans_lyric_data[lxe_ix]["lyric_line"]})', terminal_columns, w_charc)
                            lxc_data.insert(1, f'{self.passed_aescolor}{_line}\033[0m')
                       
                    else:
                        lxc_data.insert(0, "")
                        if lyric_data[lxe_ix]["lyric_line"] != "♬" and self.multi_line == True:
                            lxc_data.insert(0, "")
                        
        lxc_pad = (terminal_lines-len(lxc_data))
        if lxc_pad > 0:
            lxc_data.insert(0, "")
            lxc_pad -= 1

        for x in range (2, lxc_pad, 2):
            lxc_data.insert(0, "")
            lxc_data.append("")


        return "\n".join(lxc_data)

    def main_gxl(self, track_data: tuple) -> tuple:
            self.ex_print("↻")
            id, _, track_len, artist, title = track_data # type: ignore
            sql_id, lang_code, lyric_data, w_chars = get_lyric(artist, title, config.dest_lang, track_len) # type: ignore
            if isinstance(lyric_data, tuple):      
                if config.translate:
                    if lang_code == "orig":
                        self.trans_w_chars, self.trans_lyric_data = translate_lyric(lyric_data, dest=config.dest_lang)
                        if config.offline_storage:
                            sql_id = db_manager.store_lyric_offline(artist, title, (self.trans_w_chars, self.trans_lyric_data), config.dest_lang, sql_id) # type: ignore
                        if config.hide_source:
                            w_chars, lyric_data = self.trans_w_chars, self.trans_lyric_data

                    elif config.hide_source == False:
                        self.trans_w_chars, self.trans_lyric_data = w_chars, lyric_data
                        _, _, lyric_data, w_chars = get_lyric(artist, title, "orig", track_len) # type: ignore
                        if isinstance(lyric_data, int):
                            return None, lyric_data

                if config.romanize:
                    self.multi_line = True
                    if config.translate and config.hide_source: #H-T-R
                        if w_chars[0] != 1:
                            self.multi_line = False
                            w_chars, lyric_data = self.trans_w_chars, self.trans_lyric_data

                        self.trans_lyric_data, self.trans_w_chars = rom.romanize_lyric(self.trans_lyric_data, self.trans_w_chars)

                    elif config.translate or config.hide_source: #T-R | H-R
                        lyric_data, w_chars = rom.romanize_lyric(lyric_data, w_chars)
                        if config.hide_source:
                            self.multi_line = False

                    else: #R
                        if w_chars[0] == 0:
                            self.multi_line = False
                        else:
                            self.trans_lyric_data, self.trans_w_chars = rom.romanize_lyric(lyric_data, w_chars)


            
            return w_chars, lyric_data
        

