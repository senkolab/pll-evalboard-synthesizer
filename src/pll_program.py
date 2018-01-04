################################################################################
#   SPI programmer for ADF4355-2 and ADF41020 PLL chips
#
#   Written by Rich Rademacher, 
#           1/3/2018 
#           University of Waterloo/IQC
################################################################################

import time
import spidev
import adf41020

#
# begin main program
#
spi = spidev.Spi()

