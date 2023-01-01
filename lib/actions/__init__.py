from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays


class Action():
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel, step_delay: float = .25):
        self.disps = disps
        self.audio = audio
        self.ctrl_panel = ctrl_panel
        self.step_delay = step_delay

    def start(self):
        pass

    def step(self):
        pass

    def stop(self):
        pass
