from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
import winrt.windows.foundation.collections
import asyncio
import time

class Wmc():

    def __init__(self, session):
        if not isinstance(session, bool):
            if not self.in_event_loop():
                self.on_media(session, None)
            self.on_playback(session, None)
            self.on_timeline(session, "init")
            session.add_timeline_properties_changed(self.on_timeline)
            session.add_media_properties_changed(self.on_media)
            session.add_playback_info_changed(self.on_playback)

    def on_media(self, sender, args):
        asyncio.run(self.get_media_props(sender))
    def on_timeline(self, sender, args):
        if self.pb_state or args == "init":
            timeline = sender.get_timeline_properties()
            self.timesync = time.perf_counter()
            self.position = float(timeline.position.total_seconds()*1000)

    def on_playback(self, sender, args):
        pb_info = sender.get_playback_info()
        if pb_info.playback_status.name == "PLAYING":
            self.pb_state = True
            timeline = sender.get_timeline_properties()
            self.timesync = time.perf_counter()
            self.position = float(timeline.position.total_seconds()*1000)
        else:
            self.pb_state = False
    def in_event_loop(self):
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False

    @classmethod
    async def create(cls, player):
        cls.player = player
        cls.manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        session = cls.get_session(cls, player, cls.manager)
        if session:
            cls.status = True
            cls.session = session
            await cls.get_media_props(cls, session)
            return cls(session)
        else:
            cls.status = False
            return cls(cls.status)
    
    def get_session(self, player, manager):
        sessions = manager.get_sessions()
        session = next((x for x in sessions if player in x.source_app_user_model_id), None)
        return session

    async def get_media_props(self, session):
        try:
            player_metadata = await session.try_get_media_properties_async()
            self.artist = player_metadata.artist
            self.title = player_metadata.title
            _timeline = session.get_timeline_properties()
            self.track_len = _timeline.end_time.total_seconds()*1000
            self.new_track = True
        except Exception:
            pass
        
    def get_track_data(self, past_id: bool | None):

        try:
            pb_info = self.session.get_playback_info()
            if pb_info.controls.is_play_enabled == False and pb_info.controls.is_pause_enabled == False: # Player is not running
                raise(Exception)
        except Exception:
            self.session = self.get_session(self.player, self.manager)
            if self.session:
                self.__init__(self.session)
                pb_info = self.session.get_playback_info()
            else:
                return 2
                
        if pb_info.playback_status.name == "PLAYING":
            self.delta_timesync = float(self.position+((time.perf_counter()-self.timesync)*1000)) 
        else:
            self.delta_timesync = self.position

        if self.delta_timesync > self.track_len:
            self.delta_timesync = self.track_len 

        if self.new_track:
            past_id = True if past_id == False else False
            self.new_track = False
            if self.track_len == self.position:
                return 3
            return past_id, float(self.delta_timesync), float(self.track_len), str(self.artist.replace(" ", "+")), str(self.title.replace(" ", "+"))
        
        else:
            return past_id, float(self.delta_timesync)
        
class PPlayers():
    async def print_session(self):
        manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        sessions = manager.get_sessions()
        return sessions
    
    def player(self):
        sessions = asyncio.run(self.print_session())
        for x in sessions:
            print(x.source_app_user_model_id)
