# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:17:30 2018

@author: bbramman
"""

from evalboard import *
from synthesizer import *
import spidev

#Setup spy on rPi
device_spi = spidev.SpiDev()
device_spi.open(0, 0)
device_spi.cshigh = False
device_spi.max_speed_hz = 100000

#pll_spi = spidev.SpiDev()
#pll_spi.open(0, 0)
#pll_spi.cshigh = False
#pll_spi.max_speed_hz = 100000
#
#atten_spi = spidev.SpiDev()
#atten_spi.open(1, 1)
#atten_spi.max_speed_hz = 7629
#atten_spi.cshigh = False

#Setup all channels
channels = {
    "cooling_aom": Channel(ADF4355(25, pll_spi), attenuator=PE4312(24, atten_spi)),
}

#Setup Synthesizer class
synth = Synthesizer(channels)