from lib.actions import Action
from lib.audio import Audio
from lib.audio_notes import Notes
from lib.control_panel import ControlPanel
from lib.displays import Displays
import gc

class HuskyAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel, step_delay = 1):
        super().__init__(disps, audio, ctrl_panel)

    def start(self):
        # Start by turning off all LEDs
        self.ctrl_panel.leds_on([])
        self.show_logo_ws()
    def step(self):
        pass

    def stop(self):
        pass

    def show_logo_ws(self):
        gc.collect()
        self.disps.top_disp.jpg('media/logo_w_320x240.jpg', 0, 0, Displays.TOP_DISP_JPG_SLOW)
        self.disps.circ_disp.jpg('media/logo_w_240x240.jpg', 0, 0, Displays.TOP_DISP_JPG_SLOW)
        gc.collect()
        self.play_bow_little()

    def play_bow_little(self):
        gc.collect()
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.A3, 1.0)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED3)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.audio.play_tone(Notes.G3, .75)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.audio.play_tone(Notes.F3, .25)
        gc.collect()
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.audio.play_tone(Notes.F3, .40)
        gc.collect()
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.E3, .20)
        self.ctrl_panel.led_off(ControlPanel.LED1)
        self.ctrl_panel.led_off(ControlPanel.LED2)
        self.ctrl_panel.led_off(ControlPanel.LED3)
        gc.collect()
        self.ctrl_panel.led_on(ControlPanel.LED1)
        self.ctrl_panel.led_on(ControlPanel.LED2)
        self.ctrl_panel.led_on(ControlPanel.LED3)
        self.audio.play_tone(Notes.E3, 1.5)
        gc.collect()
        
        self.audio.mute()
