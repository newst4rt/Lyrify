import os
import shutil
import src.core.config as config
from src.core.__main__ import get_lyric
if config.translate is True:
    from src.translator.googletrans import translate_lyric
    if config.offline_storage is True:
        from src.sqlite3 import store_lyric_offline
if config.romanize is True:
    from src.utils.romanizer_uroman import romanize_lyric

class default_print:

    def __init__(self):
        self.old_lyric_index = -1
        self.old_terminal_size = -1
        self.old_track_id = -1
        self.passed_lyric_rgbcolor=(108, 108, 108)
        if config.translate or config.romanize and config.hide_source == False:
            self.multi_line = True
        else:
            self.multi_line = False
        

    def get_terminal_size(self) -> tuple:
        terminal_size = shutil.get_terminal_size()
        return terminal_size.columns, terminal_size.lines

    def center_print(self, text: str) -> None:
        terminal_size = shutil.get_terminal_size()
        os.system('clear')
        for x in range(0, terminal_size.lines-2):
            if x == int(terminal_size.lines/2)+1:
                print(f"{text.center(terminal_size.columns)}")
            else:
                print("")
                
    def error_print(self, text: str | int) -> None:
        if isinstance(text, int):
            self.center_print(f"🚫 {text} 🚫") 
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
                os.system('clear')
                for x in range(0, len(fxd_lyrics)-1):
                    print(f'{fxd_lyrics[x]}')
                else:
                    print(f'{fxd_lyrics[len(fxd_lyrics)-1]}', end="\r")
        else:
            self.center_print(str(lyric_data))


    def center_text(self, text: str, terminal_columns: int, w_chars: int) -> str:
        padding = (terminal_columns-len(text)-w_chars) // 2
        return str(" "*padding + text)

    def fxt_helper(self, lyric_data: tuple, lyric_index: int, w_chars: dict, terminal_lines: int, terminal_columns: int) -> None:
        highlight_aescolor = f"\033[38;2;{config.highlight_rgbcolor[0]};{config.highlight_rgbcolor[1]};{config.highlight_rgbcolor[2]}m"
        passed_lyric_aescolor = f"\033[38;2;{self.passed_lyric_rgbcolor[0]};{self.passed_lyric_rgbcolor[1]};{self.passed_lyric_rgbcolor[2]}m"

        lxe_total = 2 if lyric_data[lyric_index]["lyric_line"] != "♬" and self.multi_line == True else 1
        it_lxe = 0

        """Precalculation how many lines fit in our terminal."""
        while True:
            lxe_pos = 3 if lyric_index+it_lxe >= len(lyric_data) and self.multi_line else 2 if lyric_index+it_lxe >= len(lyric_data) or lyric_data[lyric_index+it_lxe]["lyric_line"] == "♬" or self.multi_line == False else 3
            lxe_neg = 3 if lyric_index+(it_lxe*-1) < 0 and self.multi_line else 2 if lyric_index+(it_lxe*-1) < 0 or lyric_data[lyric_index+(it_lxe*-1)]["lyric_line"] == "♬" or self.multi_line == False else 3
            if (lxe_total+lxe_pos+lxe_neg) < terminal_lines:
                lxe_total += lxe_pos + lxe_neg
                it_lxe += 1
            else:
                lxc_data = []
                w_charc = 0 if lyric_index not in w_chars else w_chars[lyric_index]
                lxc_data.append(f'{highlight_aescolor}{self.center_text(lyric_data[lyric_index]["lyric_line"], terminal_columns, w_charc)}\033[0m')
                if lyric_data[lyric_index]["lyric_line"] != "♬" and self.multi_line == True:
                    w_charc = 0 if lyric_index not in self.trans_w_chars else self.trans_w_chars[lyric_index]
                    lxc_data.append(f'{highlight_aescolor}{self.center_text(f'({self.trans_lyric_data[lyric_index]["lyric_line"]})', terminal_columns, w_charc)}\033[0m')
                    #lxc_data.append(f'{highlight_aescolor}{f'({self.trans_lyric_data[lyric_index]["lyric_line"]})'.center(terminal_columns-w_charc)}\033[0m')

                break

        for x in range(1, it_lxe+1):
            for y in range (1, -2, -2):
                lxe_ix = lyric_index+(x*y)
                w_charc = 0 if lxe_ix not in w_chars else w_chars[lxe_ix]
                if y > 0:
                    lxc_data.append("")
                    if lxe_ix < len(lyric_data):
                        lxc_data.append(self.center_text(lyric_data[lxe_ix]["lyric_line"], terminal_columns, w_charc))
                        if lyric_data[lxe_ix]["lyric_line"] != "♬" and self.multi_line == True:
                            w_charc = 0 if lxe_ix not in self.trans_w_chars else self.trans_w_chars[lxe_ix]
                            lxc_data.append(f'{self.center_text(f'({self.trans_lyric_data[lxe_ix]["lyric_line"]})', terminal_columns, w_charc)}')
                    else:
                        lxc_data.append("")
                        if lyric_data[lyric_index+(x*-1)]["lyric_line"] != "♬" and self.multi_line == True:
                            lxc_data.append("")

                else:
                    lxc_data.insert(0, "")
                    if lxe_ix >= 0:
                        lxc_data.insert(0, f'{passed_lyric_aescolor}{self.center_text(lyric_data[lxe_ix]["lyric_line"], terminal_columns, w_charc)}\033[0m')
                        if lyric_data[lxe_ix]["lyric_line"] != "♬" and self.multi_line == True:
                            w_charc = 0 if lxe_ix not in self.trans_w_chars else self.trans_w_chars[lxe_ix]
                            lxc_data.insert(1, f'{passed_lyric_aescolor}{self.center_text(f'({self.trans_lyric_data[lxe_ix]["lyric_line"]})', terminal_columns, w_charc)}\033[0m')
                       
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


        return lxc_data

    def main_gxl(self, track_data: tuple) -> tuple:
            self.ex_print("↻")
            id, _, track_len, artist, title = track_data # type: ignore
            sql_id, lang_code, lyric_data, w_chars = get_lyric(artist, title, config.dest_lang, track_len) # type: ignore
            if isinstance(lyric_data, tuple):      
                if config.translate:
                    if lang_code == "orig":
                        self.trans_w_chars, self.trans_lyric_data = translate_lyric(lyric_data, dest=config.dest_lang)
                        if config.offline_storage:
                            sql_id = store_lyric_offline(artist, title, (self.trans_w_chars, self.trans_lyric_data), config.dest_lang, sql_id) # type: ignore
                        if config.hide_source:
                            w_chars, lyric_data = self.trans_w_chars, self.trans_lyric_data

                    elif config.hide_source == False:
                        self.trans_w_chars, self.trans_lyric_data = w_chars, lyric_data
                        _, _, lyric_data, w_chars = get_lyric(artist, title, "orig", track_len) # type: ignore

                if config.romanize:
                    if config.translate and config.hide_source:
                        self.trans_lyric_data, self.trans_w_chars = romanize_lyric(lyric_data, w_chars)

                    elif config.translate or config.hide_source: 
                        lyric_data, w_chars = romanize_lyric(lyric_data, w_chars)
                    else:
                        self.trans_lyric_data, self.trans_w_chars = romanize_lyric(lyric_data, w_chars)
            
            return None if w_chars is None else w_chars, lyric_data
        

