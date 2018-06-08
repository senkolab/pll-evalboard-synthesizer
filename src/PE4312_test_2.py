# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:38:05 2018

@author: bbramman
"""

import spidev
import sys
import time
import pe4312
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi_dev = 0
spi_cs = 1
spi.open(spi_dev, spi_cs)
spi.max_speed_hz = 7629
spi.cshigh = False 
GPIOpin = 24 
attenuator = pe4312.PE4312(GPIOpin)
do_loop = False
atten = 23 
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin, GPIO.OUT)
GPIO.output(GPIOpin, True)


# check for command line args
if(len(sys.argv) > 1) :
    try:
        atten = float(sys.argv[1])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

# program
if(False == do_loop) :
    print 'Initialize' 
    attenuator.program_init(spi)
    atten_actual = attenuator.set_atten(atten) 
    print 'Programming PE4312 to %g Attenuation' % (atten_actual)
    attenuator.program_atten(spi)
    time.sleep(0.5)
else :
    pass
