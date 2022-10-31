# WS 320x240 display example
from machine import Pin,SPI,PWM
import time
from micropython import const  
import ustruct as struct 


import ustruct as struct

_ENCODE_PIXEL = ">H"
_ENCODE_POS = ">HH"

_BUFFER_SIZE = 256

# Color
BLACK = const(0x0000)  
BLUE = const(0x001F)  
RED = const(0xF800)  
GREEN = const(0x07E0)  
CYAN = const(0x07FF)  
MAGENTA = const(0xF81F)  
YELLOW = const(0xFFE0)  
WHITE = const(0xFFFF)  
UW_PURPLE = const(0x781a)

# commands
NOP = const(0x00)
SWRESET = const(0x01)
RDDID = const(0x04)
RDDST = const(0x09)
SLPIN = const(0x10)
SLPOUT = const(0x11)
PTLON = const(0x12)
NORON = const(0x13)
INVOFF = const(0x20)
INVON = const(0x21)
DISPOFF = const(0x28)
DISPON = const(0x29)
CASET = const(0x2A)
RASET = const(0x2B)
RAMWR = const(0x2C)
RAMRD = const(0x2E)
PTLAR = const(0x30)
VSCRDEF = const(0x33)
COLMOD = const(0x3A)
MADCTL = const(0x36)
VSCSAD = const(0x37)
MADCTL_MY = const(0x80)
MADCTL_MX = const(0x40)
MADCTL_MV = const(0x20)
MADCTL_ML = const(0x10)
MADCTL_BGR = const(0x08)
MADCTL_MH = const(0x04)
MADCTL_RGB = const(0x00)
RDID1 = const(0xDA)
RDID2 = const(0xDB)
RDID3 = const(0xDC)
RDID4 = const(0xDD)
PORCTRL = const(0xB2)
GCTRL = const(0xB7)
VCOMS = const(0xBB)
LCMCTRL = const(0xC0)
VDVVRHEN = const(0xC2)
VRHS = const(0xC3)
VDVS = const(0xC4)
FRCTRL2 = const(0xC6)
PWCTRL1 = const(0xD0)
PVGAMCTRL = const(0xE0)
NVGAMCTRL = const(0xE1)

COLOR_MODE_65K = const(0x50)
COLOR_MODE_262K = const(0x60)
COLOR_MODE_12BIT = const(0x03)
COLOR_MODE_16BIT = const(0x05)
COLOR_MODE_18BIT = const(0x06)
COLOR_MODE_16M = const(0x07)


_BIT7 = const(0x80)
_BIT6 = const(0x40)
_BIT5 = const(0x20)
_BIT4 = const(0x10)
_BIT3 = const(0x08)
_BIT2 = const(0x04)
_BIT1 = const(0x02)
_BIT0 = const(0x01)

# Rotation tables (width, height, xstart, ystart)[rotation % 4]

WIDTH_320 = [(240, 320,  0,  0),
             (320, 240,  0,  0),
             (240, 320,  0,  0),
             (320, 240,  0,  0)]

WIDTH_240 = [(240, 240,  0,  0),
             (240, 240,  0,  0),
             (240, 240,  0, 80),
             (240, 240, 80,  0)]

WIDTH_135 = [(135, 240, 52, 40),
             (240, 135, 40, 53),
             (135, 240, 53, 40),
             (240, 135, 40, 52)]

# MADCTL ROTATIONS[rotation % 4]
ROTATIONS = [0x00, 0x60, 0xc0, 0xa0]


