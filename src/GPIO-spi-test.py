# -*- coding: utf-8 -*-
"""
Created on Sat May 12 14:43:44 2018

@author: bbramman
"""

import RPi.GPIO as GPIO
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 7629
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

# split an integer into two byt array and send to spi
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xff
    spi.xfer([msb, lsb])

# repeatedly swich on and off
while True:
    write_pot(0x1ff)
    GPIO.output(25, True)
    time.sleep(30e-9)
    GPIO.output(25, False)
    time.sleep(0.5)
    write_pot(0x00)
    GPIO.output(25, True)
    time.sleep(30e-9)
    GPIO.output(25, False)
    time.sleep(0.5)

