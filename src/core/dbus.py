import time
import dbus
from src.core.config import player

class Mpris():
    
    def __init__(self):
        _code = self.init_dbus()
        if _code == 2:
             raise Exception(f"There is no player running with the name {player}.") 

    def init_dbus(self):
            session_bus = dbus.SessionBus()
            dbus_names = session_bus.list_names()
            lf_services = [names for names in dbus_names if names.startswith("org.mpris.MediaPlayer2." + player)]
            if not lf_services:
                return 2
            try:
                player_bus = session_bus.get_object(lf_services[0], "/org/mpris/MediaPlayer2")
            except dbus.exceptions.DBusException:
                return 2
            self.player_metadata = dbus.Interface(player_bus, "org.freedesktop.DBus.Properties")
            return 1

    def get_track_data(self, past_id: str | int | None):
        for _ in range(0, 2):
            try:
                player_metadata_track = self.player_metadata.Get("org.mpris.MediaPlayer2.Player", "Metadata")
                ix = str(player_metadata_track["mpris:trackid"]).rindex("/")
                if past_id != ix:
                    artist = str(player_metadata_track["xesam:artist"][0])
                    title = str(player_metadata_track["xesam:title"])
                    track_len = float(player_metadata_track["mpris:length"]) #microseconds
                    position_µs = float(self.player_metadata.Get("org.mpris.MediaPlayer2.Player", "Position")) #microseconds
                    if track_len == position_µs:
                        return 3
                        #raise Exception(f"The current player {dbus_player} is not supported. There is an issue with getting the current track position.")
                    return str(player_metadata_track["mpris:trackid"][ix+1:]), float(position_µs / 1_000.0), float(track_len / 1_000.0), str(artist.replace(" ", "+")), str(title.replace(" ", "+"))
                
                else:
                    position_µs = float(self.player_metadata.Get("org.mpris.MediaPlayer2.Player", "Position")) #microseconds
                    return ix, float(position_µs / 1_000.0)

            except (dbus.exceptions.DBusException, AttributeError) as e:
                    self.init_dbus()
        else:
            return 2

