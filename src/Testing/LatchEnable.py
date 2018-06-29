# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:32:52 2018

@author: bbramman
"""
import RPi.GPIO as GPIO
import time

def LatchEnable(GPIOpin):
    GPIO.output(GPIOpin, True)
    time.sleep(40e-9)
    GPIO.output(GPIOpin, False)
    print "Latch Enabled"
