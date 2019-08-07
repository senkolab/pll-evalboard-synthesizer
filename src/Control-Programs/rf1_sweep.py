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
GPIOpin1 = 6
#Set the current laser frequency: should be locked by wavemeter
LaserFreq = 430e12
#Set the overall sweep you want. Make sure the filter on the line isn't too low. The adf4355
FreqStart = 150e6
FreqStop = 250e6
SweepStep = 10e6
StepTime = 4


# check for command line args
if(len(sys.argv) > 1) :
    try:
        GPIOpin1 = int(sys.argv[1])
        LaserFreq = float(sys.argv[2])
        FreqStart = float(sys.argv[3])
        FreqStop = float(sys.argv[4])
        SweepStep = float(sys.argv[5])
        StepTime = float(sys.argv[6])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

rf_pll_1 = adf4355_2.ADF4355(GPIOpin1)

do_loop = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin1, GPIO.OUT)

GPIO.output(GPIOpin1, True)

# program
Freq = FreqStart
while Freq <= FreqStop:
    print'Initialize' 
    rf_pll_1.program_init(rf_spi)
#    rf_pll_2.program_init(rf_spi)
#    rf_atten.program_init(rf_spi)

    f_actual_1 = rf_pll_1.set_freq(Freq) 
#    f_actual_2 = rf_pll_2.set_freq(freq2) 
#    atten_actual = rf_atten.set_atten(atten)
    #f_actual_3 = rf_pll_3.set_freq(freq3) 
    print 'Programming ADF4355-2_1 to %g MHz' % (f_actual_1 / 1e6)
    print 'R value = %d' % (rf_pll_1.r)
    print 'INT value = %d' % (rf_pll_1.intval)
    print 'FRAC1 value = %d' % (rf_pll_1.frac1)
    print 'FRAC2 value = %d' % (rf_pll_1.frac2)
    print 'MOD2 value = %d' % (rf_pll_1.mod2)
    rf_pll_1.program_freq(rf_spi)
    Freq += SweepStep
    time.sleep(StepTime)
