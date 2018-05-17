# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:32:52 2018

@author: bbramman
"""
import RPi.GPIO as GPIO

def LatchEnable(GPIO):
    GPIO.output(25, True)
    time.sleep(30e-9)
    GPIO.output(25, False)