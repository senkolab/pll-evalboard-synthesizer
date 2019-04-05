# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:58:04 2018

@author: bbramman
"""

import time
import spidev
import adf4360_8
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
freq = 200e6 

rf_pll = adf4360_8.ADF4360(GPIOpin)
do_loop = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin, GPIO.OUT)
GPIO.output(GPIOpin, True)

# check for command line args
if(len(sys.argv) > 1) :
    try:
        freq = float(sys.argv[1])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

# program
if(False == do_loop) :
    print 'Initialize' 
    rf_pll.program_init(rf_spi)

    f_actual = rf_pll.set_freq(freq) 
    print 'Programming ADF4360_8 to %g MHz' % (f_actual / 1e6)

    print 'B value = %d' % (rf_pll.Bcounter)
    print 'R value = %d' % (rf_pll.Rcounter)
    rf_pll.program_freq(rf_spi)

    time.sleep(0.5)
else :
    pass

