## Status Codes

~

<table align="right">
    <thead>
        <tr>
            <th align="center">$${\color{gray}Code}$$</th>
            <th align="center">$${\color{gray}Reason}$$</th>
            <th align="center">$${\color{gray}Depend On}$$</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><i>2</i></td>
            <td align="center">Target player is not running.</td> 
            <td align="right">DBUS-MPRIS</td> 
        </tr>
        <tr>
            <td align="left"><i>3</i></td>
            <td align="center">Target player don't support „dynamic refreshment". </td>
            <td align="right">DBUS-MPRIS</td>           
        </tr>
        <tr>
            <td align="left"><i>4</i></td>
            <td align="center">Something went wrong with the module „requests"</td>       
            <td align="right">requests</td>           
        </tr>
        <tr>
            <td align="left"><i>5</i></td>
            <td align="center">Something went wrong calling the sqlite3 database. Maybe corrupt?</td>  
            <td align="right">sqlite3</td>           
        </tr>
        <tr>
            <td align="left"><i>204</i></td>
            <td align="center">Player has not started or a song has yet not played. Playing a song will fix it.</td> 
            <td align="right">Spotify-API</td>     
        </tr>
        <tr>
            <td align="left"><i>400</i></td>
            <td align="center">If synced lyric in the database is not available, we check after a day(24h) again at lrclib. If again there is nothing avaialable this status code will appear.</td> 
            <td align="right">sqlite3</td>     
        </tr>
        <tr>
            <td align="left"><i>401</i></td>
            <td align="center">Access Token can't be refreshed.</td> 
            <td align="right">Spotify-API</td>     
        </tr>
        <tr>
            <td align="left"><i>404</i></td>
            <td align="center">No lyrics available for target song.</td>       
            <td align="right">lrclib/sqlite3</td>      
        </tr>
        <tr>
            <td align="left"><i>404</i></td>
            <td align="center">There are partial data available at lrclib, but no synced lyric for this song.</td>       
            <td align="right">lrclib</td>      
        </tr>
        <tr>
            <td align="left"><i>503</i></td>
            <td align="center">No internet connection available </td>       
            <td align="right">requests</td>      
        </tr>
    </tbody>
</table>

If another status code appears, don't be scared it is mostly a HTTP status codes and can be determined [here](https://docs.python.org/3/library/http.html#http-status-codes).


