import uroman as ur

def romanize_lyric(lyric_data: tuple, w_chars: dict) -> tuple:
    rom_lyric_data = []
    uroman = ur.Uroman()
    if w_chars[0] == 0:
        return lyric_data, w_chars
    
    for x in range(0, len(lyric_data)):
        rom_lyric_data.append({"startTimeMs": lyric_data[x]["startTimeMs"], "lyric_line": uroman.romanize_string(lyric_data[x]["lyric_line"])})

    return tuple(rom_lyric_data), {0:0}