# -*- coding: utf-8 -*-
"""
Created on Fri May 11 15:13:26 2018

@author: bbramman
"""

import time
import spidev
import math
import RPi.GPIO as GPIO

class PE4312:
    #Constructor
    def __init__(self, GPIOpin):
        self.GPIOpin = GPIOpin
        self.atten = 0
        self.parallelorserial = 1
    
    def set_atten(self, atten):
        self.atten = atten
        return atten
    
    def get_atten(self):
        return self.atten
    
    def encode_registers(self):
        atten = self.atten
        att = int(math.floor(atten*2))
        print(att)
        Reg = att
        return Reg
    
    def decode_registers(self, byte):
        attnum = byte & 0x3f
        att = attnum/2
        self.atten = att
    
        # program registers to open spi device
    def program_reg(self, spi_dev ):
        buf = self.encode_registers()
        buf = [buf]
        print "programming Data:", buf
        GPIO.output(self.GPIOpin, True)
        time.sleep(10e-6)
        GPIO.output(self.GPIOpin, False)
        spi_dev.xfer( buf )
        time.sleep(10e-6)
        GPIO.output(self.GPIOpin, True)
        time.sleep(10e-6)
        GPIO.output(self.GPIOpin, False)
        
    def program_init(self, spi_dev):
        self.program_reg(spi_dev)
        
    def program_atten(self, spi_dev):
        self.program_reg(spi_dev)
