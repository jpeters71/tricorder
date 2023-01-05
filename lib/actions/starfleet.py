from lib.actions import Action
from lib.audio import Audio
from lib.audio_notes import Notes
from lib.control_panel import ControlPanel
from lib.displays import Displays
import gc

class StarfleetAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel, step_delay = 1):
        super().__init__(disps, audio, ctrl_panel)

    def start(self):
        self.show_starfleet_logos()
        self.play_star_trek_song()
    def step(self):
        pass

    def stop(self):
        pass

    def show_starfleet_logos(self):
        gc.collect()
        self.disps.top_disp.jpg('media/starfleet_logo_320x240.jpg', 0, 0, Displays.TOP_DISP_JPG_SLOW)
        self.disps.circ_disp.jpg('media/starfleet_logo_240x240.jpg', 0, 0, Displays.TOP_DISP_JPG_SLOW)
        gc.collect()

    def play_star_trek_song(self):
        gc.collect()
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.audio.play_tone(Notes.A3, .75)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED1)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.audio.play_tone(Notes.D4, .25)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.G4, 1.5)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED3)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.audio.play_tone(Notes.F4s, .5)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.audio.play_tone(Notes.D4, .333)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED1)
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.audio.play_tone(Notes.B3, .333)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED1)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.audio.play_tone(Notes.E4, .333)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.A4, .75)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED3)
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.A4, .25)
        gc.collect()
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.C5s, 1.0)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED1)
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_off(ControlPanel.LED3)
        gc.collect()

        self.audio.mute()
