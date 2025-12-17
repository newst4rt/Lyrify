import sys

old_text = ""

def ex_print(lyric_data: tuple | str | int, w_chars: dict | None = None, lyric_index: int | None = None, track_id: str | int | None = None):
    global old_text
    if isinstance(lyric_data, tuple) and lyric_index is not None:
        text = lyric_data[lyric_index]["lyric_line"]
    else:
        text = lyric_data

    if text == old_text:
        return
    sys.stdout.write(f'{text}\n')
    sys.stdout.flush()
    old_text = text

def error_print(text: str | int):
    ex_print(text) 