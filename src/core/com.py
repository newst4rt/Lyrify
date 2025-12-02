import sys
import re
import os

class Commander():

    class Args:
        def __init__(self, kwargs):
            self.__dict__.update(kwargs)
    class DefaultStyles():
        def __init__(self):

            self.STYLE_MAP = {
                "bold": 1,
                "italic": 3,
                "underline": 4,
                "normal": 0
            }

            self.base = ("_args", "_brackets", "_comma", "_help", "_req", "_pipe", "_metavar")
            self.prog_name = ("#2DCF27", "bold")

            """OPTIONS DELIMETER"""
            self.f_dxr = " "
            self.s_dxr = "  "

            """COLORS"""
            self.usage_prefix = "#ffffff"
            self.base_args = "#ffffff"
            self.base_comma = "7E7E7E"
            self.base_help = "#BABABA"
            self.base_brackets = "#7E7E7E"
            self.base_req = "#ffffff"
            self.base_metavar = "#ffffff"
            self.base_pipe = "#ffffff"

            self.description = ("#12DD60", "bold")

            self.optional_1 = ("#e7ec84", "bold")
            self.optional_2 = ("#FF5D30", "bold")
            self.help = "#f4f4f4"
        
        def update(self, data: dict):
            self.__dict__.update(data)

    def __init__(self):

        self.com_title = []
        self.com_args = []
        self.styles = self.DefaultStyles()
        self.title_args = []
        self.len_axt = 0
        self.len_args = 0
        self.len_coms = 0
        self.len_caxt = 0
        self.truecolor = self.check_truecolor()
        self.ix = None

    def check_truecolor(self):
        colorterm = os.environ.get("COLORTERM", "").lower()
        if colorterm in ("truecolor", "24bit"):
            return True
        term = os.environ.get("TERM_PROGRAM")
        if term and "Apple_Terminal" in term:
            return False
        else:
            return True

    def com_color(self, value: str | tuple) -> str:
            if isinstance(value, tuple):
                _value = value[0].lstrip('#')
                _fxt_code = self.styles.STYLE_MAP.get(value[1], 0)
            else:
                _value = value.lstrip('#')
                _fxt_code = "0"

            lv = len(_value)
            rgb = tuple(int(_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            if self.truecolor:
                return f'\033[0m\033[{_fxt_code};38;2;{rgb[0]};{rgb[1]};{rgb[2]}m'    
            else:
                return f"\033[{_fxt_code};38;5;{self.conv_rgb_to_256(rgb)}m"


    def conv_rgb_to_256(self, rgb: tuple):
        #convert rgb to 256 color mode
        r, g, b = rgb

        R = min(5, round(r * 6 / 256))
        G = min(5, round(g * 6 / 256))
        B = min(5, round(b * 6 / 256))

        return 16 + 36*R + 6*G + B
    
    def add_arg(self, *args, **kwargs):        
        for x in args:
            if x.startswith("-"):
                pass
            else:
                exit()
        if self._cxk_optional_kwargs(args, kwargs):
            self.com_args.append({args: kwargs})
        else:
            print("error")
            exit()

    def add_com(self, *args, **kwargs):
        _index = kwargs.get("index") if kwargs.get("index") is not None else len(self.com_args)
        #kwargs["name"] = args[0]
        self.com_args.insert(_index, {"Command": {"name": args} | kwargs})

    def add_text(self, text: str, attribut: str | None = None, idt:int = 0, index: int | None = None):
        if attribut:
            rgb_txt = self.com_color(getattr(self.styles, attribut))
            text = f'{rgb_txt}{text}'

        self.com_args.insert(index if index is not None else len(self.com_args), tuple((text, idt)))

    def add_stylegroup(self, name: str, index: int | None = None, indent: int | None = None):
        self.com_args.append({"stylegroup": {"name": name, "index": index, "indentation": indent}})
        self.ix = index
        #self.com_args.append(name)

    def raise_error(self, text: str, notice: str | None = None):
        if notice:
            print(f'{self.com_title[0]} :: \033[0m\033[0;38;2;255;51;51m{notice}\033[0m : {text}')
        else:
            print(f'{self.com_title[0]} :: {text}')

        exit()

    def parse_args(self):

        def _required(_req):
            if not any(b in _tv for b in _req):
                self.raise_error(f'Bad argument [{_tv}]. You should pick between {x[y]["required"]}.', "error")
        
        def _nargs(_narg: int | list, _req: list | None = None):
            #if a_ix-(_tb[0] + _s_args) > _narg:
            if isinstance(_narg, int): 
                if len(_tv) > _narg: # type: ignore
                    self.raise_error(f'Too many arguments {_tv} after [{sys.argv[_tb[0]+1]}]. At most, only [{_narg}] argument{"s are" if _narg != 1 else " is"} allowed.', "error")
            elif isinstance(_narg, list):
                _ix = _req.index(_tv[0])
                if len(_tv) > _narg[_ix]:
                    self.raise_error(f'Too many arguments {_tv} after [{sys.argv[_tb[0]+1]}]. At most, only [{_narg[_ix]}] argument{"s are" if _narg[_ix] != 1 else " is"} allowed.', "error")

        def _compare(dict: dict):
            val = tuple(dict.values())[0]
            if _req := val.get("required", 0):
                _required(_req)
            
            _val = val.get("nargs", 0)
            if isinstance(_val, int):
                _nargs(_val) # If nargs option doesn't exist, set it to zero 
            elif isinstance(_val, list):
                _nargs(_val, _req)

            return True
        
        _parse_args = {}
        _len = len(sys.argv)
        if _len > 1:
            if not sys.argv[1].startswith("-"): # Check command
                for y in self.com_args:
                    if isinstance(y, dict) and "Command" in y.keys():
                        if y["Command"]["name"][0] == sys.argv[1]:
                            _parse_args[sys.argv[1]] = True
                            if _len > 2 and not sys.argv[2].startswith("-"):
                                self.raise_error(f'Bad argument {sys.argv[2:]}', "error")
                            break
                else:
                    self.raise_error(f'Bad argument {sys.argv[1:]}', "error")

            for x in sys.argv[1:]: # Compare user arguments with hard coded arguments
                if x.startswith("-"):
                    for y in self.com_args:
                        if isinstance(y, dict):
                            _keys = list(y.keys())[0]
                            if x in _keys:
                                break
                    else:
                        self.raise_error(f'Bad argument [{x}]', "error")

            
        for x in self.com_args: 
            if isinstance(x, dict):
                for y in x:
                    #if (not y[0].startswith("-") and any(sys.argv[1] in z for z in y)) if len(sys.argv) > 1 else False:
                    if y == "Command":
                        _parse_args.setdefault(x["Command"]["name"][0], False)
                        #for z in y:
                            #_parse_args[z] = True
                    else:
                        _key = [re.sub("^--", "", a) for a in y]
                        _key = [re.sub("-", "_", re.sub("^-", "arg_", a)) for a in _key]
                        _tb = [i for i, arg in enumerate(sys.argv[1:]) if arg in y] # Get index from sys.argv
                        _result = None
                        if _tb:
                            _tv = []
                            for a_ix in range(_tb[0]+2, _len):
                                if not sys.argv[a_ix].startswith("-"):
                                    _tv.append(f'{sys.argv[a_ix]}')
                                else:
                                    break

                            if _tv:
                                if _compare(x):
                                    _result = _tv
                            else:
                                _result = True
                        else:
                            _result = False

                        for z in _key:    
                            _parse_args[z] = _result
                                
        return self.Args(_parse_args)
    def _cxk_optional_kwargs(self, args, kwargs):
        for x in args:
            _check = x.replace("-", "")
            if not _check.isalnum():
                raise Exception(f"Error: [{x}]; an argument should only contain alphanumeric characters.")

        for k,v in kwargs.items():
            if k == "nargs":
                if isinstance(v, int):
                    continue
                if isinstance(v, list):
                    for x in v:
                        if not isinstance(x, int):
                            break
                    else:
                        continue
                raise Exception(f"Error: [{v}]; nargs should be an integer value.")
                
            elif k == "required":
                if isinstance(v, list):
                    for x in v:
                        if not x.isalnum():
                            raise Exception(f"Error: [{v}]; an required element should only contain alphanumeric characters.")
                elif isinstance(v, str):
                    if not v.isalnum():
                            raise Exception(f"Error: [{v}]; an required element should only contain alphanumeric characters.")
                pass
            elif k == "help":
                pass
            elif k == "metavar":
                pass
            else:
                return False
        
        return True
                    
    def style(self, input: list, format: str, opt: None = None):
        if format == "title":
            for x in self.styles.base:
                try:
                    setattr(self, f"rgb_{x[1:]}", self.com_color(getattr(self.styles, format + x))) 
                except Exception:
                    setattr(self, f"t_rgb_{x[1:]}", self.com_color(getattr(self.styles, "base" + x)))  

            l_input = list(input)
            for x in range(0, len(l_input)):
                if l_input[x] in ("[", "(", "{"):
                    l_input[x] = f"{self.rgb_brackets}{l_input[x]}{self.rgb_args}"
                elif l_input[x] in ("]", ")", "}"):
                    l_input[x] = f"{self.rgb_brackets}{l_input[x]}"
                elif l_input[x] in " ":
                    if opt == None:
                        l_input[x] = f"{self.rgb_req} "
                    else:
                        l_input[x] = f"{self.rgb_metavar} "

                elif l_input[x] in "|":
                    l_input[x] = f"{self.rgb_pipe}|{self.rgb_req}"
                    
            return "".join(l_input)

        else:
            for x in self.styles.base:
                try:
                    setattr(self, f"rgb_{x[1:]}", self.com_color(getattr(self.styles, format + x))) 
                except Exception:
                    setattr(self, f"rgb_{x[1:]}", self.com_color(getattr(self.styles, "base" + x)))  

            for y in range(0, len(input)):
                if y == 0:
                    _tmp = list(input[y])
                    for z in range(0, len(_tmp)):
                        if z == 0:
                            _tmp[z] = f'{self.rgb_args}{_tmp[z]}'
                        elif _tmp[z] == ",":
                            _tmp[z] = f'{self.rgb_comma}{_tmp[z]}{self.rgb_args}'
                    
                    input[y] = "".join(_tmp)

                elif y != len(input)-1 and y != 0:
                    _tmp = list(input[y])
                    for z in range(0, len(_tmp)):
                        if _tmp[z] in ("[", "(", "{"):
                            _tmp[z] = f"{self.rgb_brackets}{_tmp[z]}{self.rgb_req}"
                        elif _tmp[z] in ("]", ")", "}"):
                            _tmp[z] = f"{self.rgb_brackets}{_tmp[z]}"
                        elif _tmp[z] in ("|"):
                            _tmp[z] = f"{self.rgb_pipe}{_tmp[z]}{self.rgb_req}"
                        elif z == 0:
                            _tmp[z] = f"{self.rgb_metavar}{_tmp[z]}"

                    input[y] = "".join(_tmp)

                elif y == len(input)-1:                            
                    _tmp = f'{self.rgb_help}{input[y]}'
                    input[y] = _tmp
        
    def print_help(self):
        def fxr_title(self, data):
            if data.get("required"):
                a_title = self.style(f'[{z} {"|".join(data["required"])}]', "title")
            elif data.get("metavar"):
                a_title = self.style(f'[{z} {data["metavar"]}]', "title", 0)
            else:
                a_title = self.style(f'[{z}]', "title")
            return a_title

        def fxr_options(self, data, flag):
            txe_options = []
            _args = ", ".join(y)
            _len_args = len(_args)
            _len_axt = 0
            txe_options.append(_args)

            if data.get("required") and data.get("metavar") is None:
                _req = f'{getattr(self.styles, "f_dxr")}[{"|".join(data["required"])}]'
                _len_axt = len(_req)
                txe_options.append(_req)

            if data.get("metavar"):
                _mvar = f'{getattr(self.styles, "f_dxr")}{data["metavar"]}'
                _len_axt = len(_mvar)
                txe_options.append(_mvar)    

            if data.get("help"):
                txe_options.append(f'{getattr(self.styles, "s_dxr")}{data["help"]}')
            else:
                txe_options.append("")

            if _len_axt > (self.len_axt if flag == 1 else self.len_caxt):
                if flag == 1:
                    self.len_axt = _len_axt
                else:
                    self.len_caxt = _len_axt

            if _len_args > (self.len_args if flag == 1 else self.len_coms):
                if flag == 1:
                    self.len_args = _len_args
                else:
                    self.len_coms = _len_args

            return txe_options
        
        def get_stylegroup_properties(stylegroup):
            style_options = stylegroup["name"]
            if stylegroup["indentation"] is not None:
                com_idt = stylegroup["indentation"]
            else:
                com_idt = 0

            if stylegroup["index"] is not None:
                index = stylegroup["index"]
            else:
                index = 0
            
            return style_options, com_idt, index



        rgb_pnxe = self.com_color(getattr(self.styles, "prog_name"))
        _prog_name = f"{rgb_pnxe}{self.com_title[0]}"
        rgb_dtxt = self.com_color(getattr(self.styles, "description"))
        _description = f"{rgb_dtxt}{self.com_title[1]}"
        print_out, _options = {}, []
        _count, _xcount, ticker = 0, 0, 0 
        style_options, index = None, 0

        for _ in range(0, sum(isinstance(x, dict) and ("stylegroup" in x) for x in self.com_args)+1):
            for x in range(_count, len(self.com_args)):
                if isinstance(self.com_args[x], dict):
                    y = tuple(self.com_args[x].keys())[0]
                    if y == "Command": # Commands
                        y = self.com_args[x]["Command"]["name"]
                        #_options.insert(len(_options), fxr_options(self, self.com_args[x]["Command"], 0))
                        _options.append(fxr_options(self, self.com_args[x]["Command"], 0)) 
                    elif y == "stylegroup":
                        style_options, com_idt, index = get_stylegroup_properties(self.com_args[x]["stylegroup"])
                        ticker += 1
                        _count=x+1
                        break
                    else:
                        for z in y:
                            if z.startswith("-") and not z.startswith("--"):
                                self.title_args.append(fxr_title(self, self.com_args[x][y])) # Title
                                _options.append(fxr_options(self, self.com_args[x][y], 1)) # Arguments
                            """elif not z.startswith("-"):
                                _options.append(fxr_options(self, self.com_args[x][y], 0)) # Commands"""
                elif isinstance(self.com_args[x], tuple):
                    _options.append(tuple(self.com_args[x]))
                    

            
            for x in range(0, len(_options)): #space alignement between columns. apply indentation
                if isinstance(_options[x], list):
                    # add_arg
                    len_args  = self.len_args if _options[x][0].strip().startswith("-") else self.len_coms
                    len_axt = self.len_axt if _options[x][0].strip().startswith("-") else self.len_caxt

                    _len_args = len(_options[x][0])
                    if len(_options[x]) == 3:
                        _lt = len(_options[x][1])
                        _options[x][0] = f'{" "*com_idt}{_options[x][0]}{" "*(len_args-_len_args)}'
                        _options[x][1] = f'{_options[x][1]}{" "*(len_axt-_lt)}'
                    elif len(_options[x]) == 2:
                        _options[x][0] = f'{" "*com_idt}{_options[x][0]}{" "*(len_args-_len_args+len_axt)}'
                    else:
                        _options[x][0] = f'{" "*com_idt}{_options[x][0]}'

                else: #add_text
                    _options[x] = (f'{" "*_options[x][1]}{_options[x][0]}') 

            for x in range(0, len(_options)): # apply style
                if isinstance(_options[x], list):
                    self.style(_options[x], style_options)
            else:
                if index in print_out:
                    print_out[index] = print_out[index] + _options
                else:
                    print_out[index] = _options
                
                _options = []
                _xcount = _count-ticker
                self.len_axt, self.len_caxt, self.len_args, self.len_coms = 0, 0, 0, 0

        print_out.setdefault(0, [])
        print_out[0].insert(0, f'\n{self.com_color(getattr(self.styles, "usage_prefix"))}Usage: {_prog_name} {"".join(self.title_args)}\n')
        print_out[0].insert(1, f'{_description}\n')

        for x in sorted(print_out):
            for y in print_out[x]:
                print("".join(y))

        else:
            print("\033[0m")

        exit()

class SubCommander(Commander): 
    def __init__(self, parents=None):
        super().__init__()
        if parents:
            self.com_args = parents.com_args[:]
            self.com_title = parents.com_title[:]
            self.len_axt = 0
            self.len_args = 0
            self.len_caxt = 0
            self.len_coms = 0
            self.styles = parents.styles