class LCD_Display(): # For 320x240 display
    def __init__(self, width: int, height: int, 
                    bl_id: int, dc_id: int, rst_id: int, mosi_id: int, sck_id: int, cs_id: int,
                    rotation: int = 0, fill_color: int = None):
        self.width = self._display_width = width
        self.height = self._display_height = height
        
        self.cs = Pin(cs_id, Pin.OUT)
        self.rst = Pin(rst_id, Pin.OUT)
        
        self.cs.high()
        self.spi = SPI(1, 100_000_000, polarity=0, phase=0, sck=Pin(sck_id), mosi=Pin(mosi_id), miso=None)
        self.dc = Pin(dc_id, Pin.OUT)
        self.dc.high()
        self.init_display(rotation=rotation)

        if fill_color:
            self.fill(fill_color)
        
    def write_cmd(self, cmd):
        self.cs.high()
        self.dc.low()
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()

    def write_data(self, buf):
        self.cs.high()
        self.dc.high()
        self.cs.low()
        self.spi.write(bytearray([buf]))
        self.cs.high()

    def hard_reset(self):
        """
        Hard reset display.
        """
        if self.cs:
            self.cs.on()
        if self.rst:
            self.rst.on()
        time.sleep_ms(50)
        if self.rst:
            self.rst.off()
        time.sleep_ms(50)
        if self.rst:
            self.rst.on()
        time.sleep_ms(150)
        if self.cs:
            self.cs.on()
    
    def soft_reset(self):
        """
        Soft reset display.
        """
        self._write(SWRESET)
        time.sleep_ms(150)

    def sleep_mode(self, value):
        """
        Enable or disable display sleep mode.

        Args:
            value (bool): if True enable sleep mode. if False disable sleep
            mode
        """
        if value:
            self._write(SLPIN)
        else:
            self._write(SLPOUT)

    def rotation(self, rotation):
        """
        Set display rotation.

        Args:
            rotation (int):
                - 0-Portrait
                - 1-Landscape
                - 2-Inverted Portrait
                - 3-Inverted Landscape
        """

        rotation %= 4
        self._rotation = rotation
        madctl = ROTATIONS[rotation]

        if self._display_width == 320:
            table = WIDTH_320
        elif self._display_width == 240:
            table = WIDTH_240
        elif self._display_width == 135:
            table = WIDTH_135
        else:
            raise ValueError(
                "Unsupported display. 320x240, 240x240 and 135x240 are supported."
            )

        self.width, self.height, self.xstart, self.ystart = table[rotation]
        self._write(MADCTL, bytes([madctl]))

    def _set_color_mode(self, mode):
        """
        Set display color mode.

        Args:
            mode (int): color mode
                COLOR_MODE_65K, COLOR_MODE_262K, COLOR_MODE_12BIT,
                COLOR_MODE_16BIT, COLOR_MODE_18BIT, COLOR_MODE_16M
        """
        self._write(COLMOD, bytes([mode & 0x77]))

    def inversion_mode(self, value):
        """
        Enable or disable display inversion mode.

        Args:
            value (bool): if True enable inversion mode. if False disable
            inversion mode
        """
        if value:
            self._write(INVON)
        else:
            self._write(INVOFF)

    def init_display(self, rotation):
        """Initialize display"""  
        self.hard_reset()
        self.soft_reset()
        self.sleep_mode(False)

        self.rotation(rotation=rotation)
        # self.write_cmd(MADCTL)
        # self.write_data(0x70)

        # self.write_cmd(COLMOD) 
        # self.write_data(0x05)
        self._set_color_mode(COLOR_MODE_65K | COLOR_MODE_16BIT)
        time.sleep_ms(50)


        self.write_cmd(PORCTRL)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(GCTRL)
        self.write_data(0x35) 

        self.write_cmd(VCOMS)
        self.write_data(0x19)

        self.write_cmd(LCMCTRL)
        self.write_data(0x2C)

        self.write_cmd(VDVVRHEN)
        self.write_data(0x01)

        self.write_cmd(VRHS)
        self.write_data(0x12)   

        self.write_cmd(VDVS)
        self.write_data(0x20)

        self.write_cmd(FRCTRL2)
        self.write_data(0x0F) 

        self.write_cmd(PWCTRL1)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(PVGAMCTRL)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(NVGAMCTRL)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        #self.write_cmd(0x21)
        self.inversion_mode(True)
        self.write_cmd(SLPOUT)
        self.write_cmd(DISPON)

    def pixel(self, x, y, color):  
        """  
        Draw a pixel at the given location and color.  
        Args:  
        x (int): x coordinate  
        Y (int): y coordinate  
        color (int): 565 encoded color  
        """  
        self._set_window(x, y, x, y)  
        self._write(None, _encode_pixel(color))

    def blit_buffer(self, buffer, x, y, width, height):
        """
        Copy buffer to display at the given location.

        Args:
            buffer (bytes): Data to copy to display
            x (int): Top left corner x coordinate
            Y (int): Top left corner y coordinate
            width (int): Width
            height (int): Height
        """
        self._set_window(x, y, x + width - 1, y + height - 1)
        self._write(None, buffer)

    xstart = 0
    ystart = 0

    def _set_columns(self, start, end):
        """
        Send CASET (column address set) command to display.

        Args:
            start (int): column start address
            end (int): column end address
        """
        if start <= end <= self.width:
            self._write(CASET, _encode_pos(
                start+self.xstart, end + self.xstart))

    def _set_rows(self, start, end):
        """
        Send RASET (row address set) command to display.

        Args:
            start (int): row start address
            end (int): row end address
       """
        if start <= end <= self.height:
            self._write(RASET, _encode_pos(
                start+self.ystart, end+self.ystart))

    def _set_window(self, x0, y0, x1, y1):
        """
        Set window to column and row address.

        Args:
            x0 (int): column start address
            y0 (int): row start address
            x1 (int): column end address
            y1 (int): row end address
        """
        self._set_columns(x0, x1)
        self._set_rows(y0, y1)
        self._write(RAMWR)

    def _write(self, command=None, data=None):
        """SPI write to the device: commands and data."""
        self.cs.on()

        if command is not None:
            self.write_cmd2(command)
        if data is not None:
            self.write_data2(data)

    def write_cmd2(self, cmd):
        self.cs.high()
        self.dc.low()
        self.cs.low()
        self.spi.write(bytes([cmd]))
        self.cs.high()

    def write_data2(self, buf):
        self.cs.high()
        self.dc.high()
        self.cs.low()
        self.spi.write(buf)
        self.cs.high()


    def fill_rect(self, x, y, width, height, color):  
        """  
        Draw a rectangle at the given location, size and filled with color.  
        Args:  
        x (int): Top left corner x coordinate  
        y (int): Top left corner y coordinate  
        width (int): Width in pixels  
        height (int): Height in pixels  
        color (int): 565 encoded color  
        """  
        self._set_window(x, y, x + width - 1, y + height - 1)  
        chunks, rest = divmod(width * height, _BUFFER_SIZE)  
        pixel = _encode_pixel(color)  
        #self.dc.on()  
        if chunks:  
            data = pixel * _BUFFER_SIZE  
            for _ in range(chunks):  
                self._write(None, data)  
        if rest:  
            self._write(None, pixel * rest)  

    def fill(self, color):  
        """  
        Fill the entire FrameBuffer with the specified color.  
        Args:  
            color (int): 565 encoded color  
        """  
        self.fill_rect(0, 0, self.width, self.height, color)  

