from machine import Pin, I2C, PWM, SPI
from utime import sleep
from lib.control_panel import ControlPanel
from wavePlayer import wavePlayer
import gc


A2=110
B2=123
C3=131
C3s=139
D3=147
D3s=156
E3=165
F3=175
F3s=185
G3=196
G3s=208
A3=220
A3s=233
B3=247
C4=262
C4s=277
D4=294
D4s=311
E4=330
F4=349
F4s=370
G4=392
G4s=415
A4=440
A4s=466
B4=494
C5=523
C5s=554
D5=597
D5s=622
E5=659
F5=698

class Audio():
    def __init__(self):
        self.power_pin = Pin(1, mode=Pin.OUT)
        self.power_pin.high()
        self.audio_pin = PWM(Pin(2))
        self.sd_pin = Pin(3)
        self.keep_playing = False

    def _play_tone(self, frequency: int, duration: float, volume: int=800):
        self.audio_pin.duty_u16(volume)
        self.audio_pin.freq(frequency)
        sleep(duration)
        self.audio_pin.duty_u16(0)

    def mute(self):
        self.audio_pin.duty_u16(0)
        self.sd_pin.low()


    def play_star_trek_song(self, ctrl_panel: ControlPanel):
        gc.collect()
        # ctrl_panel.led_on(ControlPanel.LED1)
        # self._play_tone(A3, .75)
        # ctrl_panel.led_off(ControlPanel.LED1)
        # ctrl_panel.led_on(ControlPanel.LED2)
        # self._play_tone(D4, .25)
        # ctrl_panel.led_off(ControlPanel.LED2)
        # ctrl_panel.led_on(ControlPanel.LED3)
        # self._play_tone(G4, 1.5)
        # ctrl_panel.led_off(ControlPanel.LED3)
        # ctrl_panel.led_on(ControlPanel.LED2)
        # self._play_tone(F4s, .5)
        # ctrl_panel.led_off(ControlPanel.LED2)
        # ctrl_panel.led_on(ControlPanel.LED1)
        # self._play_tone(D4, .333)
        # ctrl_panel.led_off(ControlPanel.LED1)
        # ctrl_panel.led_on(ControlPanel.LED1)
        # self._play_tone(B3, .333)
        # ctrl_panel.led_off(ControlPanel.LED1)
        # ctrl_panel.led_on(ControlPanel.LED2)
        # self._play_tone(E4, .333)
        # ctrl_panel.led_off(ControlPanel.LED2)
        # ctrl_panel.led_on(ControlPanel.LED3)
        # self._play_tone(A4, .75)
        # ctrl_panel.led_off(ControlPanel.LED3)
        # ctrl_panel.led_on(ControlPanel.LED3)
        # self._play_tone(A4, .25)
        # ctrl_panel.led_on(ControlPanel.LED1)
        # ctrl_panel.led_on(ControlPanel.LED2)
        # ctrl_panel.led_on(ControlPanel.LED3)
        # self._play_tone(C5s, 1.0)
        # ctrl_panel.led_off(ControlPanel.LED1)
        # ctrl_panel.led_off(ControlPanel.LED2)
        # ctrl_panel.led_off(ControlPanel.LED3)
        gc.collect()

        self.mute()       

    def play_wave_file(self, wave_file: str):
        gc.collect()
        # player = wavePlayer(leftPin=Pin(2), rightPin=Pin(6), virtualGndPin=Pin(4))

        # try:
        #     self.keep_playing = True
        #     idx = 0
        #     while self.keep_playing and idx < 5:
        #         player.play(wave_file)
        #         idx += 1
        # except KeyboardInterrupt:
        #     player.stop()
        gc.collect()
        self.mute()

    def stop_playing(self):
        self.keep_playing = False
