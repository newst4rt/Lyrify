## Status Codes



A list of status codes that may appear when something goes wrong:

<table align="center">
    <thead>
        <tr>
            <th align="center">$${\color{gray}Code}$$</th>
            <th align="center">$${\color{gray}Reason}$$</th>
            <th align="center">$${\color{gray}Depend On}$$</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><b>2</b></td>
            <td align="left">Target player is not running.</td> 
            <td align="left">DBUS-MPRIS</td> 
        </tr>
        <tr>
            <td align="left"><b>3</b></td>
            <td align="left">The target player isn't supported. </td>
            <td align="left">DBUS-MPRIS</td>           
        </tr>
        <tr>
            <td align="left"><b>4</b></td>
            <td align="left">An error occurred in „urllib.requests".</td>       
            <td align="left">requests</td>           
        </tr>
        <tr>
            <td align="left"><b>5</b></td>
            <td align="left">An error occurred while accessing the sqlite3 database – Maybe corrupt?</td>  
            <td align="left">sqlite3</td>           
        </tr>
        <tr>
            <td align="left"><b>6</b></td>
            <td align="left">The total duration difference is too high between playback and retrieved lyric – Maybe bad data at lrclib or artist and title don't match with the current track from your playback? </td>  
            <td align="left">lrclib</td>           
        </tr>
        <tr>
            <td align="left"><b>204</b></td>
            <td align="left">The player has not started, or no song has been played yet – playing a song will fix it.</td> 
            <td align="left">Spotify-API</td>     
        </tr>
        <tr>
            <td align="left"><b>400</b></td>
            <td align="left">Lyrics for the track haven't been found in our SQLite3 database, if `--store-offline` is enabled. Due to possible updates for the track, Lyrify performs a recheck after 24 hours to determine whether synced lyrics are available on Lrclib. The code will be shown after checking on lrclib.net if the synced lyrics are available.</td> 
            <td align="left">sqlite3</td>     
        </tr>
        <tr>
            <td align="left"><b>401</b></td>
            <td align="left">Access Token cannot be refreshed.</td> 
            <td align="left">Spotify-API</td>     
        </tr>
        <tr>
            <td align="left"><b>404</b></td>
            <td align="left">No lyrics available for target song.</td>       
            <td align="left">lrclib/sqlite3</td>      
        </tr>
        <tr>
            <td align="left"><b>422</b></td>
            <td align="left">There are partial data available on Lrclib, but no synced lyrics for this song.</td>       
            <td align="left">lrclib</td>      
        </tr>
        <tr>
            <td align="left"><b>503</b></td>
            <td align="left">No internet connection available.</td>       
            <td align="left">requests</td>      
        </tr>
    </tbody>
</table>
<br>

If another status code appears, don't worry — it's most likely a HTTP status code and can be determined [here](https://docs.python.org/3/library/http.html#http-status-codes).


