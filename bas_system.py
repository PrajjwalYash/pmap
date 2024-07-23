import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


cur_path = os.getcwd()

from panel_design import *

mission_details = {
    'mission_name': 'Space_station_base_module',
    'L': 9.6,
    'W': 2.82,
    'packing_eff': 0.85,
    'bus_vlt': 100,
    'harn_drop': 7,
    'des_T': 80,
    'bol_fac_isc':0.99*0.985*0.98,
    'bol_fac_imp': 0.99*0.985*0.98,
    'bol_fac_vmp': 0.985,
    'bol_fac_voc': 0.985,
    'eol_fac_isc':0.98,
    'eol_fac_imp': 0.98,
    'eol_fac_vmp': 0.99*0.97,
    'eol_fac_voc': 0.99*0.97
    
}
mission_details['T_range']= np.arange(mission_details['des_T']-40,mission_details['des_T']+20,10)

cell_details = {
    'isc': 457.6,
    'imp': 433.5,
    'vmp': 3025,
    'voc': 3451,
    't_isc': 0.14,
    't_imp': 0.07,
    't_vmp': -9,
    't_voc': -8.8
}

ns, n_p, i_l = pan_cur(cell_details=cell_details, mission_details=mission_details)
_,_,t_results = temp_pan_cur(cell_details=cell_details, mission_details=mission_details)