
from machine import Pin,SPI,PWM
import framebuf
import time
import os
from micropython import const

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_2inch(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 320
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BALCK =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
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

        self.write_cmd(0xE1)
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
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3f)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
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
            self._write(ST7789_CASET, _encode_pos(
                start+self.xstart, end + self.xstart))

    def _set_rows(self, start, end):
        """
        Send RASET (row address set) command to display.

        Args:
            start (int): row start address
            end (int): row end address
       """
        if start <= end <= self.height:
            self._write(ST7789_RASET, _encode_pos(
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
        self._write(ST7789_RAMWR)

    def _write(self, command=None, data=None):
        """SPI write to the device: commands and data."""
        self.cs.on()

        if command is not None:
            self.write_cmd(command)
        if data is not None:
            self.write_data(data)

import ustruct as struct

_ENCODE_PIXEL = ">H"
_ENCODE_POS = ">HH"

ST7789_CASET = const(0x2A)
ST7789_RASET = const(0x2B)
ST7789_RAMWR = const(0x2C)

def _encode_pixel(color):
    """Encode a pixel color into bytes."""
    return struct.pack(_ENCODE_PIXEL, color)

def _encode_pos(x, y):
    """Encode a postion into bytes."""
    return struct.pack(_ENCODE_POS, x, y)

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_2inch()
    #color BRG
    LCD.fill(LCD.WHITE)

    
    time.sleep(0.1)
    LCD.fill_rect(0,0,320,24,LCD.RED)
    LCD.rect(0,0,320,24,LCD.RED)
    LCD.text("Raspberry Pi Pico",2,8,LCD.WHITE)

    LCD.fill_rect(0,24,320,24,LCD.BLUE)
    LCD.rect(0,24,320,24,LCD.BLUE)
    LCD.text("PicoGo",2,32,LCD.WHITE)

    LCD.fill_rect(0,48,320,24,LCD.GREEN)
    LCD.rect(0,48,320,24,LCD.GREEN)
    LCD.text("Pico-LCD-2",2,54,LCD.WHITE)

    LCD.fill_rect(0,72,320,24,0X07FF)
    LCD.rect(0,72,320,24,0X07FF)

    LCD.fill_rect(0,96,320,24,0xF81F)
    LCD.rect(0,96,320,24,0xF81F)

    LCD.fill_rect(0,120,320,24,0x7FFF)
    LCD.rect(0,120,320,24,0x7FFF)

    LCD.fill_rect(0,144,320,24,0xFFE0)
    LCD.rect(0,144,320,24,0xFFE0)

    LCD.fill_rect(0,168,320,24,0XBC40)
    LCD.rect(0,168,320,24,0XBC40)

    LCD.fill_rect(0,192,320,24,0XFC07)
    LCD.rect(0,192,320,24,0XFC07)
    LCD.fill_rect(0,216,320,24,0X8430)
    LCD.rect(0,216,320,24,0X8430)

    time.sleep(0.1)
    LCD.show()
    LCD.fill(0xFFFF)
    time.sleep(0.5)
    key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
   
    while(1):      
        if(key0.value() == 0):
            LCD.fill_rect(12,12,20,20,LCD.RED)
        else :
            LCD.fill_rect(12,12,20,20,LCD.WHITE)
            LCD.rect(12,12,20,20,LCD.RED)
            
        if(key1.value() == 0):
            LCD.fill_rect(288,12,20,20,LCD.RED)
        else :
            LCD.fill_rect(288,12,20,20,LCD.WHITE)
            LCD.rect(288,12,20,20,LCD.RED)
            
        if(key2.value() == 0):
            LCD.fill_rect(288,208,20,20,LCD.RED)
        else :
            LCD.fill_rect(288,208,20,20,LCD.WHITE)
            LCD.rect(288,208,20,20,LCD.RED)
        if(key3.value() == 0):
            
            LCD.fill_rect(12,208,20,20,LCD.RED)
        else :
            LCD.fill_rect(12,208,20,20,LCD.WHITE)
            LCD.rect(12,208,20,20,LCD.RED) 
                      
        LCD.show()
    time.sleep(1)
    
    LCD.fill(0xFFFF)





