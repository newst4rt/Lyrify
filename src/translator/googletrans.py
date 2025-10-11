import asyncio
from googletrans import Translator
import unicodedata

def translate_lyric(lyric_data, dest='en'):
    async def googletrans(text, dest='en'):
        async with Translator() as translator:
            result = await translator.translate(text, dest=dest)
            return result
    def is_cjk(ch):
        return unicodedata.east_asian_width(ch) in ("W", "F")
    
    trans_cache = ""
    trans_lyric_data = []
    w_chars = {0: 0}
    for x in lyric_data:
        trans_cache += x["lyric_line"] + "\n"

    raw_text = asyncio.run(googletrans(trans_cache, dest=dest))
    trans_tuple = tuple(raw_text.text.split("\n"))
    for x in range(0, len(lyric_data)):
        lyric_line = trans_tuple[x]
        if (cjk_count := sum(1 for ch in lyric_line if is_cjk(ch))):
            w_chars[x + 1] = cjk_count

        trans_lyric_data.append({"startTimeMs": lyric_data[x]["startTimeMs"], "lyric_line": lyric_line})

    return w_chars, tuple(trans_lyric_data)

if __name__ == "src.translator.googletrans":
    translate = True

