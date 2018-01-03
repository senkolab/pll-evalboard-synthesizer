################################################################################
#   driver for Analog Devices ADF-4355-2 PLL
################################################################################

import time
import spidev

class ADF4355:
    glob_reg1 = 0
    glob_reg2 = 0
    glob_reg3 = 0

    # register 0
    autocal = 0
    prescaler = 0
    n = 0   

    # register 1
    f = 0

    # register 2
    faux = 0
    m = 0

    # register 3
    sd_load_preset = 0
    phase_resync = 0
    phase_adjust = 0
    p = 0

    # register 4
    muxout = 0
    reference_doubler = 0
    rdiv2 = 0
    r = 0
    double_buff = 0
    current = 0
    ref_mode = 0
    mux_logic = 0
    pd_polarity = 0
    pd = 0
    cp_tristate = 0
    counter_reset = 0

    #register 5
    # all reserved

    # register 6
    gated_bleed = 0
    nevgative_bleed = 0
    feedback_select = 0
    rf_divider_select = 0
    cp_bleed_current = 0
    mtld = 0
    auxrf_output_enable = 0
    auxrf_output_power = 0
    rf_output_power = 0
    
    # register 7
    le_sync = 0
    ld_cycle_count = 0
    lol_mode = 0
    frac_n_ld_precision = 0
    ldo_mode = 0

    # register 8
    # all reserved
    
    # register 9
    vco_band_division = 0
    timeout = 0
    autolevel_timeout = 0
    synth_timeout = 0

    # register 10
    adc_clk_div = 0
    adc_conversion = 0
    adc_enable = 0

    # register 11
    # all reserved

    # register 12
    resync_clock = 0

    # constructor
    def __init__:
        pass

    # sets a frequency
    def set_freq( freq ):
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
            reg = ((vco_band_division & 0xff) << 24) | ((timeout 0x3ff) << 14) | \
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
        regnum = reg & 0x3

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
            ((timeout 0x3ff) << 14) 
            autolevel_timeout = (reg >> 9) & 0x1f 
            synth_timeout = (reg >> 4) & 0x1f 
        if( regnum == 10 ):
            adc_clk_div = (reg >> 6) & 0xff 
            adc_conversion = (reg >> 5) & 1 
            adc_enable = (reg >> 4) & 1 
        if( regnum == 12 ):
            resync_clock = (reg >> 16) & 0xffff 





        
        
