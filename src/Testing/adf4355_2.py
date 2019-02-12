################################################################################
#   driver for Analog Devices ADF-4355-2 PLL
#
#   Written by Rich Rademacher, 
#           1/2/2018 
#           University of Waterloo/IQC
################################################################################

import time
import spidev
import math
import RPi.GPIO as GPIO
class ADF4355:
    # constructor
    def __init__(self, GPIOpin, fref=122.88e6, fspace=100e3):
        self.GPIOpin = GPIOpin
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
        self.cp_bleed_current = 9      # 12x3.75uA = 45uA
        self.mtld = 0                   # disabled
        self.auxrf_output_enable = 0    # enabled
        self.auxrf_output_power = 1     # eval board default -1dBm
        self.rf_output_enable = 1       # enabled
        self.rf_output_power = 3        # +5dBm
        
        # register 7
        self.le_sync = 1                # eval board default: enabled
        self.ld_cycle_count = 0         # eval board default: 1024 cycles
        self.lol_mode = 1               # disabled
        self.frac_n_ld_precision = 3    # eval board default: 5ns
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

    def hcf(self, a, b):
        if a > b:
            small = b
        else:
            small = a
        for i in range(1, small+1):
            if ((a%i == 0) and (b % i == 0)):
                hcf = i
        return hcf 

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
        #print(self.hcf(f_pfd, self.fspace))
        #self.mod2 = int(f_pfd/(self.hcf(int(f_pfd), int(self.fspace))))
        self.mod2 = 1536    # default from evb programming software
        #self.frac2 = int(((N - self.intval)*2**24-self.frac1)*self.mod2)
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
            reg = (1 << 23) | (1 <<5) |(regnum)
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
        GPIO.output(self.GPIOpin, False)
        spi_dev.xfer( buf )
        GPIO.output(self.GPIOpin, True)
        time.sleep(200e-6)


    
    # program all registers
    # program in reverse order (ADF4355-2 Datasheet pg 30
    def program_init(self, spi_dev) :
        self.counter_reset = 1
        for n in range(12, -1, -1) :
            self.program_reg(n, spi_dev)
        self.counter_reset = 0
        #GPIO.output(self.GPIOpin, True)
     
    #
    # program a new frequency
    def program_freq(self, spi_dev) :
        self.counter_reset = 1
        self.program_reg(10, spi_dev)
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

        
        
