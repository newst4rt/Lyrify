
<div align="center">
<h1>Lyrify<br></h1>
A lightweight Python application for displaying synchronized lyrics in the terminal, optionally with translation and offline storage, via the <a href="https://lrclib.net">Lrclib API</a>.
<br></br>
<img src="https://github.com/user-attachments/assets/4eb25559-4c81-4266-93d4-8ffa54b76c06" width="70%"></img>
<br></br>


[![License MIT](https://img.shields.io/badge/License-MIT-blue)](#)<br><br>
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](#)&nbsp;&nbsp;[![Windows](https://img.shields.io/badge/Windows-003054)](#)&nbsp;&nbsp;[![macOS](https://img.shields.io/badge/macOS-343d46?logoColor=F0F0F0)](#)&nbsp;&nbsp;[![Python](https://img.shields.io/badge/Python-%3E3.10-s?style=plastic&logo=python&logoColor=white&labelColor=3776AB&color=3a4c7a)](#)&nbsp;&nbsp;[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#) 
</div>

## Table of Contents
- [Introduction](#introduction)
  - [How Lyrify Started](#how-lyrify-started)
  - [Why Lyrify ?](#why-lyrify-)
  - [Python Dependencies](#python-dependencies)
  - [Feature Request](#feature-request)
- [Installation](#installation)
- [Get Started](#get-started)
  - [Initializing](#initializing)
  - [Start ~ Print Modes](#start--print-modes)
  - [Status Handler](#status-handler)
- [Options](#options)
  - [Core Options](#core-options)
  - [Default Options](#default-options)
- [Credits](#credits)
- [License](#license)




## Introduction

### How Lyrify Started 

It began with a similar application that no longer worked. Since there was no suitable replacement, I decided to look into what had changed to fix the issue by myself.

First, I discovered that Spotify provides a separate, undocumented endpoint to get lyrics from Musixmatch, and they changed the authentication method for using it. After digging deeper into my research, it turns out that using the endpoint with unauthorized applications could raise to legal concerns (see [this](https://stackoverflow.com/a/73853859)). For this reason, I intended to avoid the API and sought a replacement and found Lrclib.net.

Lrclib.net provides versatile and relatively qualitatively good data without requiring authentication. Moreover, the project is open source, and there is a GitHub repo ([here](https://github.com/tranxuanthang/lrclib)) available. All the aforementioned points made me decide to set Lrclib as my first choice — and I'm glad I did.

That was the moment when the project marked the beginning of **Lyrify**. It started as a simple application, without any options, featuring just a simple print output, and evolved over time into a software with some useful features. 

### Why Lyrify ?

Lyrify is built in Python3, and most of its modules rely on the Python standard library, which makes it lightweight in terms of dependencies. The application follows a modular design with a dynamic load — only necessary components will be loaded into the program. All common operating systems such as Linux, Windows and macOS are fully supported included full width characters like kanji, kana and aside from that, many customizable options are present to improve the user's experience. 

<table align="right">
    <thead>
        <tr>
            <th align="center">$${\color{gray}Features}$$</th>
            <th align="center">$${\color{gray}Status}$$</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><i>LRCLIB.net API</i></td>
            <td align="center">$${\color{green}✓}$$</td> 
        </tr>
        <tr>
        <tr>
            <td align="left"><i>Spotify API</i></td>
            <td align="center">$${\color{green}✓}$$</td>           
        </tr>
        <tr>
            <td align="left"><i>Store Lyrics Offline</i></td>
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
          <tr>
            <td align="left"><i>Offline Romanizer</i></td>
            <td align="center">$${\color{green}✓}$$</td>        
        </tr>
    </tbody>
</table>

### Python Dependencies 

- [dbus-python](https://pypi.org/project/dbus-python/) 
- [pywinrt](https://github.com/pywinrt/pywinrt)
- [googletrans](https://github.com/ssut/py-googletrans)
- [requests](https://github.com/psf/requests)
- [uroman](https://github.com/isi-nlp/uroman)
- [Commander](https://github.com/newst4rt/Commander)


### Feature Request

The application is currently in development. New features may be added over time. If your desired feature is not listed, feel free to open an issue. If it makes sense and I have time, I may add it.<br>

## Installation

```bash
pip3 install .
```
## Get Started
        
### Initializing

Lyrify retrieves playback information through the system’s native API, by default – user configuration are not required. Furtheremore, the current playback can be retrieved by the Spotify-API with a required online connection. Here's a simple instruction how to do that:

 - *First, use this command to initialize the setup dialog.*
   ```bash
   python3 main.py --init spotify
   ```
 - *Second, follow the instructions how to get your credentials.*
 - *After them, fill the terminal with the required data.*

If everything goes well, a message with the text `Authentication succeeded` will be displayed. Lyrify has successfully applied your credential and is now ready to get in touch with your playback. To use it, simply add the argument `--mode spotify`.

#### *Using an Alternative Music Player Instead of Spotify*

Any music player that uses the system's native media API should work. To check whether your player is supported, follow these instruction:

 - Display all running music players.
    ```bash
    python3 main.py --print-players 
    ```
 - Pass the session name as second argument after the `--mode` parameter.
   ```bash
   python3 main.py --mode [dbus|wmc|ascript] <session> 
   ```

<br>  

Using a different player instead of Spotify may not work with all media players. It mostly depends on how accurately the data are transmitted to the target interface. The functionality cannot be guaranteed. 


### Start ~ Print Modes

There are three different methods to display lyrics on the terminal. 

- ***Default*** : *display lyrics in full-screen on your terminal with automatic scrolling and highlighting.*
  ```bash
  python3 main.py
  ```

- ***Stream*** : *print it as a stream to stdout.*
  ```bash
  python3 main.py stream
  ```
  
- ***Interactive*** : *show the lyrics in one line and refresh them dynamically.*
  ```bash
  python3 main.py interactive
  ```

### Status Handler

Predefined status codes are appearing if something goes wrong. This feature make it easy to detect and handle issues during runtime. Codes and their description can be found [here](docs/status_codes.md).


## Options
Options are organized into different categories to accommodate the various states and their operational behaviours. 
<br>

### Core Options

  Available across all print states.
  - #### **`-m --mode`**

     *Choose from an interface how to get the playback either from any media player or from Spotify by default.*

     - **`--mode [dbus|dbus <player>]`** <sub><sup><a href=""><img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black&style=plastic" width=40></img></a></sup></sub>
       
       ***Linux**: get the current playback with D-BUS – MPRIS.* 

     - **`--mode [wmc|wmc <player>]`**   <sub><sup><a href=""><img src="https://img.shields.io/badge/Windows-003054" width=40></img></a></sup></sub> 

       ***Windows**: retrieve the current playback through the Windows-Runtime-API.*

     - **`--mode [ascript|ascript <player]`** <sub><sup><a href=""><img src="https://img.shields.io/badge/macOS-343d46?logoColor=F0F0F0" width=35></img></a></sup></sub>

        ***macOS**: use AppleScript to get the current playback.*  

     - **`--mode spotify`** <sub><sup><a href=""><img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black&style=plastic" width=40></img></sup></sub> <sub><sup><img src="https://img.shields.io/badge/Windows-003054" width=40></img>  <img src="https://img.shields.io/badge/macOS-343d46?logoColor=F0F0F0" width=35></a></sup></sub>

       *Use the public API from Spotify to get your current playback – a stable online connection is required. If the credentials has not been passed yet, an error occurs. To fix the issue use `--init spotify`.*
  


  - #### **`-t --translate`***`<language_code>`*
  
    *Translate the lyrics in your target language – the value of the language code should be defined as [ISO-639](https://cloud.google.com/translate/docs/languages).*
  
  - #### **`-r --romanize`**

    *Romanize lines if lyrics contain characters that can be romanized.<br>
    This option can be used both combined or individually with `--translate` and `--hide-sourcelyrics` whether to romanize the translated or original lyrics. Here are some examples for a better understanding:*


    - **`--translate zh-CN --romanize --hide-sourcelyrics`**

       *Display on the first row the translation and on the second the romanized translation. If translation can't be transliterated, only first row will be displayed.*

    - **`--translate zh-CN --romanize`** 
      
       *Display the romanized lyric and below the translation.*

    -  **`stream --romanize --translate zh-CN`**
    
        *Just display the romanized translation as stream.* 
  
  - #### **`-o --store-offline`**
  
    *Lyrify maintains an SQLite3 database to store downloaded lyrics and translations in its local storage. It reduces transactions between the different endpoints, and it's compatible to use them offline. By applying `--store-offline`, you no longer have to worry about getting the lyrics of your favorite songs. You will always get them – just listen to them one time, and Lyrify will store it.*

  - #### **`-p --print-players`**
    *Display all running music players. More info [here](#using-an-alternative-music-player-instead-of-spotify)*

### Default Options
  *Can only be used in the **default print mode**.*
  - #### `-s --style`
    *Use a style configuration file for changing lyrics' color. For more information take a look [here](docs/style.md)*

  - #### `-0 --hide-sourcelyrics`
    *Hide the displayed source lyrics when translation or romanizing is enabled.* 

## Credits

Greetings to all contributors and everyone who took part in Lyrify:

 - The D-Bus maintainers @ dbus-python
 - The pywinrt maintainers @ pywinrt 
 - SuHun Han @ googletrans
 - Kenneth Reitz @ requests
 - This project uses the universal romanizer software 'uroman' written by Ulf Hermjakob, USC Information Sciences Institute (2015-2020)

  Thank you for providing your projects for the public. Without your efforts Lyrify isn't what it is – you're all awesome ❤️

## License
Lyrify is licensed under the MIT license. See [LICENSE](https://github.com/newst4rt/Lyrify/blob/main/LICENSE) for more information.
