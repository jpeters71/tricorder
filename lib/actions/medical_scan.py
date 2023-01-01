import _thread

from lib.actions import Action
from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays


class MedicalScanAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel):
        super().__init__(disps, audio, ctrl_panel)
        self.thread = None

    def start(self):
        self.disps.start_medical_scan()
        self.thread = _thread.start_new_thread(self.audio.play_wave_file, ('media/tos_tricorder_scan.wav',))

    def step(self):
        self.disps.step_medical_scan()

    def stop(self):
        self.audio.keep_playing = False
