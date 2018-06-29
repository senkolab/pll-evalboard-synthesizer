# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:19:02 2018

@author: bbramman
"""

from dev_config import synth
import json

#Create configuration json file based on current synthesizer settings
with open('config.json', 'w') as outfile:
    json.dump(synth.get_channels(), outfile, indent=4)