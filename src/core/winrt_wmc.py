from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
import winrt.windows.foundation.collections
from src.core.config import config
import asyncio
import time

class Wmc():

    def __init__(self, session):

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
        else:
            self.pb_state = False

    @classmethod
    async def create(cls):
        manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        sessions = manager.get_sessions()
        session = next((x for x in sessions if "Spotify" in x.source_app_user_model_id), None)
        if session:
            await cls.get_media_props(cls, session)
            cls.on_playback(cls, session, None)
            cls.on_timeline(cls, session, "init")
            return cls(session)

    async def get_media_props(self, session):
        player_metadata = await session.try_get_media_properties_async()
        self.artist = player_metadata.artist
        self.title = player_metadata.title
        _timeline = session.get_timeline_properties()
        self.track_len = _timeline.end_time.total_seconds()*1000
        self.new_track = True
        
    def get_track_data(self, past_id: str | int | None):
            delta_timesync = float(self.position+((time.perf_counter()-self.timesync)*1000)) 
            if delta_timesync > self.track_len:
                delta_timesync = self.track_len 
            if self.new_track:
                self.new_track = False
                past_id += 1
                if self.track_len == self.position:
                    return 3
                return past_id, float(delta_timesync), float(self.track_len), str(self.artist.replace(" ", "+")), str(self.title.replace(" ", "+"))
            
            else:
                return past_id, float(delta_timesync)