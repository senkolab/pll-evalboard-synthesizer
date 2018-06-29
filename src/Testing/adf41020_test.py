#!/usr/bin/python
################################################################################
#   SPI programmer for ADF4355-2 
#
#   Written by Rich Rademacher, 
#           1/3/2018 
#           University of Waterloo/IQC
################################################################################

import time
import spidev
import adf41020

import sys
import RPi.GPIO as GPIO

#
# begin main program
#
rf_spi = spidev.SpiDev()
spidev = 0
spi_cs = 1
rf_spi.open(spidev, spi_cs)
rf_spi.cshigh = False 
rf_spi.max_speed_hz = 100000
GPIOpin = 25
rf_pll = adf41020.ADF41020(GPIOpin)
do_loop = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin, GPIO.OUT)
GPIO.output(GPIOpin, True)
freq = 8.037e9 

# check for command line args
if(len(sys.argv) > 1) :
    try:
        freq = float(sys.argv[1])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

# program
if(False == do_loop) :
    while True:

        f_actual = rf_pll.set_freq(freq) 
        print 'Programming ADF41020 to %g MHz' % (f_actual / 1e6)

        rf_pll.program_freq(rf_spi)

        time.sleep(2)
else :
    pass

