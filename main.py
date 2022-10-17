# WS 320x240 display example
from machine import Pin,SPI,PWM
import framebuf
import time
import os

from lcd_display import LCD_1inch3, BL


if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch3()
    #color BRG
    LCD.fill(LCD.WHITE)
    LCD.show()
    
    cnt = 0
    while(1):
        cnt += 1
        LCD.fill_rect(0,0,320,24,LCD.RED)
        LCD.rect(0,0,320,24,LCD.RED)
        LCD.text(f"Raspberry Pi Pico {cnt}",2,8,LCD.WHITE)
        #time.sleep(0.1)
        LCD.fill_rect(0,24,320,24,LCD.BLUE)
        LCD.rect(0,24,320,24,LCD.BLUE)
        LCD.text("PicoGo",2,32,LCD.WHITE)
        #time.sleep(0.1)
        LCD.fill_rect(0,48,320,24,LCD.GREEN)
        LCD.rect(0,48,320,24,LCD.GREEN)
        LCD.text("Pico-LCD-2",2,54,LCD.WHITE)
        #time.sleep(0.1)
        LCD.fill_rect(0,72,320,24,0X07FF)
        LCD.rect(0,72,320,24,0X07FF)
        #time.sleep(0.1)
        LCD.fill_rect(0,96,320,24,0xF81F)
        LCD.rect(0,96,320,24,0xF81F)
        #time.sleep(0.1)
        LCD.fill_rect(0,120,320,24,0x7FFF)
        LCD.rect(0,120,320,24,0x7FFF)
        #time.sleep(0.1)
        LCD.fill_rect(0,144,320,24,0xFFE0)
        LCD.rect(0,144,320,24,0xFFE0)
        #time.sleep(0.1)
        LCD.fill_rect(0,168,320,24,0XBC40)
        LCD.rect(0,168,320,24,0XBC40)
        #time.sleep(0.1)
        LCD.fill_rect(0,192,320,24,0XFC07)
        LCD.rect(0,192,320,24,0XFC07)
        #time.sleep(0.1)
        LCD.fill_rect(0,216,320,24,0X8430)
        LCD.rect(0,216,320,24,0X8430)
        #time.sleep(0.1)
        #time.sleep(0.1)
        LCD.show()
    #time.sleep(1)
    LCD.fill(0xFFFF)

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




