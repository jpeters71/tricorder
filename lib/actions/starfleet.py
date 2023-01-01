from lib.actions import Action
from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays


class StarfleetAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel, step_delay = 1):
        super().__init__(disps, audio, ctrl_panel)

    def start(self):
        self.disps.show_starfleet_logos()
        self.audio.play_star_trek_song(self.ctrl_panel)

    def step(self):
        pass

    def stop(self):
        pass
