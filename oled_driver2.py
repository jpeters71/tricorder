# SSD1351_16bit.py MicroPython driver for Adafruit color OLED displays.

# Adafruit 1.5" 128*128 OLED display: https://www.adafruit.com/product/1431
# Adafruit 1.27" 128*96 display https://www.adafruit.com/product/1673
# For wiring details see drivers/ADAFRUIT.md in this repo.

# This driver is based on the Adafruit C++ library for Arduino
# https://github.com/adafruit/Adafruit-SSD1351-library.git

# Copyright (c) Peter Hinch 2019-2020
# Released under the MIT license see LICENSE

import framebuf
import utime
import gc
from machine import PWM, Pin, SoftSPI, SPI
import micropython
import time
from micropython import const  


class OLEDDriver(framebuf.FrameBuffer):
    # Convert r, g, b in range 0-255 to a 16 bit colour value RGB565
    #  acceptable to hardware: rrrrrggggggbbbbb
    @staticmethod
    def rgb(r, g, b):
        return ((r & 0xf8) << 5) | ((g & 0x1c) << 11) | (b & 0xf8) | ((g & 0xe0) >> 5)


    # pdc = Pin(3, Pin.OUT, value=0)
    # pcs = Pin(2, Pin.OUT, value=1)
    # prst = Pin(4, Pin.OUT, value=1)
    # #spi = machine.SPI(1, baudrate=1_000_000)
    # spi = SoftSPI(sck=Pin(1, Pin.OUT), mosi=Pin(5, Pin.OUT), miso=Pin(0, Pin.OUT))
    # gc.collect()  # Precaution before instantiating framebuf
    # ssd = SSD1351(spi, pcs, pdc, prst, height)  # Create a display instance
    def __init__(self, cs_id: int, dc_id: int, sck_id: int, mosi_id: int, rst_id: int, miso_id: int, height=128, width=128):
        self.cs = Pin(cs_id, Pin.OUT)
        self.dc = Pin(dc_id, Pin.OUT)
        self.rst = Pin(rst_id, Pin.OUT)
        self.height = height  # Required by Writer class
        self.width = width
        gc.collect()
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

    
        # Init module
        #self.spi = SoftSPI(10_000_000, sck=Pin(sck_id, Pin.OUT), mosi=Pin(mosi_id, Pin.OUT), miso=Pin(miso_id, Pin.OUT))

        self.spi = SPI(0, 10_000_000, polarity=1, phase=1, sck=Pin(sck_id, Pin.OUT), mosi=Pin(mosi_id, Pin.OUT), miso=None)


        self.rst.low()
        # GPIO.output(RST_PIN, 0)
        # if(Device == Device_SPI):
        #     spi.max_speed_hz = 10000000
        #     spi.mode = 0b11  
        self.cs.low()
        self.dc.low()

        self._init_display()
    
    def _init_display(self):
        self.reset()

        self.write_cmd(0xfd) # write_cmd lock
        self.write_data(0x12)
        self.write_cmd(0xfd) # write_cmd lock
        self.write_data(0xB1)

        self.write_cmd(0xae) # display off
        self.write_cmd(0xa4) # Normal Display mode

        self.write_cmd(0x15) # set column address
        self.write_data(0x00)    # column address start 00
        self.write_data(0x7f)    # column address end 127
        self.write_cmd(0x75) # set row address
        self.write_data(0x00)    # row address start 00
        self.write_data(0x7f)    # row address end 127   

        self.write_cmd(0xB3)
        self.write_data(0xF1)

        self.write_cmd(0xCA)
        self.write_data(0x7F)

        self.write_cmd(0xa0) # set re-map & write_data format
        self.write_data(0x74)    # Horizontal address increment

        self.write_cmd(0xa1) # set display start line
        self.write_data(0x00)    # start 00 line

        self.write_cmd(0xa2) # set display offset
        self.write_data(0x00)

        self.write_cmd(0xAB)
        self.write_cmd(0x01)

        self.write_cmd(0xB4)
        self.write_data(0xA0)
        self.write_data(0xB5)
        self.write_data(0x55)

        self.write_cmd(0xC1)
        self.write_data(0xC8)
        self.write_data(0x80)
        self.write_data(0xC0)

        self.write_cmd(0xC7)
        self.write_data(0x0F)

        self.write_cmd(0xB1)
        self.write_data(0x32)

        self.write_cmd(0xB2)
        self.write_data(0xA4)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0xBB)
        self.write_data(0x17)

        self.write_cmd(0xB6)
        self.write_data(0x01)

        self.write_cmd(0xBE)
        self.write_data(0x05)

        self.write_cmd(0xA6)

        time.sleep(0.1)
        self.write_cmd(0xAF);#--turn on oled panel


    def write_cmd(self, cmd):
        self.dc.low()
        self.spi.write(bytearray([cmd]))

    def write_data(self, buf):
        self.dc.high()
        self.spi.write(bytearray([buf]))

    def write_data2(self, buf):
        self.dc.high()
        self.spi.write(bytearray(buf))

    def reset(self):
        self.rst.high()
        time.sleep_ms(100)
        self.rst.low()
        time.sleep_ms(100)
        self.rst.high()
        time.sleep_ms(100)    
    
    
    def show(self):
        self.write_cmd(0x15) # set column address
        self.write_data(0x00)    # column address start 00
        self.write_data(0x7f)    # column address end 127
        self.write_cmd(0x75) # set row address
        self.write_data(0x00)    # row address start 00
        self.write_data(0x7f)    # row address end 127   
        self.write_cmd(0x5C); 

        self.write_data2(self.buffer)
        # for i in range(0, self.height):
        #     for j in range(0, self.width*2):
        #         self.write_data(self.buffer[j + self.width*2*i])
        return

if __name__=='__main__':

    gc.collect()  # Precaution before instantiating framebuf
    disp = OLEDDriver(
        cs_id=17,
        dc_id=20,
        sck_id=18,
        mosi_id=19,
        rst_id=21,
        miso_id=0)
    #     def __init__(self, cs_id: int, dc_id: int, sck_id: int, mosi_id: int, rst_id: int, miso_id: int = None, height=128, width=128):


    BLUE = const(0x001F)  
    RED = const(0xF800)  
    GREEN = const(0x07E0)  
    start = time.ticks_ms()
    # show_starfleet_logo(LCD)
    disp.fill_rect(20, 20, 70, 70, RED)
    disp.show()
    time.sleep_ms(500)
    disp.fill_rect(20, 20, 70, 70, GREEN)
    disp.show()
    time.sleep_ms(500)
    disp.fill_rect(20, 20, 70, 70, BLUE)
    disp.show()
    end = time.ticks_ms()
    print(f'Time: {end - start}, {start}, {end}')


