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
import adf4355_2
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

#This program sets the frequency of one PLL connected to this pin
GPIOpin1 = 4
freq1 = 150e6

# check for command line args
if(len(sys.argv) > 1) :
    try:
        GPIOpin1 = int(sys.argv[1])
        freq = float(sys.argv[2])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

rf_pll_1 = adf4355_2.ADF4355(GPIOpin1)

do_loop = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin1, GPIO.OUT)

GPIO.output(GPIOpin1, True)

# program
if(False == do_loop) :

    print 'Initialize' 
    rf_pll_1.program_init(rf_spi)

    f_actual_1 = rf_pll_1.set_freq(freq1) 
    print 'Programming ADF4355-2_1 to %g MHz' % (f_actual_1 / 1e6)
    print 'R value = %d' % (rf_pll_1.r)
    print 'INT value = %d' % (rf_pll_1.intval)
    print 'FRAC1 value = %d' % (rf_pll_1.frac1)
    print 'FRAC2 value = %d' % (rf_pll_1.frac2)
    print 'MOD2 value = %d' % (rf_pll_1.mod2)
    rf_pll_1.program_freq(rf_spi)
    time.sleep(1)

else :
    pass

