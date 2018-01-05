################################################################################
#   driver for Analog Devices ADF-4355-2 PLL
#
#   Written by Rich Rademacher, 
#           1/2/2018 
#           University of Waterloo/IQC
################################################################################

import time
import spidev

class ADF4355:
    # constructor
    def __init__(self, fref=122.88e6):
        self.fref = fref * 1.0  # force float
        
        # register 0
        self.autocal = 0
        self.prescaler = 0
        self.n = 0   

        # register 1
        self.f = 0

        # register 2
        self.faux = 0
        self.m = 0

        # register 3
        self.sd_load_preset = 0
        self.phase_resync = 0
        self.phase_adjust = 0
        self.p = 0

        # register 4
        self.muxout = 0
        self.reference_doubler = 0
        self.rdiv2 = 0
        self.r = 0
        self.double_buff = 0
        self.current = 0
        self.ref_mode = 0
        self.mux_logic = 0
        self.pd_polarity = 0
        self.pd = 0
        self.cp_tristate = 0
        self.counter_reset = 0

        #register 5
        # all reserved

        # register 6
        self.gated_bleed = 0
        self.nevgative_bleed = 0
        self.feedback_select = 0
        self.rf_divider_select = 0
        self.cp_bleed_current = 0
        self.mtld = 0
        self.auxrf_output_enable = 0
        self.auxrf_output_power = 0
        self.rf_output_power = 0
        
        # register 7
        self.le_sync = 0
        self.ld_cycle_count = 0
        self.lol_mode = 0
        self.frac_n_ld_precision = 0
        self.ldo_mode = 0

        # register 8
        # all reserved
        
        # register 9
        self.vco_band_division = 0
        self.timeout = 0
        self.autolevel_timeout = 0
        self.synth_timeout = 0

        # register 10
        self.adc_clk_div = 0
        self.adc_conversion = 0
        self.adc_enable = 0

        # register 11
        # all reserved

        # register 12
        self.resync_clock = 0


    # sets a frequency
    def set_freq( freq ):
        D = reference_doubler
        R = 1.0 # fixme
        # from ADF4355-2 dadasheet rev C pg 13
        f_pfd = fref * (1 + D) / (R * (1 + T))
        f_vco = freq * 
        N = 1.0 #fixme

