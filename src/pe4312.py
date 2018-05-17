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
    
    def set_atten(self, atten):
        self.atten = atten
    
    def get_atten(self):
        return self.atten
    
    def encode_registers(self):
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
        Reg = attnum
        return Reg & 128
    
    def decode_registers(self, byte):
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
        buf = self.encode_registers()
        print "programming reg: ", buf
        spi_dev.xfer( buf )
        
    def program_init(self, spi_dev):
        self.program_reg(spi_dev)
        
    def program_atten(self, spi_dev):
        self.program_reg(spi_dev)