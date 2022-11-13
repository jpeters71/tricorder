# main.py -- put your code here!
import _thread
import time
import gc

from machine import PWM, Pin, SoftSPI
from micropython import const

from lcd_driver import LCD_Display
from oled_driver import SSD1351
from wavePlayer import wavePlayer


def show_starfleet_logo(lcd):

    with open('./media/sfl.raw', 'rb') as fp:
        buff = fp.read()
    lcd.blit_buffer(buff, 100, 5, 143, 230)

if __name__=='__main__':
    # Start display thread
    #_thread.start_new_thread(display_thread, ())

    #sound_pin = Pin(5, Pin.OUT, Pin.PULL_DOWN)
    #sound_pin.high()
    #player = wavePlayer(Pin(0))

    # try:
    #     while True:
    #         player.play('./tos_tricorder_scan.wav')
    
    # except KeyboardInterrupt:
    #     player.stop()
    #     sound_pin.low()

    pwm = PWM(Pin(16))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    height = 128 # 1.5 inch 128*128 display

    

    pdc = Pin(3, Pin.OUT, value=0)
    pcs = Pin(2, Pin.OUT, value=1)
    prst = Pin(4, Pin.OUT, value=1)
    #spi = machine.SPI(1, baudrate=1_000_000)
    spi = SoftSPI(sck=Pin(1, Pin.OUT), mosi=Pin(5, Pin.OUT), miso=Pin(0, Pin.OUT))
    gc.collect()  # Precaution before instantiating framebuf
    ssd = SSD1351(spi, pcs, pdc, prst, height)  # Create a display instance
    ssd.show()

    # LCD = LCD_Display(width=320, height=240, 
    #     bl_id=16, dc_id=17, rst_id=20, mosi_id=11, sck_id=10, cs_id=21,
    #     rotation=3, fill_color=const(0x00d1))

    start = time.ticks_ms()
    # show_starfleet_logo(LCD)
    ssd.fill_rect(20, 20, 70, 70, SSD1351.rgb(0, 0, 255))   
    end = time.ticks_ms()
    print(f'Time: {end - start}, {start}, {end}')

