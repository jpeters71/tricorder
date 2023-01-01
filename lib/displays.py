from machine import Pin, I2C, PWM, SPI
import st7789
import gc
import gc9a01
import lib.tft_config as tft_config
from utime import sleep
import random
import math


TRIANGLE_HALF_HEIGHT = 4
TRIANGLE_WIDTHS = [9, 7, 5, 3, 0]
MED_RESP_X = 156
MED_RESP_Y = 48
MED_PULSE_X = 156
MED_PULSE_Y = 100
MED_RADIUS = 12


class Wave:
    def __init__(self, max_deviation: int, start_height: int, num_points: int, step_size: int, color: int):
        super().__init__()
        self.max_deviation = max_deviation
        self.pts = [start_height] * num_points
        self.color = color
        self.step_size = step_size


class Triangle:
    def __init__(self, mid_height: int, random_range: int, start_x: int):
        super().__init__()
        self.mid_height = mid_height
        self.current_height = mid_height
        self.random_range = random_range
        self.start_x = start_x
        self.rand_range_min = mid_height - int(random_range / 2)
        self.rand_range_max = mid_height + int(random_range / 2)


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

    def show_starfleet_logos(self):
        gc.collect()
        self.top_disp.jpg('media/starfleet_logo_320x240.jpg', 0, 0, st7789.SLOW)
        self.circ_disp.jpg('media/starfleet_logo_240x240.jpg', 0, 0, gc9a01.SLOW)
        gc.collect()

    def start_medical_scan(self):
        gc.collect()
        # Start with the initial state
        self.top_disp.jpg('media/medical_display_320x240.jpg', 0, 0, st7789.SLOW)
        self.circ_disp.fill_rect(0, 0, 240, 240, st7789.BLACK)
        gc.collect()

        # Create the triangles
        self.tris = self._create_triangles()
        self._render_tris(st7789.WHITE)
        self.med_scan_cnt = 0

        # Create the wave
        self.med_waves = self._create_med_waves()

    def step_medical_scan(self):
        # Increment med scan count        
        if self.med_scan_cnt > 99:
            self.med_scan_cnt = 0
        self.med_scan_cnt += 1

        # Start by clearing the old triangles
        self._render_tris(st7789.BLACK)

        # Update triangle positions
        for tri in self.tris:
            tri.current_height = random.randint(tri.rand_range_min, tri.rand_range_max)
        
        # Draw new triangles
        self._render_tris(st7789.WHITE)

        # Clear waves
        self._render_waves(self.med_waves, self.circ_disp, True)
        self._increment_waves(self.med_waves)
        self._render_waves(self.med_waves, self.circ_disp, False)

        # Check to see if we need to update the respiration
        if self.med_scan_cnt % 3 == 0:
            # Update respiration
            if self.med_scan_cnt % 2 == 0:
                color = st7789.BLACK
            else:
                color = st7789.RED
            self.draw_circle(MED_RESP_X, MED_RESP_Y, MED_RADIUS, color)

        # Check to see if we need to update the pulse
        if self.med_scan_cnt % 2 == 0:
            # Update respiration
            if self.med_scan_cnt % 4 == 0:
                color = st7789.BLACK
            else:
                color = st7789.RED
            self.draw_circle(MED_PULSE_X, MED_PULSE_Y, MED_RADIUS, color)


    def draw_circle(self, x, y, r, color):
        self.top_disp.hline(x-r, y, r*2, color)
        for i in range(1,r):
            a = int(math.sqrt(r*r-i*i)) # Pythagoras!
            self.top_disp.hline(x-a, y+i, a*2, color) # Lower half
            self.top_disp.hline(x-a, y-i, a*2, color) # Upper half

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

    def _create_triangles(self):
        tris = [
            Triangle(mid_height=103, random_range=20, start_x=51),
            Triangle(mid_height=105, random_range=50, start_x=85),
            Triangle(mid_height=107, random_range=57, start_x=131),

            Triangle(mid_height=100, random_range=62, start_x=199),
            Triangle(mid_height=96, random_range=68, start_x=236),
            Triangle(mid_height=103, random_range=52, start_x=281),
        ]
        return tris

    def _render_tris(self, color: int):
        for tri in self.tris:
            # Calculate starting point
            start_x = tri.start_x
            curr_offset = 0
            max_width = TRIANGLE_WIDTHS[0]

            for idx, width in enumerate(TRIANGLE_WIDTHS):
                self.top_disp.hline(start_x + (max_width - width), tri.current_height - idx, width, color)
                if idx > 0:
                    self.top_disp.hline(start_x + (max_width - width), tri.current_height + idx, width, color)

    def _render_waves(self, waves, disp, clear, bg_color=st7789.BLACK):
        for wave in waves:
            if clear:
                color = bg_color
            else:
                color = wave.color
            for idx, pt in enumerate(wave.pts):
                if idx > 0:
                    disp.line((idx - 1) * wave.step_size, wave.pts[idx-1], idx * wave.step_size, pt, color)

    def _increment_waves(self, waves):
        for wave in waves:
            for idx, pt in enumerate(wave.pts):
                new_y = pt + random.randint(-wave.max_deviation, wave.max_deviation)
                wave.pts[idx] = new_y


    def _create_med_waves(self):
        waves = [
            Wave(5, 120, 120, 2, st7789.WHITE)
        ]
        return waves

