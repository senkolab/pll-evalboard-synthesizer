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
import adf41020_2
import pe4312

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

#This program sets the frequency of one pll connected to this pin
GPIOpin1 = 4 
freq = 8.037e9 


rf_pll = adf41020_2.ADF41020(GPIOpin1)
do_loop = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin1, GPIO.OUT)
#GPIO.output(GPIOpin1, False)
#GPIO.setup(GPIOpin2, GPIO.OUT)
#GPIO.output(GPIOpin2, True)

# check for command line args
if(len(sys.argv) > 1) :
    try:
        freq = float(sys.argv[1])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

# program
if(False == do_loop):
    #attenuator.program_init(rf_spi)

    f_actual = rf_pll.set_freq(freq) 
    #atten_actual = attenuator.set_atten(atten)

    print 'Programming ADF41020 to %g MHz' % (f_actual / 1e6)
    print 'R value = %d' % (rf_pll.R)
    print 'B value = %d' % (rf_pll.B)
    print 'A value = %d' % (rf_pll.A)
    rf_pll.program_freq(rf_spi)

    time.sleep(1)
    
    #attenuator.program_atten(rf_spi)

    #time.sleep(2)
else :
    pass

