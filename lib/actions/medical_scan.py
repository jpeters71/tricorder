import _thread
import gc
import math
import random

from lib.actions import Action
from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays

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


class MedicalScanAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel):
        super().__init__(disps, audio, ctrl_panel)
        self.thread = None

    def start(self):
        self.start_medical_scan()
        #self.thread = _thread.start_new_thread(self.audio.play_wave_file, ('media/tos_tricorder_scan.wav',))

    def step(self):
        self.step_medical_scan()

    def stop(self):
        self.audio.keep_playing = False

    def start_medical_scan(self):
        gc.collect()        
        # Start with the initial state
        self.disps.top_disp.jpg('media/medical_display_320x240.jpg', 0, 0, Displays.TOP_DISP_JPG_SLOW)
        self.disps.circ_disp.fill_rect(0, 0, 240, 240, Displays.BLACK)
        gc.collect()

        # Create the triangles
        self.tris = self._create_triangles()
        self._render_tris(Displays.WHITE)
        self.med_scan_cnt = 0

        # Create the wave
        self.med_waves = self._create_med_waves()

    def step_medical_scan(self):
        # Increment med scan count        
        if self.med_scan_cnt > 99:
            self.med_scan_cnt = 0
        self.med_scan_cnt += 1

        # Start by clearing the old triangles
        self._render_tris(Displays.BLACK)

        # Update triangle positions
        for tri in self.tris:
            tri.current_height = random.randint(tri.rand_range_min, tri.rand_range_max)
        
        # Draw new triangles
        self._render_tris(Displays.WHITE)

        # Clear waves
        self._render_waves(self.med_waves, True)
        self._increment_waves(self.med_waves)
        self._render_waves(self.med_waves, False)

        # Check to see if we need to update the respiration
        if self.med_scan_cnt % 3 == 0:
            # Update respiration
            if self.med_scan_cnt % 2 == 0:
                color = Displays.BLACK
            else:
                color = Displays.RED
            self._draw_circle(MED_RESP_X, MED_RESP_Y, MED_RADIUS, color)

        # Check to see if we need to update the pulse
        if self.med_scan_cnt % 2 == 0:
            # Update respiration
            if self.med_scan_cnt % 4 == 0:
                color = Displays.BLACK
            else:
                color = Displays.RED
            self._draw_circle(MED_PULSE_X, MED_PULSE_Y, MED_RADIUS, color)

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
            max_width = TRIANGLE_WIDTHS[0]

            for idx, width in enumerate(TRIANGLE_WIDTHS):
                self.disps.top_disp.hline(start_x + (max_width - width), tri.current_height - idx, width, color)
                if idx > 0:
                    self.disps.top_disp.hline(start_x + (max_width - width), tri.current_height + idx, width, color)

    def _render_waves(self, waves, clear, bg_color=Displays.BLACK):
        for wave in waves:
            if clear:
                color = bg_color
            else:
                color = wave.color
            for idx, pt in enumerate(wave.pts):
                if idx > 0:
                    self.disps.circ_disp.line((idx - 1) * wave.step_size, wave.pts[idx-1], idx * wave.step_size, pt, color)

    def _increment_waves(self, waves):
        for wave in waves:
            for idx, pt in enumerate(wave.pts):
                new_y = pt + random.randint(-wave.max_deviation, wave.max_deviation)
                if new_y > 150 or new_y < 90:
                    new_y = 120
                wave.pts[idx] = new_y

    def _draw_circle(self, x, y, r, color):
        self.disps.top_disp.hline(x-r, y, r*2, color)
        for i in range(1,r):
            a = int(math.sqrt(r*r-i*i)) # Pythagoras!
            self.disps.top_disp.hline(x-a, y+i, a*2, color) # Lower half
            self.disps.top_disp.hline(x-a, y-i, a*2, color) # Upper half

    def _create_med_waves(self):
        waves = [
            Wave(5, 120, 120, 2, Displays.WHITE)
        ]
        return waves
