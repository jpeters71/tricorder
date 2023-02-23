import gc
import random

from lib.actions import Action
from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays

# These angles are NOT regular on purpose: if we did everything with equal 
# angle increments, the stars tend to cluster around the 45 degree vector.
# This is an artifact of the rounding errors involved in calculating the 
# tangent line. The easy solution is to have more increments closer to 0 and 90
# and fewer increments around 45 degrees.
ANGLE_RISE_RUN = [
    (1, 57.29), # 1
    (1, 28.636), # 2
    (1, 19.081), # 3
    (1, 14.301), # 4
    (1, 11.43), # 5
    (1, 5.6713), # 10    
    (1, 3.7321), # 15    
    (1, 2.7475), # 20    
    (1, 2.1445), # 25    
    (1, 1.7321), # 30
    #(1, 1.4281), # 35    
    #(1, 1.1918), # 40    
    (1, 1), # 45    
    #(1.1918, 1), # 50    
    #(1.4281, 1), # 55    
    (1.7321, 1), # 60    
    (2.1445, 1), # 65    
    (2.7475, 1), # 70    
    (3.732  , 1), # 75    
    (5.6713, 1), # 80    
    (11.43, 1), # 85    
    (57.29, 1), # 86
    (28.636, 1), # 87
    (19.081, 1), # 88
    (14.301, 1), # 89
    (1, 0), # 90
]

QUADRANT = [
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1)
]

BACKGROUND_COLOR = Displays.BLACK
STAR_CNT_INC = 15


class Star():
    def __init__(self, x: int, y: int, rate: int, quadrant: int, angle_idx: int, color: int):
        self.x = x
        self.y = y
        self.rate = rate
        self.quadrant = quadrant
        self.angle_idx = angle_idx
        self.color = color

        # Calculate increments
        quad = QUADRANT[self.quadrant]
        x_mul = quad[0]
        y_mul = quad[1]
        rise_run = ANGLE_RISE_RUN[self.angle_idx]
        rise = rise_run[0]
        run = rise_run[1]
        self.increment_x = round(x_mul * (run + self.rate))
        self.increment_y = round(y_mul * (rise + self.rate))        


class SpaceScanAction(Action):
    def __init__(self, disps: Displays, audio: Audio, ctrl_panel: ControlPanel):
        super().__init__(disps, audio, ctrl_panel, step_delay = .05)
        self.stars = []
        self.step_cnt = 0

    def start(self):
        gc.collect()
        # Start with the initial state
        self.disps.top_disp.fill_rect(0, 0, 320, 240, Displays.BLACK)
        self._init_stars()
        self.disps.circ_disp.jpg('media/bluemarble.jpg', 0, 0, Displays.CIRC_DISP_JPG_SLOW)
        gc.collect()
        self.step_cnt = 0
        self._draw_stars(erase=False)
        
    def step(self):
        gc.collect()
        self.step_cnt += 1
        self._draw_stars(erase=True)
        self._increment_stars()
        self._draw_stars(erase=False)
        if self.step_cnt % 3 == 0:
            self._add_stars(STAR_CNT_INC)

    def stop(self):
        pass

    def _init_stars(self):
        self.stars = []
        self._add_stars(STAR_CNT_INC)

    def _add_stars(self, num_stars: int):
        for _ in range(0, num_stars):
            quad = random.randint(0, len(QUADRANT) - 1)
           
            self.stars.append(Star(
                x=160,
                y=120,
                rate=random.randint(1, 5),
                quadrant=quad,
                angle_idx=random.randint(0, len(ANGLE_RISE_RUN) - 1),
                color=random.choice([
                    Displays.WHITE,
                    Displays.GREEN,
                    Displays.WHITE,
                    Displays.RED,
                    Displays.WHITE,
                    Displays.YELLOW,
                    Displays.WHITE,
                ])
            ))

    def _draw_stars(self, erase: bool):
        for star in self.stars:
            color = BACKGROUND_COLOR if erase else star.color
            self.disps.top_disp.pixel(star.x, star.y, color)

    def _increment_stars(self):
        remove_lst = []
        
        for star in self.stars:
            if star.x < 0 or star.y < 0 or star.x > 320 or star.y > 240:
                remove_lst.append(star)
            star.x += star.increment_x
            star.y += star.increment_y
 
        for star in remove_lst:
            self.stars.remove(star)
        gc.collect()
        

