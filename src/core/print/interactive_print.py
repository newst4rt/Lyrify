import sys
import shutil
#from utils_print import get_terminal_size 

old_text = ""
max_lyric_len = 0

<<<<<<< HEAD

=======
>>>>>>> main
def ex_print(lyric_data: tuple | str | int, w_chars: dict | None = None, lyric_index: int | None = None, track_id: str | int | None = None):
    global old_text, max_lyric_len
    if isinstance(lyric_data, tuple) and lyric_index is not None:
        text = lyric_data[lyric_index]["lyric_line"]
    else:
        text = str(lyric_data)
    
    len_text = len(text)
    if len_text < max_lyric_len:
        print(" "*max_lyric_len, end="\r", flush=True)
    
    """If you like to set a maximum of character for displaying the lyric add [:<num>] to print and define the number"""
    print(f'{text}', end="\r", flush=True)
    max_lyric_len = len_text

def error_print(text: str | int):
    ex_print(text) 