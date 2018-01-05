################################################################################
#   driver for Analog Devices ADF-41020 PLL
#
#   Written by Rich Rademacher, 
#           1/2/2018 
#           University of Waterloo/IQC
################################################################################

import time
import spidev

class ADF41020:
    # constructor
    def __init__(self, fref=100e6):
        self.fref = fref * 1.0      # force float

        # register 0 (Reference Counter Latch)
        self.R = (int) ( 100e6 / 2.5e6 ) # Eval board defaults

        # register 1 (N Counter Latch)
        self.cp_gain = 0
        self.B = 0
        self.A = 0

        # register 2 (Function Latch)
        self.prescaler = 1      # eval board default
        self.powerdown2 = 0
        self.current2 = 3       # eval board default
        self.current1 = 3       # eval board default
        self.timer_control = 0
        self.fastlock_mode = 0
        self.fastlock_enable = 0
        self.cp_tristate = 0
        self.pd_polarity = 0    # eval board default
        self.muxout = 0
        self.powerdown1 = 0
        self.counter_reset = 0


    # get the prescaler value
    def get_prescale( self ) :
        if(self.prescaler == 0) :
            return 8
        if(self.prescaler == 1) : 
            return 16
        if(self.prescaler == 2) :
            return 32
        if(self.prescaler == 3) :
            return 64
        return 0
 
    # sets a frequency
    # basic equation is f_vco = (P*B + A) / R * fref
    def set_freq( self, freq ):
        P = self.get_prescale( )
        numerator = (freq / self.fref) * (self.R) / 4
        self.B = (int) (numerator // P)
        self.A = (int) (numerator - self.B * P) 
        return self.get_freq()
        

    # gets current frequency
    def get_freq( self ):
        P = self.get_prescale( )
        f_vco = 4 * (P * self.B + self.A) * (self.fref / self.R)
        return f_vco 

    # sets powerdown
    def set_powerdown( self, value ):
        pass

    # encode the binary value of each register into 32 bits per ADF 41020 datasheet Fig 15
    def encode_register( self, regnum ):
        
        reg = 0

        if( regnum == 0 ):
            reg = (0x91 << 16) | ((self.R & 0x3fff) << 2) | (regnum)
        if( regnum == 1 ):
            reg = ((self.cp_gain & 1) << 21) | ((self.B & 0x1fff) << 8) | ((self.A & 0x3f) << 2) | (regnum)
        if( regnum == 2 ):
            reg = ((self.prescaler & 0x3) << 22) | ((self.powerdown2 & 1) << 21) | ((self.current2 & 0x7) << 18) \
                  | ((self.current1 & 0x7) << 15) | ((self.timer_control & 0xf) << 11) | ((self.fastlock_mode & 1 ) << 10) \
                  | ((self.fastlock_enable & 1) << 9) | ((self.cp_tristate & 1) << 8) | ((self.pd_polarity & 1) << 7) \
                  | ((self.muxout & 0x7) << 4) | ((self.powerdown1 & 1) << 3) | ((self.counter_reset & 1) << 2) | (regnum)

        # split into 3 8-bit values for SPI transfer
        return [ ((reg >> 16) & 0xff), ((reg >> 8) & 0xff), (reg & 0xff) ]

        
    # decode retured bytes into the value of each register per ADF 41020 datasheet Fig 15
    def decode_register( self, byte_array ):
        
        # convert individual 8-bit bytes to 32-bit word
        reg = (byte_array[2] << 16) | (byte_array[1] << 8) | (byte_array)

        # get control bits as register id
        regnum = reg & 0x3

        if( regnum == 0 ):
            self.R = (reg >> 2) & 0x3fff 
        if( regnum == 1 ):
            self.cp_gain = (reg >> 21) & 1 
            self.self.B = (reg >> 8) & 0x1fff 
            self.A = (reg >> 2) & 0x3f 
        if( regnum == 2 ):
            self.prescaler = (reg >> 22) & 0x3 
            self.powerdown2 = (reg >> 21) & 1 
            self.current2 = (reg >> 18) & 0x7 
            self.current1 = (reg >> 15) & 0x7 
            self.timer_control = (reg >> 11) & 0xf 
            self.fastlock_mode = (reg >> 10) & 1 
            self.fastlock_enable = (reg >> 9) & 1 
            self.cp_tristate = (reg >> 8) & 1 
            self.pd_polarity = (reg >> 7) & 1 
            self.muxout = (reg >> 4) & 0x7 
            self.powerdown1 = (reg >> 3) & 1 
            self.counter_reset = (reg >> 2) & 1 
    
    
    # program registers to open spi device
    def program_reg( self, regnum, spi_dev ):
        spi_dev.xfer( self.encode_register(regnum) )




        
        
