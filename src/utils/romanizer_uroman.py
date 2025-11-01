import uroman as ur

class Uroman()
    def __init__(self):
        self.uroman = ur.Uroman()
    def romanize_lyric(self, lyric_data: tuple, w_chars: dict) -> tuple:
        rom_lyric_data = []

        if w_chars[0] == 0:
            return lyric_data, w_chars
        
        for x in range(0, len(lyric_data)):
            rom_lyric_data.append({"startTimeMs": lyric_data[x]["startTimeMs"], "lyric_line": self.uroman.romanize_string(lyric_data[x]["lyric_line"])})

        return tuple(rom_lyric_data), {0:0}