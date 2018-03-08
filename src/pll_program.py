################################################################################
#   SPI programmer for ADF4355-2 and ADF41020 PLL chips
#
#   Written by Rich Rademacher, 
#           1/3/2018 
#           University of Waterloo/IQC
################################################################################

import time
import spidev
import pllboard
import sys

#
# begin main program
#
mw_spi = spidev.SpiDev()
mw_spi.open(0,0)
mw_spi.cshigh = False 
mw_spi.max_speed_hz = 100000
mw_pll = pllboard.ADF41020()
do_loop = False
freq = 14.7e9

# check for command line args
if(len(sys.argv) > 1) :
    try:
        freq = float(sys.argv[1])
    except ValueError:
        if(sys.argv[1] == "loop"):
            do_loop = True

# program
if(False == do_loop) :
    print 'Programming ADF41020 to %g GHz' % (mw_pll.set_freq(freq) / 1e9)
    print 'R = %02x%02x%02x' % tuple(mw_pll.encode_register(0))
    print 'N = %02x%02x%02x' % tuple(mw_pll.encode_register(1))
    print 'F = %02x%02x%02x' % tuple(mw_pll.encode_register(2))

    mw_pll.program_reg(0, mw_spi)
    mw_pll.program_reg(1, mw_spi)
    mw_pll.program_reg(2, mw_spi)
    time.sleep(0.5)
else :
    while True:
        print 'Programming ADF41020 to %g GHz' % (mw_pll.set_freq(freq) / 1e9)
        print 'R = %02x%02x%02x' % tuple(mw_pll.encode_register(0))
        print 'N = %02x%02x%02x' % tuple(mw_pll.encode_register(1))
        print 'F = %02x%02x%02x' % tuple(mw_pll.encode_register(2))

        mw_pll.program_reg(0, mw_spi)
        mw_pll.program_reg(1, mw_spi)
        mw_pll.program_reg(2, mw_spi)
        time.sleep(0.5)
        
        if(freq > 15.5e9) :
            freq = 12e9
        else : 
            freq += 100e6
