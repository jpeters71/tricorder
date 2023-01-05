from machine import Pin, I2C, PWM, SPI
from time import sleep, ticks_ms
from lib.control_panel import ControlPanel
from wavePlayer import wavePlayer
import gc




class Audio():
    def __init__(self):
        self.power_pin = Pin(1, mode=Pin.OUT)
        self.power_pin.high()
        self.audio_pin = PWM(Pin(2))
        self.sd_pin = Pin(3)
        self.keep_playing = False

    def play_tone(self, frequency: int, duration: float, volume: int=800):
        self.audio_pin.duty_u16(volume)
        self.audio_pin.freq(frequency)
        sleep(duration)
        self.audio_pin.duty_u16(0)

    def mute(self):
        self.audio_pin.duty_u16(0)
        self.sd_pin.low()


    def play_wave_file(self, wave_file: str):
        gc.collect()
        player = wavePlayer(leftPin=Pin(2), rightPin=Pin(6), virtualGndPin=Pin(4))

        try:
            self.keep_playing = True
            idx = 0
            while self.keep_playing and idx < 5:
                player.play(wave_file)
                idx += 1
        except KeyboardInterrupt:
            player.stop()
        gc.collect()
        self.mute()

    def stop_playing(self):
        self.keep_playing = False

