################################################################################
#   SPI programmer for ADF4355-2 and ADF41020 PLL chips
#
#   Written by Rich Rademacher, 
#           1/3/2018 
#           University of Waterloo/IQC
################################################################################

import spidev
import time
import spidev
import math


class PllEvalBoard:
    def program_freq(self, spi_dev) :
        pass

    def program_init(self, spi_dev) :
        pass

    def set_freq( self, freq):
        pass

class ADF4355(PllEvalBoard):
    # constructor
    def __init__(self, fref=122.88e6, fspace=100e3):
        self.fref = fref * 1.0  # force float
        self.fspace = fspace * 1.0
        self.mod1 = 1 << 24     # fixed modulus: datasheet pg 13

        # register 0
        self.autocal = 1
        self.prescaler = 0
        self.intval = 0   

        # register 1
        self.frac1 = 7077888    # default from evb programming software

        # register 2
        self.frac2 = 0
        self.mod2 = 1536  # default from evb software

        # register 3
        self.sd_load_reset = 0
        self.phase_resync = 0
        self.phase_adjust = 0
        self.p = 0

        # register 4
        self.muxout = 6         # digital lock det
        self.reference_doubler = 0
        self.rdiv2 = 1          # enabled
        self.r = 1              # eval board default
        self.double_buf = 0     # disabled
        self.current = 2        # eval board default: 0.93mA
        self.ref_mode = 1       # eval board default: differential
        self.mux_logic = 1      # eval board default: 3.3v
        self.pd_polarity = 1    # eval board default: positive
        self.pd = 0             # power down
        self.cp_tristate = 0    # disable
        self.counter_reset = 0  # disable

        #register 5
        # all reserved

        # register 6
        self.gated_bleed = 0            # disabled
        self.negative_bleed = 1         # enabled 
        self.feedback_select = 1        # fundamental
        self.rf_divider_select = 2      # eval board default: div-by-4
        self.cp_bleed_current = 12      # 12x3.75uA = 45uA
        self.mtld = 0                   # disabled
        self.auxrf_output_enable = 1    # enabled
        self.auxrf_output_power = 1     # eval board default -1dBm
        self.rf_output_enable = 1       # enabled
        self.rf_output_power = 3        # +5dBm
        
        # register 7
        self.le_sync = 1                # eval board default: enabled
        self.ld_cycle_count = 0         # eval board default: 1024 cycles
        self.lol_mode = 0               # disabled
        self.frac_n_ld_precision = 0    # eval board default: 5ns
        self.ld_mode = 0                # fractional-n

        # register 8
        # all reserved
        
        # register 9
        self.vco_band_division = 26     # eval board autoset
        self.timeout = 103              # eval board autoset
        self.autolevel_timeout = 30     # eval board autoset
        self.synth_timeout = 12         # eval board autoset

        # register 10
        self.adc_clk_div = 154          # eval board autoset
        self.adc_conversion = 1         # eval board default: enabled
        self.adc_enable = 1             # eval board default: enabled

        # register 11
        # all reserved

        # register 12
        self.resync_clock = 1


    # get the ouptut divider ratio
    #   ref adf4355-2 datasheet page 25
    def get_output_divider(self) :
        T = self.rf_divider_select
        if(T <= 7) :
            return (1 << T)     # equiv 2^T
        else :
            return 1


    # sets a frequency
    def set_freq( self, freq ):
        D = self.reference_doubler
        R = self.r
        T = self.rdiv2

        # div_out forces VCO to 3400 - 6800 MHz
        self.rf_divider_select = int( math.ceil(math.log(3400e6 / freq, 2)) )
        div_out = self.get_output_divider()

        # from ADF4355-2 datasheet rev C pg 13
        f_pfd = self.fref * (1 + D) / (R * (1 + T))
        f_vco = freq * div_out
        N = f_vco / f_pfd

        fract_N, int_N = math.modf(N)
        print 'fref=%g   freq=%g   div=%d   pfd=%g   vco=%g   N=%g   int_N=%g   frac_N=%g   rf_div_sel=%d' \
                % (self.fref, freq, div_out, f_pfd, f_vco, N, int_N, fract_N, self.rf_divider_select)

        # ignore optimization - just use frac2=0 for simplicity
        # frac1 = math.floor(fract_N * self.mod1)
        # mod2 = f_pdf / math.gcd(f_pfd, self.fspace)
        # frac2 = ((N - int_N)*self.mod1 - frac1) * mod2
        self.intval = int(int_N)
        self.frac1 = int(math.floor(fract_N * self.mod1))  # frac1 = remainder * 2^24
        self.frac2 = 0
        self.mod2 = 1536    # default from evb programming software
        return self.get_freq()

    #
    # gets current frequency
    def get_freq( self ):
        return self.fref * float(1+self.reference_doubler) / float(self.r) / float(1 + self.rdiv2) * \
                ( float(self.intval) + \
                ( float( self.frac1 + self.frac2/self.mod2) / float(self.mod1) )) \
                 / float(self.get_output_divider())
 
    # sets powerdown
    def set_powerdown( self, value ):
        pass

    # encode the binary value of each register into 32 bits per ADF 4355-2 datasheet Fig 29
    def encode_registers( self, regnum ):
        s = self 
        reg = 0

        if( regnum == 0 ):
            reg = ((s.autocal & 1) << 21) | ((s.prescaler & 1) << 20) | ((s.intval & 0xffff) << 4) | (regnum)
        if( regnum == 1 ):
            reg = ((s.frac1 & 0xffffff) << 4) | (regnum)
        if( regnum == 2 ):
            reg = ((s.frac2 & 0x3fff) << 18) | ((s.mod2 & 0x3fff) << 4) | (regnum)
        if( regnum == 3 ):
            reg = ((s.sd_load_reset & 1) << 30) | ((s.phase_resync & 1) << 29) | ((s.phase_adjust & 1) << 28) \
                  | ((s.p & 0xffffff) << 4) | (regnum)
        if( regnum == 4 ):
            reg = ((s.muxout & 0x7) << 27) | ((s.reference_doubler & 1) << 26) | ((s.rdiv2 & 1) << 25) \
                  | ((s.r & 0x3ff) << 15) | ((s.double_buf & 1) << 14) | ((s.current & 0xf) << 10) \
                  | ((s.ref_mode & 1) << 9) | ((s.mux_logic & 1) << 8) | ((s.pd_polarity & 1) << 7) \
                  | ((s.pd & 1) << 6) | ((s.cp_tristate & 1) << 5) | ((s.counter_reset & 1) << 4)  | regnum
        if( regnum == 5 ):
            reg = (1 << 23) | (regnum)
        if( regnum == 6 ):
            reg = ((s.gated_bleed & 1) << 30) | ((s.negative_bleed & 1) << 29) | (0xa << 25) \
                  | ((s.feedback_select & 1) << 24) | ((s.rf_divider_select & 0x7) << 21) \
                  | ((s.cp_bleed_current & 0xff) << 13) | ((s.mtld & 1) << 11) \
                  | ((s.auxrf_output_enable & 1) << 9) | ((s.auxrf_output_power & 0x3) << 7) \
                  | ((s.rf_output_enable & 1) << 6) | ((s.rf_output_power & 0x3) << 4)| (regnum)
        if( regnum == 7 ):
            reg = (1<<28) | ((s.le_sync & 1) << 25) | ((s.ld_cycle_count & 0x3) << 8) \
                  | ((s.lol_mode & 1) << 7) | (( s.frac_n_ld_precision & 0x3) << 5) \
                  | (( s.lol_mode & 1) << 4) | (regnum)
        if( regnum == 8 ):
            reg = (0x102D042 << 4) | (regnum)
        if( regnum == 9 ):
            reg = ((s.vco_band_division & 0xff) << 24) | ((s.timeout & 0x3ff) << 14)  \
                  | ((s.autolevel_timeout & 0x1f) << 9) | ((s.synth_timeout & 0x1f) << 4) | (regnum)
        if( regnum == 10 ):
            reg = (0x3 << 22) | ((s.adc_clk_div & 0xff) << 6) | ((s.adc_conversion & 1) << 5) \
                  | ((s.adc_enable & 1) << 4) | (regnum)
        if( regnum == 11 ):
            reg = (0x0061300 << 4) | (regnum)
        if( regnum == 12 ):
            reg = ((s.resync_clock & 0xffff) << 16) | (1 << 10) | (1 << 4) | (regnum)

        # split into 4 8-bit values for SPI transfer
        return [ ((reg >> 24) & 0xff), ((reg >> 16) & 0xff), ((reg >> 8) & 0xff), (reg & 0xff) ]

        
    # decode retured bytes into the value of each register per ADF 4355-2 datasheet Fig 29
    def decode_registers( self, byte_array ):

        s = self
        
        # convert individual 8-bit bytes to 32-bit word
        reg = (byte_array[3] << 24) | (byte_array[2] << 16) | (byte_array[1] << 8) | (byte_array)

        # get control bits as register id
        regnum = reg & 0xf

        if( regnum == 0 ):
            s.autocal = (reg >> 21) & 1 
            s.prescaler = (reg >> 20) & 1 
            s.intval = (reg >> 4) & 0xffff 
        if( regnum == 1 ):
            s.frac1 = (reg >> 4) & 0xffffff 
        if( regnum == 2 ):
            s.frac2 = (reg >> 18) & 0x3fff 
            s.mod2 = (reg >> 4) & 0x3fff 
        if( regnum == 3 ):
            s.sd_load_reset = (reg >> 30) & 1 
            s.phase_resync = (reg >> 29) & 1 
            s.phase_adjust = (reg >> 28) & 1 
            s.p = (reg >> 4) & 0xffffff 
        if( regnum == 4 ):
            s.muxout = (reg >> 27) & 0x7 
            s.reference_doubler = (reg >> 26) & 1 
            s.rdiv2 = (reg >> 25) & 1 
            s.r = (reg >> 15) & 0x3ff 
            s.double_buf = (reg >> 14) & 1 
            s.current = (reg >> 10) & 0xf 
            s.ref_mode = (reg >> 9) & 1 
            s.mux_logic = (reg >> 8) & 1 
            s.pd_polarity = (reg >> 7) & 1
            s.pd = (reg >> 6) & 1 
            s.cp_tristate = (reg >> 5) & 1 
            s.counter_reset = (reg >> 4) & 1  
        if( regnum == 6 ):
            s.gated_bleed = (reg >> 30) & 1 
            s.negative_bleed = (reg >> 29) & 1 
            s.feedback_select = (reg >> 24) & 1 
            s.rf_divider_select = (reg >> 21) & 0x7 
            s.cp_bleed_current = (reg >> 13) & 0xff 
            s.mtld = (reg >> 11) & 1 
            s.auxrf_output_enable = (reg >> 9) & 1 
            s.auxrf_output_power = (reg >> 7) & 0x3 
            s.rf_output_enable = (reg >> 6) & 1 
            s.rf_output_power = (reg >> 4) & 0x3
        if( regnum == 7 ):
            s.le_sync = (reg >> 25) & 1 
            s.ld_cycle_count = (reg >> 8) & 0x3 
            s.lol_mode = (reg >> 7) & 1 
            s.frac_n_ld_precision = (reg >> 5) & 0x3 
            s.lol_mode = (reg >> 4) & 1 
        if( regnum == 9 ):
            s.vco_band_division = (reg >> 24) & 0xff 
            s.timeout = (reg >> 14) & 0x3ff
            s.autolevel_timeout = (reg >> 9) & 0x1f 
            s.synth_timeout = (reg >> 4) & 0x1f 
        if( regnum == 10 ):
            s.adc_clk_div = (reg >> 6) & 0xff 
            s.adc_conversion = (reg >> 5) & 1 
            s.adc_enable = (reg >> 4) & 1 
        if( regnum == 12 ):
            s.resync_clock = (reg >> 16) & 0xffff 




    # program registers to open spi device
    def program_reg( self, regnum, spi_dev ):
        buf = self.encode_registers(regnum)
        print "programming reg %2d: %02x%02x%02x%02x" % (regnum, buf[0], buf[1], buf[2], buf[3])
        spi_dev.xfer( buf )


    
    # program all registers
    # program in reverse order (ADF4355-2 Datasheet pg 30
    def program_init(self, spi_dev) :
        self.counter_reset = 1
        for n in range(12, -1, -1) :
            self.program_reg(n, spi_dev)
        self.counter_reset = 0
     
    #
    # program a new frequency
    def program_freq(self, spi_dev) :
        self.counter_reset = 1
        self.program_reg(6, spi_dev)
        self.program_reg(4, spi_dev)
        self.program_reg(2, spi_dev)
        self.program_reg(1, spi_dev)

        self.autocal = 0
        self.program_reg(0, spi_dev)
        self.counter_reset = 0
        self.program_reg(4, spi_dev)

        self.autocal = 1
        self.program_reg(0, spi_dev)

class ADF41020(PllEvalBoard):
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
        self.pd_polarity = 1    # eval board default
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
