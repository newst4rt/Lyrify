
<div align="center">
<h1>Lyrify<br></h1>
A lightweight Python application for displaying synchronized lyrics in the terminal, optionally with translation and offline storage, via the <a href="https://lrclib.net">Lrclib API</a>.
<br></br>
<img src="https://github.com/user-attachments/assets/f1e977a2-a204-4bc9-882a-fffcb10d3138" width="600"></img>
</div>


## Introduction

The idea of printing lyrics from Spotify in a terminal is not new; there are many projects they are taking the same approach. Lyrify is developed with the idea behind to avoid fetching lyrics directly from Spotify. The project has started first as a simple application, without any options, featuring just a simple print output, and has evolved over the time into a application with some handsome features. 

### Why Lyrify ?

Lyrify is built in Python3, and most of its modules rely on the Python standard library, which makes it lightweight in terms of dependencies. Furthermore, the application follows a modular design with a dynamic load which only the necessary components are loaded into the main thread. Moreover, wide characters like Kanji, Kana, and full-width Latin letters are full supported.
<br></br>
<table align="right">
    <thead>
        <tr>
            <th align="center">$${\color{gray}Features}$$</th>
            <th align="center">$${\color{gray}Status}$$</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><i>LRCLIB.net API-Support</i></td>
            <td align="center">$${\color{green}✓}$$</td> 
        </tr>
        <tr>
            <td align="left"><i>DBUS-Support</i></td>
            <td align="center">$${\color{green}✓}$$</td>          
        </tr>
        <tr>
            <td align="left"><i>Spotify-API Support</i></td>
            <td align="center">$${\color{green}✓}$$</td>           
        </tr>
        <tr>
            <td align="left"><i>Offline-Storage</i></td>
            <td align="center">$${\color{green}✓}$$</td>     
        </tr>
        <tr>
            <td align="left"><i>Google-Translation</i></td>
            <td align="center">$${\color{green}✓}$$</td>          
        </tr>
        <tr>
            <td align="left"><i>Different Print Modes</i></td>
            <td align="center">$${\color{green}✓}$$</td> 
        </tr>
        <tr>
            <td align="left"><i>Wide Character Support</i></td>
            <td align="center">$${\color{green}✓}$$</td>        
        </tr>
    </tbody>
</table>

### Python Dependencies 

- [dbus-python](https://pypi.org/project/dbus-python/)
- [googletrans](https://pypi.org/project/googletrans/)
- [rich-argparse](https://github.com/hamdanal/rich-argparse)
- [requests](https://github.com/psf/requests)
  
### Features

If your desired feature is not listed, feel free to open a new issue. If it makes sense and I have time, I may add it.




## Installation

```bash
pip3 install -r requirements.txt
```

## Usage
```bash
python3 main.py
```

### Options

- **```-m, --mode```**_```dbus|spotify-api```_  _Set the mode how the lyrics from your track should be retrieved_
  - **```--mode```**_```dbus <name>```_ _Use a different music player instead of Spotify_
- **```-p, --print```**_```stream|interactive```_  _Print as stream or interactive (overwrite line)._
- **```-t --translate```**_```language_code```_ _Translate the lyric to your desired language (e.g. 'de' for German, 'en' for English, 'fr' for French, etc.)_
- **```-i --init```**_```spotify```_ _Initialize the API set up for the target music player._
- **```-0 --store-offline```** _Store lyrics locally to use them without an internet connection_
- **```-h --help```** _Display the help message and exit._

## Example

```bash
python3 main.py --mode spotify-api -t de -0
```
Fetch the current playback, translate the lyric to German and store origin and translated lyrics local.


## License
Lyrify is licensed under the MIT license. See [LICENSE](https://github.com/newst4rt/Lyrify/blob/main/LICENSE) for more information.
