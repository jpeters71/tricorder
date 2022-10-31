# main.py -- put your code here!
import _thread
import time

from machine import PWM, Pin
from micropython import const

from lcd_driver import LCD_Display
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

