import time
import dbus

class Mpris():
    
    def __init__(self, player):
        self.player = player
        _code = self.init_dbus(player)

    def init_dbus(self, player):
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
                artist = str(player_metadata_track["xesam:artist"][0])
                title = str(player_metadata_track["xesam:title"])
                ix = artist+title
                if past_id != ix:
                    
                    track_len = float(player_metadata_track["mpris:length"]) #microseconds
                    position_µs = float(self.player_metadata.Get("org.mpris.MediaPlayer2.Player", "Position")) #microseconds
                    if track_len == position_µs:
                        return 3
                        #raise Exception(f"The current player {dbus_player} is not supported. There is an issue with getting the current track position.")
                    return ix, float(position_µs / 1_000.0), float(track_len / 1_000.0), str(artist.replace(" ", "+")), str(title.replace(" ", "+"))
                
                else:
                    position_µs = float(self.player_metadata.Get("org.mpris.MediaPlayer2.Player", "Position")) #microseconds
                    return ix, float(position_µs / 1_000.0)

            except (dbus.exceptions.DBusException, AttributeError) as e:
                    self.init_dbus(self.player)
            except KeyError:
                 title = str(player_metadata_track["xesam:title"])
                 # amazon music, spotify ad.
                 if title in ("Amazon Music", "Advertisement"):  
                    return "📣"
        else:
            return 2