def _encode_pixel(color):
    """Encode a pixel color into bytes."""
    return struct.pack(_ENCODE_PIXEL, color)

def _encode_pos(x, y):
    """Encode a postion into bytes."""
    return struct.pack(_ENCODE_POS, x, y)

def show_starfleet_logo(lcd):

    with open('./media/sfl.raw', 'rb') as fp:
        buff = fp.read()
    lcd.blit_buffer(buff, 100, 5, 143, 230)

if __name__=='__main__':
    pwm = PWM(Pin(16))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535


    LCD = LCD_Display(width=320, height=240, 
        bl_id=16, dc_id=17, rst_id=20, mosi_id=11, sck_id=10, cs_id=21,
        rotation=3, fill_color=const(0x00d1))

    start = time.ticks_ms()
    show_starfleet_logo(LCD)
       
    # LCD.fill_rect(0, 100, 100, 100, BLUE)
    # LCD.fill_rect(100, 50, 100, 100, MAGENTA)
    # LCD.fill_rect(200, 0, 120, 240, UW_PURPLE)
    
    # old_x = 100
    # old_y = 50
    
    # for i in range(0, 100):
    #     LCD.fill_rect(old_x, old_y, 100, 100, WHITE)
    #     old_x += 1
    #     old_y += 1
    #     LCD.fill_rect(old_x, old_y, 100, 100, MAGENTA)
    #     time.sleep_ms(250)
    end = time.ticks_ms()
    print(f'Time: {end - start}, {start}, {end}')
            


'''
LCD.rect(0,0,160,128,colour(0,0,255)) # Blue Frame
LCD.text("WaveShare", 44,10,colour(255,0,0))
LCD.text('Pico Display 1.8"', 10,24,colour(255,255,0))
LCD.text("160x128 SPI", 38,37,colour(0,255,0))
LCD.text("Tony Goodhew", 30,48,colour(100,100,100))
c = colour(255,240,0)
printstring("New Font - Size 1",14,65,1,0,0,c)
c = colour(255,0,255)
printstring("Now size 2",12,78,2,0,0,c)
c = colour(0,255,255)
printstring("Size 3",30,100,3,0,0,c)

LCD.pixel(0,0,0xFFFF)     # Left Top - OK
LCD.pixel(0,239,0xFFFF)   # Left Bottom - OK
LCD.pixel(319,0,0xFFFF)   # Right Top - OK
LCD.pixel(319,239,0xFFFF) # Right Bottom - OK
LCD.show()
utime.sleep(20)
'''
