# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 13:11:21 2018

@author: bbramman
"""

import time
import spidev
import math
import RPi.GPIO as GPIO

class ADF4360:
    #Constructor for ADF4360
    def __init__(self, GPIOpin, fref = 10e6):
        self.GPIOpin = GPIOpin 
        self.fref = fref * 1.0  # force float
        self.mod1 = 1<<24 #24 bit shift register
        
        #Register(Latch) 0 - Control
        self.corepower = 1
        self.countreset = 0
        self.muxout = 0
        self.phasedetpolarity = 1
        self.cpout = 0
        self.cpgain = 0
        self.mutelockdetect = 0
        self.rfpowerout = 3
        self.current1 = 7
        self.current2 = 7
        self.powerdown1 = 0
        self.powerdown2 = 0
        
        #Register(Latch) 1 - N Counter
        self.Bcounter = 200
        #This register has cpgain as well
        
        #Register(Latch) 2 - R Counter: Set at 100 for 100kHz resolution
        self.Rcounter = 10 
        self.antibacklash = 0
        self.lockdetectprecision = 0
        self.testmode = 0
        self.bandselclockdiv = 3
        
    def set_freq(self, freq):
        fref = self.fref
        #Hold the R counter at a constant
        R = self.Rcounter
        f_pfd = fref*4/R
        
        #What Ncounter is needed for the output freq
        N = freq*R/fref
        B = N 
        fract_N, int_N = math.modf(N)
        print 'fref=%g   freq=%g   pfd=%g   N=%g   int_N=%g   frac_N=%g   R=%g   B=%g   rf_vco_div=%d' % (fref, freq, f_pfd, N, int_N, fract_N, R, B, self.bandselclockdiv)
        #Set Bcounter
        self.Bcounter = int(B)
        return self.get_freq()
        
        
    def get_freq(self):
        return float(self.fref)*float(self.Bcounter)/float(self.Rcounter)
    
    def encode_registers(self, regnum):
        s = self
        reg = 0
        
        #Control register 0
        if (regnum == 0):
            reg = ((s.powerdown2 & 1) << 21)|((s.powerdown1 & 1) << 20) | ((s.current2 & 0x7) << 17) | ((s.current1 & 0x7) << 14) \
            | ((s.rfpowerout & 0x3) << 12) | ((s.mutelockdetect & 1) << 11) | ((s.cpgain & 1) << 10) | ((s.cpout & 1) << 9) \
            | ((s.phasedetpolarity & 1) << 8) | ((s.muxout & 0x7) << 5) | ((s.countreset & 1) << 4) | ((s.corepower & 0x3) << 2) | (regnum)
        #N Counter register 1
        if regnum == 2:
            reg = ((s.cpgain & 1) << 21) | ((s.Bcounter & 0x1fff) << 8) | (regnum)
        #R Counter register 2
        if regnum == 1:
            reg = ((s.bandselclockdiv & 0x3) << 20) | ((s.testmode & 1) << 19) | ((s.lockdetectprecision & 1) << 18) \
            | ((s.antibacklash & 0x3) << 16) | ((s.Rcounter & 0x1fff) << 2) | (regnum)
            
        return [((reg >> 16) & 0xff), ((reg >> 8) & 0xff), (reg & 0xff)]
    
    def decode_registers(self, byte_array):
        s = self
        reg = (byte_array[2] << 16) | (byte_array[1] << 8) | (byte_array[0])
        
        regnum = reg & 0x3
        #Control register 0
        if regnum == 0:
            s.powerdown2 = (reg >> 21) & 1
            s.powerdown1 = (reg >> 20) & 1
            s.current2 = (reg >> 17) & 0x7
            s.current1 = (reg >> 14) & 0x7
            s.rfpowerout = (reg >> 12) & 0x3
            s.mutelockdetect = (reg >> 11) & 1
            s.cpgain = (reg >> 10) & 1
            s.cpout = (reg >> 9) & 1
            s.phasedetpolarity = (reg >> 8) & 1
            s.muxout = (reg >> 5) & 0x7
            s.countreset = (reg >> 4) & 1
            s.corepower = (reg >> 2) & 0x3
        #N Counter register 1
        if regnum == 2:
            s.cpgain = (reg >> 21) & 1
            s.Bcounter = (reg >> 8) & 0x1fff
        #R Counter register 2
        if regnum == 1:
            s.bandselclockdiv = (reg >> 20) & 0x3
            s.testmode = (reg >> 19) & 1
            s.lockdetectprecision = (reg >> 18) & 1
            s.antibacklash = (reg >> 16) & 0x3
            s.Rcounter = (reg >> 2) & 0x1fff
            
        # program registers to open spi device
    def program_reg(self, regnum, spi_dev ):
        buf = self.encode_registers(regnum)
        print "programming reg %2d: %02x%02x%02x" % (regnum, buf[0], buf[1], buf[2])
        spi_dev.xfer( buf )
        
    def program_init(self, spi_dev):
        GPIO.output(self.GPIOpin, False)
        self.program_reg(2, spi_dev)
        GPIO.output(self.GPIOpin, True)
        time.sleep(400e-6)
        GPIO.output(self.GPIOpin, False)
        self.program_reg(0, spi_dev)
        GPIO.output(self.GPIOpin, True)
        time.sleep(200e-6) 
        GPIO.output(self.GPIOpin, False)
        self.program_reg(1, spi_dev)
        GPIO.output(self.GPIOpin, True)

        
    def program_freq(self, spi_dev):
        for i in range(0,3,1):
            GPIO.output(self.GPIOpin, False)
            self.program_reg(i, spi_dev)
            GPIO.output(self.GPIOpin, True)
            time.sleep(200e-6)
