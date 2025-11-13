from platform import system

class Config():

    def __init__(self):
        self.offline_storage = False
        self.offline_usage = False
        self.translate = False
        self.romanize = False
        self.dest_lang = "orig"
        self.highlight_rgbcolor = (0, 255, 0)
        self.terminal_mode = "Default"
        self.hide_source = False
        self.player = "spotify"
        self.delta = 3000

        _os = system()

        if _os == "Linux":
            self.os = _os
            self.cls = "clear"
        elif _os == "Windows":
            self.os = _os
            self.cls = "cls"
        elif _os == "Darwin":
            self.os = _os
            self.cls = "printf '\33c\\e[3J'"
        else:
            print("Unknown Operating System.\n\nExit...")
            exit()

        #delta = 3000

config = Config()