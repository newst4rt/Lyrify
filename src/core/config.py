from platform import system
log_errors = False
class Config():

    def __init__(self):
        self.offline_storage = False
        self.offline_usage = False
        self.translate = False
        self.romanize = False
        self.dest_lang = "orig"
        self.highlight_color = ("#00ff00",)
        self.passed_color= ("#6c6c6c",)
        self.future_color= ("#ffffff",)
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
            self.cls = "printf '\33c\\e[3J\033[?25l'"
        else:
            print("Unknown Operating System.\n\nExit...")
            exit()

        #delta = 3000

    def read_style(self, file = "src/style.config"):
        mode = None
        with open(file) as f:
            data = f.readlines()
            if data[0].startswith("[") and data[0].endswith("]"):
                    mode = data[0][0].strip()[1:-1]
                    if mode is not ["DEFAULT"]:
                        print(f'Wrong section header {mode} in style.config. \n\n Exit...')
                        exit()
            for x in data[1:]:
                if x == "\n":
                    continue
                elif x.startswith("passed_color"):
                    self.passed_color=tuple(x[x.index(":")+1:].strip().replace(" ", "").split(","))
                elif x.startswith("highlight_color"):
                    self.highlight_color=tuple(x[x.index(":")+1:].strip().replace(" ", "").split(","))
                elif x.startswith("future_color"):
                    self.future_color=tuple(x[x.index(":")+1:].strip().replace(" ", "").split(","))
                else:
                    print(f'Bad options {x} in style.config. \n\n Exit...')
                    exit()







config = Config()