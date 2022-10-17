# aclock.py Test/demo program for nanogui
# Orinally for ssd1351-based OLED displays but runs on most displays
# Adafruit 1.5" 128*128 OLED display: https://www.adafruit.com/product/1431
# Adafruit 1.27" 128*96 display https://www.adafruit.com/product/1673

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2018-2020 Peter Hinch

# Initialise hardware and framebuf before importing modules.
from color_setup import ssd  # Create a display instance
from gui.core.nanogui import refresh  # Color LUT is updated now.
from gui.widgets.label import Label
from gui.widgets.dial import Dial, Pointer
refresh(ssd, True)  # Initialise and clear display.

# Now import other modules
import cmath
import utime
from gui.core.writer import CWriter

# Font for CWriter
import gui.fonts.arial10 as arial10
from gui.core.colors import *

PURPLE = create_color(12, 51, 0, 102)
GOLD = create_color(13, 204, 204, 0)
def aclock():
    print("BOZO")
    uv = lambda phi : cmath.rect(1, phi)  # Return a unit vector of phase phi
    pi = cmath.pi
    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday')
    months = ('Jan', 'Feb', 'March', 'April', 'May', 'June', 'July',
              'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
    # Instantiate CWriter
    CWriter.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = CWriter(ssd, arial10, PURPLE, GOLD)  # Report on fast mode. Or use verbose=False
    wri.set_clip(True, True, True)
    wri.printstring('Bozo was here. Go Dawgs! Go Huskies!')

    refresh(ssd)

aclock()
