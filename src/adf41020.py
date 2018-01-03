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
        self.current2 = 0
        self.current1 = 0
        self.timer_contorl = 0
        self.fastlock_mode = 0
        self.fastlock_enable = 0
        self.cp_tristate = 0
        self.pd_polarity = 1    # eval board default
        self.muxout = 0
        self.powerdown1 = 0
        self.counter_reset = 0


    # get the prescaler value
    def get_prescale( ) :
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
    def set_freq( freq ):
        P = get_prescale( )
        numerator = (freq / self.fref) * (self.R)
        self.A = (int) (numerator - self.B * P) 
        return get_freq()
        

    # gets current frequency
    def get_freq( ):
        P = get_prescale()
        f_vco = (P * self.B + self.A) * (f * self.fref / self.R)
        return f_vco 

    # sets powerdown
    def set_powerdown( value ):
        pass

    # encode the binary value of each register into 32 bits per ADF 41020 datasheet Fig 15
    def encode_registers( regnum ):
        
        reg = 0

        if( regnum == 0 ):
            reg = ((R & 0x3fff) << 2) | (regnum)
        if( regnum == 1 ):
            reg = ((cp_gain & 1) << 21) | ((B & 0x1fff) << 8) | ((A & 0x3f) << 2) | (regnum)
        if( regnum == 2 ):
            reg = ((prescaler & 0x3) << 22) | ((powerdown2 & 1) << 21) | ((current2 & 0x7) << 18) \
                  | ((current1 & 0x7) << 15) | ((timer_control & 0xf) << 11) | ((fastlock_mode & 1 ) << 10) \
                  | ((fastlock_enable & 1) << 9) | ((cp_tristate & 1) << 8) | ((pd_polarity & 1) << 7) \
                  | ((muxout & 0x7) << 4) | ((powerdown_1 & 1) << 3) | ((counter_reset & 1) << 2) | (regnum)

        # split into 3 8-bit values for SPI transfer
        return [ ((reg >> 16) & 0xff), ((reg >> 8) & 0xff), (reg & 0xff) ]

        
    # decode retured bytes into the value of each register per ADF 41020 datasheet Fig 15
    def decode_registers( byte_array ):
        
        # convert individual 8-bit bytes to 32-bit word
        reg = (byte_array[2] << 16) | (byte_array[1] << 8) | (byte_array)

        # get control bits as register id
        regnum = reg & 0x3

        if( regnum == 0 ):
            R = (reg >> 2) & 0x3fff 
        if( regnum == 1 ):
            cp_gain = (reg >> 21) & 1 
            B = (reg >> 8) & 0x1fff 
            A = (reg >> 2) & 0x3f 
        if( regnum == 2 ):
            prescaler = (reg >> 22) & 0x3 
            powerdown2 = (reg >> 21) & 1 
            current2 = (reg >> 18) & 0x7 
            current1 = (reg >> 15) & 0x7 
            timer_control = (reg >> 11) & 0xf 
            fastlock_mode = (reg >> 10) & 1 
            fastlock_enable = (reg >> 9) & 1 
            cp_tristate = (reg >> 8) & 1 
            pd_polarity = (reg >> 7) & 1 
            muxout = (reg >> 4) & 0x7 
            powerdown_1 = (reg >> 3) & 1 
            counter_reset = (reg >> 2) & 1 





        
        
