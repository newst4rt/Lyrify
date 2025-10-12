
<div align="center">
<h1>Lyrify<br></h1>
A lightweight Python application for displaying synchronized lyrics in the terminal, optionally with translation and offline storage, via the <a href="https://lrclib.net">Lrclib API</a>.
<br></br>
<img src="https://github.com/user-attachments/assets/f1e977a2-a204-4bc9-882a-fffcb10d3138" width="600"></img>
<br></br>
<img alt="License MIT" src="https://img.shields.io/badge/License-MIT-blue"></img>
</div>




## Introduction

### How Lyrify started 

It started with a similar application that no longer worked anymore. I looked for a replacement, but there was nothing what satisfied me. So, I did some research to find out what has been actually changed to fix the issue by myself.

I discovered that Spotify provides a seperat undocumented endpoint to get lyrics from Musixmatch and they changed the authentication method for using this. After digging deeper into my research, it turns out that using this endpoint with unauthorized applications can raise legal concerns (see [this](https://stackoverflow.com/a/73853859)). For this reason, I intend to avoid the API and sought for a replacement that eventually fit and found Lrclib.net.

Lrclib.net provides versatile and relatively qualitavly good data, without requiring authentication. Moreover, the project is opensource and there is a GitHub repo ([here](https://github.com/tranxuanthang/lrclib)) available. All the aforementioned points made me decide to set Lrclib as my first choice, and I'm glad I did.

That was the moment when the project marked the beginning of **Lyrify**. It started as a simple application, without any options, featuring just a simple print output, and evolved over time into a software with some useful features. 


### Why Lyrify ?

Lyrify is built in Python3, and most of its modules rely on the Python standard library, which makes it lightweight in terms of dependencies. Furthermore, the application follows a modular design with a dynamic load which only the necessary components are loaded into the programme. There is a Full-Width Characters support include Kanji, Kana and all other full-width letters and aside from that the status handler helps you to understand if something goes wrong. The Codes can be determined [here](docs/status_codes.md)


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
            <td align="left"><i>DBUS-MPRIS-Support</i></td>
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

## Status Codes

Here is a list of all 

## License
Lyrify is licensed under the MIT license. See [LICENSE](https://github.com/newst4rt/Lyrify/blob/main/LICENSE) for more information.
