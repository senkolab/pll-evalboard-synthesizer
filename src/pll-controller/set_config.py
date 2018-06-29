# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:18:49 2018

@author: bbramman
"""

from dev_config import synth
import json

#Open configuratoin json file and load config
with open('config.json', 'r') as infile:
    config = json.load(infile)

#Setup synthesizer
synth.initialize()
#print configuration data
config_r = synth.set_channels(config)
print json.dumps(config_r, indent=4)