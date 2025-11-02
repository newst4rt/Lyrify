from platform import system

offline_storage = False
offline_usage = False
translate = False
romanize = False
dest_lang = "orig"
highlight_rgbcolor = (23, 255, 23)
terminal_mode = "Default"
hide_source = False

if system() == "Linux":
    os = "Linux"
    cls = "clear"
elif system() == "Windows":
    os = "Windows"
    cls = "cls"

#delta = 3000