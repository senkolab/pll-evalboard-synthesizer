# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:09:42 2018

@author: bbramman
"""

from evalboard import *

#Channel class - PLL and its attenuator
class Channel:
    #If no attenuator given, set as None
    def __init__(self, pll, attenuator=None):
        self.pll = pll
        self.attenuator = attenuator
        self.freq = None
        self.atten = None

    def initialize_chanel(self):
        self.pll.gpio_init()
        
        #Program gpio for attenuator
        if self.attenuator is not None:
            self.attenuator.gpio_init()
            self.attenuator.program_atten()

        #Initialize PLL
        self.pll.program_init()

        self.freq = self.pll.get_freq()
        self.atten = self.attenuator.get_atten()
        
    #Change frequency of channel
    def set_freq(self, freq):
        if freq is None:
            return
        #Try each type of PLL, return error if didn't use an implimented PLL
        if isinstance(self.pll, ADF4355):
            self.pll.set_freq(freq)
            self.pll.program_freq()
            self.freq = self.pll.get_freq()
        elif isinstance(self.pll, ADF41020):
            self.pll.set_freq(freq)
            self.pll.program_freq()
            self.freq=self.pll.get_freq()
        elif isinstance(self.pll, ADF4360):
            self.pll.set_freq(freq)
            self.pll.program_freq()
            self.freq=self.pll.get_freq()
        else:
            raise NotImplementedError
            
    #Change attenuation of channel
    def set_atten(self, atten):
        if atten is None:
            return

        if self.attenuator is None:
            raise ValueError("No attenuator in this channel!")
        
        #Try each type of Attenuator, return error if non implimented attenuator
        if isinstance(self.attenuator, PE4312):
            self.attenuator.set_atten(atten)
            self.attenuator.program_atten()
            self.atten = self.attenuator.get_atten()
        else:
            raise NotImplementedError

#Synthesizer class - All channels
class Synthesizer:
    def __init__(self, channels):
        #Channels must be a dict data type
        if not isinstance(channels, dict):
            raise TypeError()
        self.channels = channels

    def initialize(self):
        #Initialize each channel's GPIOs
        for ch in self.channels.itervalues():
            ch.initialize_chanel()
    
    #Set each individual channel
    def set_channel(self, channel_config):
        channel_config_r = dict()
        name = channel_config["Name"]
        channel_config_r["Name"] = name
        ch = self.channels[name]
        ch.set_freq(channel_config["Frequency"])
        channel_config_r["Frequency"] = ch.freq
        try:
            ch.set_atten(channel_config["Attenuation"])
            channel_config_r["Attenuation"] = ch.atten
        except KeyError:
            pass
        return channel_config_r

    #Get the config of a channel
    def get_channel(self, name):
        ch = self.channels[name]
        channel_config_r = dict()
        channel_config_r["Name"] = name
        channel_config_r["Frequency"] = ch.freq
        channel_config_r["Attenuation"] = ch.atten
        return channel_config_r

    #Set each channel
    def set_channels(self, config):
        config_r = []
        #Set each channel, append config of each to config_r
        for channel_config in config:
            channel_config_r = self.set_channel(channel_config)
            config_r.append(channel_config_r)
        #Return list of channel configurations
        return config_r

    #Get all channels
    def get_channels(self):
        config_r = []
        for name, ch in self.channels.iteritems():
            config_r.append(self.get_channel(name))
        return config_r