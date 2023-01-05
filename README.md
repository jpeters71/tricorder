# tricorder

This project represents code for a Star Trek TOS ("The Original Series") tricorder.  This project represents just the software for this project; see the hardware requirements below.

This project is meant to be used in conjunction with the 3d-printer models for this project which can be found in the https://github.com/jpeters71/tricorder_models (which desperately needs some documentation).

## Hardware Requirements
* SBC (Single Board Computer) - This project uses the Raspberry Pico (RP2040 CPU) based board. Specifically this, this project is using the Pimoroni Pico board (https://shop.pimoroni.com/products/pimoroni-pico-lipo?variant=39335427080275). The main reason for using this board as opposed to the plain vanilla Pico is that the Pimoroni board includes a Qwiic connector and a battery connector/charger built-into the board. You can still use project with the plain vanilla Pico but you'll need to wire up the SX1508 GPIO expander to I2C pins on the Pico.
* SX1508 GPIO expander - GPIO expander from SparkFun (https://www.sparkfun.com/products/13601). Used for the main control panel LEDs and buttons.
* ST7789 320x240 2" LCD Display - Top display for the tricorder (https://smile.amazon.com/gp/product/B081Q79X2F/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1). Other displays may be used but code and/or 3d models may need to be adjusted.
* GC9A01 240x240 1.28" Round LCD Display - Bottom display for the tricorder (https://smile.amazon.com/gp/product/B0B7TFRNN1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1). Like the top display, other displays may be used but the 3d model and/or the code may need to be adjusted.

TODO: Finish this
