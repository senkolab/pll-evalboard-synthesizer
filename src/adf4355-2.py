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
    # f shared w/ reg 1
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

    def encode_registers( ):
        pass
        
