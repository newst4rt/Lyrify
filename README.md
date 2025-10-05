
<div align="center">
<h1>Lyrify<br></h1>
A lightweight Python application for displaying synchronized lyrics in the terminal, optionally with translation and offline storage, via the <a href="https://lrclib.net">Lrclib API</a>.
<br></br>
<img src="https://github.com/user-attachments/assets/04e8f13c-f06f-45d4-860d-40eebce5edba" width="600"></img>
</div>


## Introduction

The idea of printing lyrics from Spotify in a terminal is not new; there are many projects that take the same approach. Lyrify was developed to avoid fetching lyrics directly from Spotify. It started as a simple application, without any options, featuring with a simple print stream, and has evolved over time into an application with many new features. 

### Why Lyrify ?

Lyrify is built in Python, and most of its modules rely on the Python standard library, which makes it lightweight in terms of dependencies. Lyrify is still in development and many new features are planned for the future additionaly stability fixes and code refactoring. 

### Dependencies 


- [dbus-python](https://pypi.org/project/dbus-python/)
- [googletrans](https://pypi.org/project/googletrans/)
- [rich-argparse](https://github.com/hamdanal/rich-argparse)
- [requests](https://github.com/psf/requests) 

_Currently, Lyrify works only for Linux._


## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python3 main.py
```

### Options

- **```-m, --mode```**_```dbus|spotify-api```_  _Set the mode how the lyrics from your track should be retrieved_
- **```-p, --print```**_```stream|interactive```_  _Print as stream or interactive (overwrite line)._
- **```-t --translate```**_```language_code```_ _Translate the lyric to your desired language (e.g. 'de' for German, 'en' for English, 'fr' for French, etc.)_
- **```-0 --store-offline```** _Store lyrics locally to use them without an internet connection_
- **```-h --help```** _Display the help message and exit._

## Example

```bash
python3 main.py -p interactive -t de
```

Set the output interactive and translate it to the German language.


## License
Lyrify is licensed under the MIT license. See [LICENSE](https://github.com/newst4rt/Lyrify/blob/main/LICENSE) for more information.
