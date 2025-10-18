import os
import shutil

def get_terminal_size():
    terminal_size = shutil.get_terminal_size()
    return terminal_size.columns, terminal_size.lines

def center_print(text: str):
    terminal_size = shutil.get_terminal_size()
    os.system('clear')
    for x in range(0, terminal_size.lines-2):
        if x == int(terminal_size.lines/2)+1:
            print(f"{text.center(terminal_size.columns)}")
        else:
            print("")
            
def error_print(text: str | int):
    if isinstance(text, int):
        center_print(f"🚫 {text} 🚫") 
    else:
        center_print(text) 

#highlight_color #17ff17 , passed_color #6c6c6c
def ex_print(lyric_data: tuple | str | int, w_chars: dict = {0:0}, lyric_index: int | None = None, track_id: str | int | None = None):
    global old_lyric_index, old_terminal_size, old_track_id
    if isinstance(lyric_data, tuple) and lyric_index is not None:
        #AES = ANSI-Escape-Sequenz
        highlight_aescolor = f"\033[38;2;{highlight_rgbcolor[0]};{highlight_rgbcolor[1]};{highlight_rgbcolor[2]}m"
        passed_lyric_aescolor = f"\033[38;2;{passed_lyric_rgbcolor[0]};{passed_lyric_rgbcolor[1]};{passed_lyric_rgbcolor[2]}m"
        
        #terminal_size = shutil.get_terminal_size()
        terminal_columns, terminal_lines = get_terminal_size()
        sum_terminal_size = terminal_columns+terminal_lines
        max_range = lyric_index+int(terminal_lines/4)
        if lyric_index != old_lyric_index or sum_terminal_size != old_terminal_size or track_id != old_track_id:
            old_lyric_index = lyric_index # In order to avoid unnecessary screen refreshes
            old_terminal_size = sum_terminal_size # In order to execute a screen refresh when the terminal size has changed
            old_track_id = track_id
            max_len = len(lyric_data)
            if terminal_lines % 4 == 3 or terminal_lines % 4 == 2:
                max_range += 1

            os.system('clear')
            for x in range(lyric_index-int(terminal_lines/4), max_range):
                if x >= max_len:
                    break
                if x < 0:
                    print("\n".center(terminal_columns))
                    continue
                if x in w_chars:
                    w_charc = w_chars[x]
                else:
                    w_charc = 0

                if x == lyric_index:
                    print(f"{highlight_aescolor}{lyric_data[x]["lyric_line"].center(terminal_columns-w_charc)}\033[0m")                
                elif x < lyric_index:
                    print(f"{passed_lyric_aescolor}{lyric_data[x]["lyric_line"].center(terminal_columns-w_charc)}\033[0m")
                else:
                    print(lyric_data[x]["lyric_line"].center(terminal_columns-w_charc))
                print("\n", end="")
    else:
        center_print(str(lyric_data))

if __name__ == "src.core.print.default_print":
    
    old_lyric_index = -1
    old_terminal_size = -1
    old_track_id = -1
    # Hint: you can change this color how you like.
    highlight_rgbcolor=(23, 255, 23)
    passed_lyric_rgbcolor=(108, 108, 108)