# gets current frequency
    def get_freq( ):
        pass



    # sets powerdown
    def set_powerdown( value ):
        pass

    # encode the binary value of each register into 32 bits per ADF 4355-2 datasheet Fig 29
    def encode_registers( regnum ):
        
        reg = 0

        if( regnum == 0 ):
            reg = ((autocal & 1) << 21) | ((prescaler & 1) << 20) | ((n & 0xffff) << 4) | (regnum)
        if( regnum == 1 ):
            reg = ((f & 0xffffff) << 4) | (regnum)
        if( regnum == 2 ):
            reg = ((faux & 0x3fff) << 18) | ((m & 0x3fff) << 4) | (regnum)
        if( regnum == 3 ):
            reg = ((sd_load_reset & 1) << 30) | ((phase_resync & 1) << 29) | ((phase_adjust & 1) << 28) \
                  | ((p & 0xffffff) << 4) | (regnum)
        if( regnum == 4 ):
            reg = ((muxout & 0x7) << 27) | ((reference_doubler & 1) << 26) | ((rdiv2 & 1) << 25) \
                  | ((r & 0x3ff) << 15) | ((double_buf & 1) << 14) | ((current & 0xf) << 10) \
                  | ((ref_mode & 1) << 9) | ((mux_logic & 1) << 8) | ((pd_polarity & 1) << 7) \
                  | ((pd & 1) << 6) | ((cp_tristate & 1) << 5) | ((counter_reset & 1) << 4)  | regnum
        if( regnum == 5 ):
            reg = (regnum)
        if( regnum == 6 ):
            reg = ((gate_bleed & 1) << 30) | ((negative_bleed & 1) << 29) | ((feedback_select & 1) << 24) \
                  | ((rf_divider_select & 0x7) << 21) | ((cp_bleed_current & 0xff) << 13) | ((mltd & 1) << 11) \
                  | ((auxrf_output_enable & 1) << 9) | ((auxrf_output_power & 0x3) << 7) \
                  | ((rf_output_enable & 1) << 6) | ((rf_output_power & 0x3) << 4)| (regnum)
        if( regnum == 7 ):
            reg = ((le_sync & 1) << 25) | ((ld_cycle_count & 0x3) << 8) | ((lol_mode & 1) << 7) \
                  | (( frac_n_ld_precision & 0x3) << 5) | (( ldo_mode & 1) << 4) | (regnum)
        if( regnum == 8 ):
            reg = (regnum)
        if( regnum == 9 ):
            reg = ((vco_band_division & 0xff) << 24) | ((timeout & 0x3ff) << 14)  \
                  | ((autolevel_timeout & 0x1f) << 9) | ((synth_timeout & 0x1f) << 4) | (regnum)
        if( regnum == 10 ):
            reg = ((adc_clk_div & 0xff) << 6) | ((adc_conversion & 1) << 5) | ((adc_enable & 1) << 4) \
                  | (regnum)
        if( regnum == 11 ):
            reg = 0 (regnum)
        if( regnum == 12 ):
            reg = ((resync_clock & 0xffff) << 16) | (regnum)

        # split into 4 8-bit values for SPI transfer
        return [ ((reg >> 24) & 0xff), ((reg >> 16) & 0xff), ((reg >> 8) & 0xff), (reg & 0xff) ]

        
    # decode retured bytes into the value of each register per ADF 4355-2 datasheet Fig 29
    def decode_registers( byte_array ):
        
        # convert individual 8-bit bytes to 32-bit word
        reg = (byte_array[3] << 24) | (byte_array[2] << 16) | (byte_array[1] << 8) | (byte_array)

        # get control bits as register id
        regnum = reg & 0xf

        if( regnum == 0 ):
            autocal = (reg >> 21) & 1 
            prescaler = (reg >> 20) & 1 
            n = (reg >> 4) & 0xffff 
        if( regnum == 1 ):
            f = (reg >> 4) & 0xffffff 
        if( regnum == 2 ):
            faux = (reg >> 18) & 0x3fff 
            m = (reg >> 4) & 0x3fff 
        if( regnum == 3 ):
            sd_load_reset = (reg >> 30) & 1 
            phase_resync = (reg >> 29) & 1 
            phase_adjust = (reg >> 28) & 1 
            p = (reg >> 4) & 0xffffff 
        if( regnum == 4 ):
            muxout = (reg >> 27) & 0x7 
            reference_doubler = (reg >> 26) & 1 
            rdiv2 = (reg >> 25) & 1 
            r = (reg >> 15) & 0x3ff 
            double_buf = (reg >> 14) & 1 
            current = (reg >> 10) & 0xf 
            ref_mode = (reg >> 9) & 1 
            mux_logic = (reg >> 8) & 1 
            pd_polarity = (reg >> 7) & 1
            pd = (reg >> 6) & 1 
            cp_tristate = (reg >> 5) & 1 
            counter_reset = (reg >> 4) & 1  
        if( regnum == 6 ):
            gate_bleed = (reg >> 30) & 1 
            negative_bleed = (reg >> 29) & 1 
            feedback_select = (reg >> 24) & 1 
            rf_divider_select = (reg >> 21) & 0x7 
            cp_bleed_current = (reg >> 13) & 0xff 
            mltd = (reg >> 11) & 1 
            auxrf_output_enable = (reg >> 9) & 1 
            auxrf_output_power = (reg >> 7) & 0x3 
            rf_output_enable = (reg >> 6) & 1 
            rf_output_power = (reg >> 4) & 0x3
        if( regnum == 7 ):
            le_sync = (reg >> 25) & 1 
            ld_cycle_count = (reg >> 8) & 0x3 
            lol_mode = (reg >> 7) & 1 
            frac_n_ld_precision = (reg >> 5) & 0x3 
            ldo_mode = (reg >> 4) & 1 
        if( regnum == 9 ):
            vco_band_division = (reg >> 24) & 0xff 
            timeout = (reg >> 14) & 0x3ff
            autolevel_timeout = (reg >> 9) & 0x1f 
            synth_timeout = (reg >> 4) & 0x1f 
        if( regnum == 10 ):
            adc_clk_div = (reg >> 6) & 0xff 
            adc_conversion = (reg >> 5) & 1 
            adc_enable = (reg >> 4) & 1 
        if( regnum == 12 ):
            resync_clock = (reg >> 16) & 0xffff 





        
        
