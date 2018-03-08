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
import sys

#
# begin main program
#
rf_spi = spidev.SpiDev()
spidev = 0
spi_cs = 1
rf_spi.open(spidev, spi_cs)
rf_spi.cshigh = False 
rf_spi.max_speed_hz = 100000
rf_pll = adf4355_2.ADF4355()
do_loop = False
freq =  250e6 

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


    print 'Programming ADF4355-2 to %g MHz' % (rf_pll.set_freq(freq) / 1e6)

    print 'R value = %d' % (rf_pll.r)
    print 'INT value = %d' % (rf_pll.intval)
    print 'FRAC1 value = %d' % (rf_pll.frac1)
    print 'FRAC2 value = %d' % (rf_pll.frac2)
    print 'MOD2 value = %d' % (rf_pll.mod2)

    rf_pll.program_freq(rf_spi)

    time.sleep(0.5)
else :
    pass

