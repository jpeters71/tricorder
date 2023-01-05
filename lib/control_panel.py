from machine import Pin, I2C, PWM, SPI

from lib.sx1509 import SX1509, SX1590def
from lib.utils import log
#from lib.sx1509b import SX1509


# INPUT = 0x00
# OUTPUT = 0x01
# INPUT_PULLUP = 0x02
# ANALOG_OUTPUT = 0x03
# INPUT_PULLDOWN = 0x04
# INPUT_OPEN_DRAIN = 0x05

INPUT = 0x00
INPUT_PULLUP = 0x02
OUTPUT = 0x01
HIGH = 255
LOW  = 0

class ControlPanel:
    LED1 = 0
    LED2 = 1
    LED3 = 2
    SW1 = 0
    SW2 = 1
    SW3 = 2

    LED1_PIN = 8
    LED2_PIN = 9
    LED3_PIN = 10
    LEDS = [LED1_PIN, LED2_PIN, LED3_PIN]
    SW1_PIN = 11
    SW2_PIN = 12
    SW3_PIN = 13
    SWS = [SW1_PIN, SW2_PIN, SW3_PIN]

    def __init__(self):
        self.i2c = I2C(0, scl=Pin(5), sda=Pin(4))

        # Test
        scan_tst = self.i2c.scan()
        log(f'SCAN TEST: {scan_tst}')

        self.io = SX1509(i2c=self.i2c, addr=0x3E)
        self.io.reset(hard=False)

        self._init_leds()
        self._init_buttons()

    def _init_leds(self):
        self.io.pinMode(self.LED1_PIN, inOut=OUTPUT)
        self.io.pinMode(self.LED2_PIN, inOut=OUTPUT)
        self.io.pinMode(self.LED3_PIN, inOut=OUTPUT)
        self.io.digitalWrite(self.LED1_PIN, LOW)
        self.io.digitalWrite(self.LED2_PIN, LOW)
        self.io.digitalWrite(self.LED3_PIN, LOW)

    def _init_buttons(self):
        self.io.pinMode(self.SW1_PIN, inOut=INPUT_PULLUP)
        self.io.pinMode(self.SW2_PIN, inOut=INPUT_PULLUP)
        self.io.pinMode(self.SW3_PIN, inOut=INPUT_PULLUP)

        self.io.debounceEnable(self.SW1_PIN)
        self.io.debounceEnable(self.SW2_PIN)
        self.io.debounceEnable(self.SW3_PIN)

    def leds_on(self, leds):
        self.io.digitalWrite(self.LED1_PIN, LOW)
        self.io.digitalWrite(self.LED2_PIN, LOW)
        self.io.digitalWrite(self.LED3_PIN, LOW)

        for led in leds:
            self.io.digitalWrite(self.LEDS[led], HIGH)
        
    def led_on(self, led_id: int):
        pin_id = self.LEDS[led_id]
        self.io.digitalWrite(pin_id, HIGH)

    def led_off(self, led_id: int):
        pin_id = self.LEDS[led_id]
        self.io.digitalWrite(pin_id, LOW)

    def read_buttons(self):
        btn_state = self.io.digitalReadAllPins()

        return [
            btn_state & (1<<self.SW1_PIN) == 0,
            btn_state & (1<<self.SW2_PIN) == 0,
            btn_state & (1<<self.SW3_PIN) == 0,
        ]
