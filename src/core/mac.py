import os
import subprocess
class AScript():

    def __init__(self, player):
        self.ix = None
        player = player
        self.get_all = (
            f'tell application "{player}" '
            f'to get {{duration of current track, '
            f'artist of current track, '
            f'name of current track}}'
        )

        self.get_pos = (
            f'tell application "{player}" '
            f'to get {{id of current track, player position}}'
        )

    def get_track_data(self, past_id: str | int | None):
        try:
            data = subprocess.check_output(
                ["osascript", "-e", self.get_pos],
                stderr=subprocess.STDOUT,  
                text=True                   
            ).strip().split(",")
            if past_id != data[0]:
                _data = subprocess.check_output(
                ["osascript", "-e", self.get_all],
                    stderr=subprocess.STDOUT,  
                    text=True                   
                ).strip().split(",")
                return data[0], float(data[1]) * 1_000.0, float(_data[0]), str(_data[1].replace(" ", "+")), str(_data[2].replace(" ", "+"))
            else:
                time_pos = float(data[1]) * 1_000.0
                return data[0], time_pos
        except subprocess.CalledProcessError:
            return 2
