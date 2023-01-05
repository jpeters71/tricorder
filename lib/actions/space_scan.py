import _thread
import gc
import math 
import random

from lib.actions import Action
from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays


ANGLE_RISE_RUN = [
    (1, 0), # 90
    (15, 4), # 75
    (12, 7), # 60
    (3, 4), # 45
    (26, 15), # 30
    (15, 66), # 15
    (0, 1) # 0
]

QUADRANT = [
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1)
]

class Star():
    def __init__(self, x: int, y: int, rate: int, quadrant: int, angle: int, color: int):
        self.x = x
        self.y = y
        self.rate = rate
        self.quadrant = quadrant
        self.angle = angle
        self.color = color


class SpaceScanAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel):
        super().__init__(disps, audio, ctrl_panel, step_delay = .25)
        self.stars = []
        self.step_cnt = 0

    def start(self):
        gc.collect()
        # Start with the initial state
        self._init_stars()
        self.disps.circ_disp.jpg('media/bluemarble.jpg', 0, 0, Displays.CIRC_DISP_JPG_SLOW)
        gc.collect()
        self.step_cnt = 0
        
    def step(self):
        gc.collect()

    def stop(self):
        pass


    def _init_stars(self):
        self.stars = []

        self._add_stars(10)

    def _add_stars(self, num_stars: int):
        for _ in range(0, num_stars):
            self.stars.append(Star(
                x=160,
                y=120,
                rate=random.randint(1, 5),
                quadrant=random.randint(0, 3),
                angle=random.randint(0, 6),
                color=random.choice([Displays.GREEN, Displays.RED, Displays.WHITE, Displays.YELLOW])
            ))

 b 
    def _draw_grid(self):
        # Draw grid
        horz_start_y = 47
        inc = 30
        vert_start_x = 64
        
        for line_idx in range (0, 5):
            new_y = horz_start_y + (line_idx * inc)
            new_x = vert_start_x + (line_idx * inc)
            self.disps.top_disp.hline(33, new_y, 216, Displays.BLACK)
            self.disps.top_disp.vline(new_x, 16, 200, Displays.BLACK)
        
    def _draw_signals(self, clear):
        # Scanner signals first
        for signal in self.scanner_signals:
            if not clear: 
                if self.step_cnt > 0 and (self.step_cnt % signal.motion_mod) == 0:
                    signal.x = random.randint(signal.bounds[0], signal.bounds[2])
                    signal.y = random.randint(signal.bounds[1], signal.bounds[3])
                color = signal.color
            else:
                color = BACKGROUND_CLR

            if signal.shape == TRIANGLE:
                self._draw_triangle(signal.x, signal.y, color)
            elif signal.shape == CIRCLE:
                self._draw_circle(signal.x, signal.y, 3, color, self.disps.top_disp)


    def _draw_triangle(self, center_x, center_y, color):
        max_height = TRIANGLE_HEIGHTS[0]
        start_y = center_y + int(max_height / 2)

        for idx, height in enumerate(TRIANGLE_HEIGHTS):
            y_pos = start_y - height
            self.disps.top_disp.vline(center_x - idx, y_pos, height, color)
            if idx > 0:
                self.disps.top_disp.vline(center_x + idx, y_pos, height, color)

    def _draw_circle(self, x, y, r, color, disp):
        disp.hline(x-r, y, r*2, color)
        for i in range(1,r):
            a = int(math.sqrt(r*r-i*i)) # Pythagoras!
            disp.hline(x-a, y+i, a*2, color) # Lower half
            disp.hline(x-a, y-i, a*2, color) # Upper half

    def _init_signals(self):
        self.scanner_signals = []
        self.radar_signals = []

        # Start with landing party
        for _ in range(0, random.randint(2, 5)):
            self.scanner_signals.append(self._init_signal(self.LANDING_PARTY_BOUNDS, Displays.GREEN, TRIANGLE))            

        # Next lifeforms
        for _ in range(0, random.randint(2, 7)):
            self.scanner_signals.append(self._init_signal(self.LIFEFORM_BOUNDS, Displays.RED, TRIANGLE))            

        # Next energy sources
        for _ in range(0, random.randint(1, 2)):
            self.scanner_signals.append(self._init_signal(self.ENERGY_SOURCE_BOUNDS, Displays.WHITE, CIRCLE, 7))            

        # Next indeterminate lifeforms 
        for _ in range(0, random.randint(1, 3)):
            self.scanner_signals.append(self._init_signal(self.INDETERMINATE_LIFEFORM_BOUNDS, Displays.YELLOW, TRIANGLE))            

        # Radar signals
        for _ in range(2, random.randint(2, 6)):
            colors = (Displays.RED, 0x5800) if random.randint(0, 1) else (Displays.GREEN, 0x0220)

            self.radar_signals.append(
                RadarSignal(
                    x=random.randint(self.RADAR_BOUNDS[0], self.RADAR_BOUNDS[2]),
                    y=random.randint(self.RADAR_BOUNDS[1], self.RADAR_BOUNDS[3]),
                    bounds=self.RADAR_BOUNDS,
                    motion_mod=0, # Not used
                    bright_color=colors[0],
                    dim_color=colors[1],
                    shape=CIRCLE
                )
            )

    def _init_signal(self, bounds, color, shape, motion_mod = None) -> Signal:
        return Signal(
            x=random.randint(bounds[0], bounds[2]),
            y=random.randint(bounds[1], bounds[3]),
            bounds=bounds,
            motion_mod=(motion_mod if motion_mod else random.randint(1, 5)) * SCAN_STEP_OFFSET,
            color=color,
            shape=shape
        )

    def _update_radar(self):
        self._draw_radar_sweep(True)
        self._draw_polar_grid()
        self._draw_radar_sweep(False)

    def _draw_polar_grid(self):
        self.disps.circ_disp.line(0, 0, 240, 240, POLAR_GRID_CLR)
        self.disps.circ_disp.line(240, 0, 0, 240, POLAR_GRID_CLR)
        self.disps.circ_disp.vline(120, 0, 240, POLAR_GRID_CLR)
        self.disps.circ_disp.hline(0, 120, 240, POLAR_GRID_CLR)

    def _draw_radar_sweep(self, clear):
        step_mod = self.step_cnt % RADAR_SWEEP_INC
        if not clear:
            self.current_sweep_radius = RADAR_SWEEP_INC * step_mod
            color = POLAR_GRID_CLR
        else:
            color = Displays.BLACK

        self._draw_ring(120, 120, self.current_sweep_radius, color)
        self._draw_radar_signals(clear)


    def _draw_radar_signals(self, clear):
        for sig in self.radar_signals:
            if not clear:
                #print(f'x={sig.x}, y={sig.y}, show_radius = {sig.show_radius}, sweep={self.current_sweep_radius}')
                if sig.show_radius <= self.current_sweep_radius and sig.show_radius >= (self.current_sweep_radius - RADAR_SWEEP_INC):
                    # OK, we need to show it bright
                    color = sig.bright_color
                else:
                    color = sig.dim_color
            else: 
                color = Displays.BLACK
            self._draw_circle(sig.x, sig.y, RADAR_SIGNAL_RADIUS, color, self.disps.circ_disp)

    def _draw_ring(self, x, y, r, color):
        self.disps.circ_disp.pixel(x-r, y, color)
        self.disps.circ_disp.pixel(x+r, y, color)
        self.disps.circ_disp.pixel(x, y-r, color)
        self.disps.circ_disp.pixel(x, y+r, color)

        for i in range(1, r):
            a = int(math.sqrt(r*r-i*i)) # Pythagoras
            self.disps.circ_disp.pixel(x-a, y-i, color)
            self.disps.circ_disp.pixel(x+a, y-i, color)
            self.disps.circ_disp.pixel(x-a, y+i, color)
            self.disps.circ_disp.pixel(x+a, y+i, color)
            self.disps.circ_disp.pixel(x-i, y-a, color)
            self.disps.circ_disp.pixel(x+i, y-a, color)
            self.disps.circ_disp.pixel(x-i, y+a, color)
            self.disps.circ_disp.pixel(x+i, y+a, color)

