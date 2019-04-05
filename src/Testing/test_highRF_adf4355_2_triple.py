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
GPIOpin1 = 4
GPIOpin2 = 5
GPIOpin3 = 6

GPIOpin4 = 12
GPIOpin5 = 13
GPIOpin6 = 16

rf_pll_1 = adf4355_2.ADF4355(GPIOpin1)
rf_pll_2 = adf4355_2.ADF4355(GPIOpin2)
rf_pll_3 = adf4355_2.ADF4355(GPIOpin3)

rf_atten1= pe4312.PE4312(GPIOpin4)
rf_atten2= pe4312.PE4312(GPIOpin5)
rf_atten3= pe4312.PE4312(GPIOpin6)

do_loop = False
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIOpin1, GPIO.OUT)
GPIO.setup(GPIOpin2, GPIO.OUT)
GPIO.setup(GPIOpin3, GPIO.OUT)

GPIO.setup(GPIOpin4, GPIO.OUT)
GPIO.setup(GPIOpin5, GPIO.OUT)
GPIO.setup(GPIOpin6, GPIO.OUT)


GPIO.output(GPIOpin1, True)
GPIO.output(GPIOpin2, True)
GPIO.output(GPIOpin3, True)

GPIO.output(GPIOpin4, True)
GPIO.output(GPIOpin5, True)
GPIO.output(GPIOpin6, True)

freq1 = 394e6 
freq2 = 539e6 
freq3 = 614e6

atten1 = 0
atten2 = 0
atten3 = 0

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
    rf_pll_1.program_init(rf_spi)
    rf_pll_2.program_init(rf_spi)
    rf_pll_3.program_init(rf_spi)

    rf_atten1.program_init(rf_spi)
    rf_atten2.program_init(rf_spi)
    rf_atten3.program_init(rf_spi)

    f_actual_1 = rf_pll_1.set_freq(freq1) 
    f_actual_2 = rf_pll_2.set_freq(freq2) 
    f_actual_3 = rf_pll_3.set_freq(freq3) 

    atten_actual1 = rf_atten1.set_atten(atten1)
    atten_actual2 = rf_atten2.set_atten(atten2)
    atten_actual3 = rf_atten3.set_atten(atten3)

    print 'Programming ADF4355-2_1 to %g MHz' % (f_actual_1 / 1e6)
    print 'R value = %d' % (rf_pll_1.r)
    print 'INT value = %d' % (rf_pll_1.intval)
    print 'FRAC1 value = %d' % (rf_pll_1.frac1)
    print 'FRAC2 value = %d' % (rf_pll_1.frac2)
    print 'MOD2 value = %d' % (rf_pll_1.mod2)
    rf_pll_1.program_freq(rf_spi)
    time.sleep(1)
    print 'Programming ADF4355-2_2 to %g MHz' % (f_actual_2 / 1e6)
    print 'R value = %d' % (rf_pll_2.r)
    print 'INT value = %d' % (rf_pll_2.intval)
    print 'FRAC1 value = %d' % (rf_pll_2.frac1)
    print 'FRAC2 value = %d' % (rf_pll_2.frac2)
    print 'MOD2 value = %d' % (rf_pll_2.mod2)
    rf_pll_2.program_freq(rf_spi)
    time.sleep(1)
    print 'Programming ADF4355-2_3 to %g MHz' % (f_actual_3 / 1e6)
    print 'R value = %d' % (rf_pll_3.r)
    print 'INT value = %d' % (rf_pll_3.intval)
    print 'FRAC1 value = %d' % (rf_pll_3.frac1)
    print 'FRAC2 value = %d' % (rf_pll_3.frac2)
    print 'MOD2 value = %d' % (rf_pll_3.mod2)
    rf_pll_3.program_freq(rf_spi)
    
    rf_atten1.program_atten(rf_spi)
    rf_atten2.program_atten(rf_spi)
    rf_atten3.program_atten(rf_spi)
    time.sleep(1)

else :
    pass

