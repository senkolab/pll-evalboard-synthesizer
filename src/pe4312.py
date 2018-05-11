# -*- coding: utf-8 -*-
"""
Created on Fri May 11 15:13:26 2018

@author: bbramman
"""

import time
import spidev
import math

class PE4312:
    #Constructor
    def __init__(self):
        self.atten = 0
        self.parallelorserial = 1
    
    def setAtten(self, atten):
        self.atten = atten
    
    def getAtten(self):
        return self.atten
    
    def encodeReg(self):
        atten = self.atten
        if atten == 0:
            attnum = 0
        elif atten == 0.5:
            attnum = 1
        elif atten == 1:
            attnum = 2
        elif atten == 2:
            attnum = 4
        elif atten == 4:
            attnum = 8
        elif atten == 8:
            attnum = 16 
        elif atten == 16:
            attnum = 32
        elif atten == 31.5:
            attnum = 63
        Reg = (self.parallelorserial & 1)<< 6 | attnum
        return Reg & 128
    
    def decodeReg(self, byte):
        pors = (byte >> 6) & 1
        self.parallelorserial = pors
        attnum = byte & 0x3f
        if attnum == 0:
            atten = 0
        elif attnum == 1:
            atten = 0.5
        elif attnum == 2:
            atten = 1
        elif attnum == 4:
            atten = 2
        elif attnum == 8:
            atten = 4
        elif attnum == 16:
            atten = 8
        elif attnum == 32:
            atten = 16
        elif attnum == 63:
            atten = 31.5
        self.atten = atten
    
        # program registers to open spi device
    def program_reg(self, spi_dev ):
        buf = self.encodeReg()
        print ("programming reg: ", buf)
        spi_dev.xfer( buf )
        
    def program_init(self, spi_dev):
        self.countreset = 1
        self.program_reg(2, spi_dev)
        self.program_reg(0, spi_dev)
        self.program_reg(1, spi_dev)
        self.countreset = 0
        
    def program_freq(self, spi_dev):
        self.get_freq(freq)
        for i in range(0,3,1):
            self.encode_registers(i)