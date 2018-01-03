#!/usr/bin/python

################################################################################
# test script for python-spi-dev
# written by Rich Rademacher 1/2/2018 UWaterloo/IQC Trapped Ion Group
################################################################################

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 7629

# split an integer into two byt array and send to spi
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xff
    spi.xfer([msb, lsb])

# repeatedly swich on and off
while True:
    write_pot(0x1ff)
    time.sleep(0.5)
    write_pot(0x00)
    time.sleep(0.5)

