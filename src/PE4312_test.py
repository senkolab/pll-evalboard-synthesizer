# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:38:05 2018

@author: bbramman
"""

import LatchEnable
import spidev
import time
import pe4312

spi = spidev.SpiDev()
spi_dev = 0
spi_cs = 1
spi.open(spi_dev, spi_cs)
spi.max_speed_hz = 7629
spi.cshigh = False 
atten = pe4312.PE4312()
do_loop = False
attenuation = 4


GPIOpin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOpin, GPIO.OUT)

# check for command line args
if(len(sys.argv) > 1) :
    try:
        atten = float(sys.argv[1])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

# program
if(False == do_loop) :
    while True:
        print 'Initialize' 
        atten.program_init(spi)

        atten_actual = atten.set_atten(atten) 
        print 'Programming PE4312 to %g Attenuation' % (atten_actual)

        atten.program_atten(spi)

        LatchEnable(GPIOpin)

        time.sleep(0.5)
    else :
        pass
