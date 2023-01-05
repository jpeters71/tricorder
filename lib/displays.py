from machine import Pin, I2C, PWM, SPI
import st7789
import gc
import gc9a01
import lib.tft_config as tft_config
from utime import sleep
import random
import math


class Displays:
    TOP_DISP_JPG_SLOW = st7789.SLOW
    CIRC_DISP_JPG_SLOW = gc9a01.SLOW
    BLACK = st7789.BLACK
    BLUE = st7789.BLUE
    RED = st7789.RED 
    GREEN = st7789.GREEN
    CYAN = st7789.CYAN
    MAGENTA = st7789.MAGENTA
    YELLOW = st7789.YELLOW
    WHITE = st7789.WHITE
    

    def __init__(self):
        gc.collect()  # Precaution before instantiating framebuf
        self.circ_disp = self._init_circ_display()
        self.top_disp = self._init_top_display()
        self.tris = []
        self.med_waves = []

    def _init_circ_display(self) -> gc9a01.GC9A01:
        circ_disp = gc9a01.GC9A01(
            SPI(0, 40_000_000, polarity=1, phase=1, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=None),
            240,
            240,
            reset=Pin(21, Pin.OUT),
            cs=Pin(17, Pin.OUT),
            dc=Pin(20, Pin.OUT),
            rotation=3)
        circ_disp.init()
        return circ_disp

    def _init_top_display(self) -> st7789.ST7789:
        top_disp = tft_config.config(3, buffer_size=64*62*2)
        top_disp.init()
        return top_disp


