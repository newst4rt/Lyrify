
<div align="center">
<h1>Lyrify<br></h1>
A lightweight Python application for displaying synchronized lyrics in the terminal, optionally with translation and offline storage, via the <a href="https://lrclib.net">Lrclib API</a>.
<br></br>
<img src="https://github.com/user-attachments/assets/d426b46b-cafb-42d7-8d0f-4b12d475f397" width="650"></img>
<br></br>


[![License MIT](https://img.shields.io/badge/License-MIT-blue)](#)<br>
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](#) [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) [![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#)

</div>




## Introduction

### How Lyrify started 

It began with a similar application that no longer worked. Since there was no suitable replacement, I decided to look into what had changed to fix the issue myself.

First, I discovered that Spotify provides a separate, undocumented endpoint to get lyrics from Musixmatch, and they changed the authentication method for using this. After digging deeper into my research, it turns out that using this endpoint with unauthorized applications can raise legal concerns (see [this](https://stackoverflow.com/a/73853859)). For this reason, I intended to avoid the API and sought a replacement and found Lrclib.net.

Lrclib.net provides versatile and relatively qualitatively good data without requiring authentication. Moreover, the project is open source, and there is a GitHub repo ([here](https://github.com/tranxuanthang/lrclib)) available. All the aforementioned points made me decide to set Lrclib as my first choice — and I'm glad I did.

That was the moment when the project marked the beginning of **Lyrify**. It started as a simple application, without any options, featuring just a simple print output, and evolved over time into a software with some useful features. 

### Why Lyrify ?

Lyrify is built in Python3, and most of its modules rely on the Python standard library, which makes it lightweight in terms of dependencies. Furthermore, the application follows a modular design with a dynamic load — only necessary components will be loaded into the program. It supports full width characters, including kanji, kana, and all other full-width letters, and it is rich in features. Aside from that, if something goes wrong, a status handler helps you understand what happened by displaying a status code. 


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
            <td align="left"><i>D-BUS-MPRIS-Support</i></td>
            <td align="center">$${\color{green}✓}$$</td>          
        </tr>
        <tr>
            <td align="left"><i>Spotify API Support</i></td>
            <td align="center">$${\color{green}✓}$$</td>           
        </tr>
        <tr>
            <td align="left"><i>Offline-Storage</i></td>
            <td align="center">$${\color{green}✓}$$</td>     
        </tr>
        <tr>
            <td align="left"><i>Google Translation</i></td>
            <td align="center">$${\color{green}✓}$$</td>          
        </tr>
        <tr>
            <td align="left"><i>Different Display Modes</i></td>
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
  
### Feature Request

If your desired feature is not listed, feel free to open a new issue. If it makes sense and I have time, I may add it.

## Installation

```bash
pip3 install -r requirements.txt
```
## Get Started
        
### Initializing

Lyrify uses the MPRIS D-Bus interface by default to retrieve the current playback. For using D-Bus there is no user configuration required. If you want to get in touch with playbacks from external devices, you can use the Spotify API by set up your API credentials from your account. Here's a simple instruction how to do that:

 - *First, use this command to initialize the setup dialog.*
   ```bash
   python3 main.py --init spotify
   ```
 - *Second, follow the instructions how to get your credentials.*
 - *After them, fill the terminal with the required data.*

If everything goes well, a message with the text `Authentication succeeded` will be displayed. Lyrify has successfully applied the credential and is now ready to get in touch with your playback. To use it, simply add the argument `--mode spotify`.

#### *Using an Alternative Music Player Instead of Spotify*

Lyrify supports any music player that implements the MPRIS D-Bus interface. To check whether your player is supported, follow these instructions:

 - Get the bus-name from your application. 
```bash
python3 -c "import dbus; bus = dbus.SessionBus(); [print(x.replace('org.mpris.MediaPlayer2.', '')) for x in bus.list_names() if x.startswith('org.mpris.MediaPlayer2')]"
```
 - If the player appears, fill the name as positional argument by add them after `--mode dbus`. 
```bash
python3 main.py --mode dbus <name>
```

This feature is experimental and may not work with all players. It mostly depends on how accurately the data is transmitted to D-Bus. 

### Start ~ Print Mode

There are three different methods to display lyrics on the terminal. 

- ***Default*** : *Display lyrics in full-screen on your terminal with automatic scrolling and highlighting.*
  ```bash
  python3 main.py
  ```

- ***Stream*** : *Print it as a stream to stdout.*
  ```bash
  python3 main.py stream
  ```
  
- ***Interactive*** : *Display the lyric in just one row with dynamic refreshment.*
  ```bash
  python3 main.py interactive
  ```

## Options

Options are separated into different categories due to the different print modes and those behaviors. 

### Core Options
  *Core options are useable in all states.*
  - #### **`-m --mode`**

     *Choose from an interface to get the current playback from the player.*
     > **`--mode dbus`** : *apply D-Bus MPRIS.*   
     > **`--mode dbus <name>`** : *apply D-Bus MPRIS with another player instead of Spotify [(more info)](#using-an-alternative-music-player-instead-of-spotify)*  
     > **`--mode spotify`** : *apply the Spotify API.*
  

  - #### **`-t --translate`**
  
    *Translate the lyrics in your target language.*
  
    > **`--translate <language_code>`** : the value of the language code should be defined as [ISO-639](https://cloud.google.com/translate/docs/languages).
  
  - #### **`-0 --store-offline`**
  
    *Lyrify maintains an SQLite3 database to store downloaded lyrics and translations in its local storage. It reduces transactions between the different endpoints, and it's compatible to use them offline. By applying `--store-offline`, you no longer have to worry about getting the lyrics of your favorite songs. You will always get them — just listen to them one time, and Lyrify will store it.*

### Default Options
  *Can only be used in the **default print mode**.*
  - #### `-c --highlight-color`
    *Define how lyrics should be highlighted as RGB color.*

    > **`--highlight-color 255,200,0`** 

## License
Lyrify is licensed under the MIT license. See [LICENSE](https://github.com/newst4rt/Lyrify/blob/main/LICENSE) for more information.
