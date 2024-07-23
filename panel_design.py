import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def pan_cur(cell_details, mission_details):
    cur_path = os.getcwd()
    if cell_details['voc']==3451:
        cell_type = '4J_cell'
    else:
        cell_type = '3J_cell'
    voc_t = cell_details['voc']+cell_details['t_voc']*(mission_details['des_T']-28)
    vmp_t = cell_details['vmp']+cell_details['t_vmp']*(mission_details['des_T']-28)
    isc_t = cell_details['isc']+cell_details['t_isc']*(mission_details['des_T']-28)
    imp_t = cell_details['imp']+cell_details['t_imp']*(mission_details['des_T']-28)
    voc_t_eol,vmp_t_eol,isc_t_eol,imp_t_eol = voc_t*mission_details['bol_fac_voc']*mission_details['eol_fac_voc'], vmp_t*mission_details['bol_fac_vmp']*mission_details['eol_fac_vmp'],\
                                            isc_t*mission_details['bol_fac_isc']*mission_details['eol_fac_isc'], imp_t*mission_details['bol_fac_imp']*mission_details['eol_fac_imp']
    print('voc, vmp, isc, imp=',  voc_t_eol,vmp_t_eol,isc_t_eol,imp_t_eol)
    ns = (mission_details['bus_vlt']+mission_details['harn_drop'])/(vmp_t_eol/1000)
    ns = int(np.round(ns,0))
    print('ns = ', ns)
    A = mission_details['L']*mission_details['W']
    A_eff = A*mission_details['packing_eff']
    cell_area = 32.2/10000
    one_p_area = cell_area*ns
    n_p = A_eff/one_p_area
    n_p=np.floor(n_p)
    print('np = ', n_p)
    i_sc, i_mp, v_mp, v_oc = isc_t_eol/1000,imp_t_eol/1000, vmp_t_eol/1000, voc_t_eol/1000
    v_l = (np.arange(0, mission_details['bus_vlt']+20,1)+mission_details['harn_drop'])/ns
    c3 = 0.000000001
    m = np.log(np.log((i_sc*(1+c3)-i_mp)/(c3*i_sc))/(np.log((1+c3)/c3)))/np.log(v_mp/v_oc)
    i_l = i_sc*(1-c3*np.exp((np.log(((1+c3)/c3))/v_oc**m) * v_l**m - 1))
    i_l[i_l<0] = 0
    print('Panel Current at {} V = {}'.format(mission_details['bus_vlt'] , i_l[-20]*n_p))
    df = pd.DataFrame(columns= ['Bus_vlt'])
    df['Bus_vlt'] = np.arange(0, mission_details['bus_vlt']+20,1)
    df['Panel_cur'] = n_p*i_l
    folder_path = os.path.join(cur_path, 'Exports/', cell_type+'_'+mission_details['mission_name']+'_panel_current_data.csv')
    df.to_csv(folder_path)
    plt.figure(figsize = (20,12))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l, lw = 3, marker = '*', color = 'goldenrod', label ='Ns, Np = {}\n Panel Current at {} V = {} A '.format((ns,n_p), mission_details['bus_vlt'], np.round(i_l[-20]*n_p,2)))
    plt.xlabel('Bus voltage', fontsize = 30)
    plt.ylabel('Panel current', fontsize = 30)
    plt.axvline(mission_details['bus_vlt']-5, color = 'black', ls = '--')
    plt.axvline(mission_details['bus_vlt'], color = 'black', ls = '--')
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    plt.legend(fontsize = 25)
    plt.title('Panel current for panel of {} x {} m$^2$ with {} cells\n at design T = {} deg C'.format(mission_details['L'],mission_details['W'], cell_type, mission_details['des_T']), fontsize = 30)
    plt.grid()
    folder_path = os.path.join(cur_path, 'Plots/', cell_type+'_'+mission_details['mission_name']+'_panel_current.png')
    plt.savefig(folder_path)
    return ns, n_p, n_p*i_l


def temp_pan_cur(mission_details, cell_details):
    cur_path = os.getcwd()
    i_l = np.zeros((len(mission_details['T_range']),len(np.arange(0, mission_details['bus_vlt']+20,1))))
    if cell_details['voc']==3451:
        cell_type = '4J_cell'
    else:
        cell_type = '3J_cell'
    voc_t = cell_details['voc']+cell_details['t_voc']*(mission_details['des_T']-28)
    vmp_t = cell_details['vmp']+cell_details['t_vmp']*(mission_details['des_T']-28)
    isc_t = cell_details['isc']+cell_details['t_isc']*(mission_details['des_T']-28)
    imp_t = cell_details['imp']+cell_details['t_imp']*(mission_details['des_T']-28)
    voc_t_eol,vmp_t_eol,isc_t_eol,imp_t_eol = voc_t*mission_details['bol_fac_voc']*mission_details['eol_fac_voc'], vmp_t*mission_details['bol_fac_vmp']*mission_details['eol_fac_vmp'],\
                                            isc_t*mission_details['bol_fac_isc']*mission_details['eol_fac_isc'], imp_t*mission_details['bol_fac_imp']*mission_details['eol_fac_imp']
    print('voc, vmp, isc, imp=',  voc_t_eol,vmp_t_eol,isc_t_eol,imp_t_eol)
    ns = (mission_details['bus_vlt']+mission_details['harn_drop'])/(vmp_t_eol/1000)
    ns = int(np.round(ns,0))
    print('ns = ', ns)
    A = mission_details['L']*mission_details['W']
    A_eff = A*mission_details['packing_eff']
    cell_area = 32.2/10000
    one_p_area = cell_area*ns
    n_p = A_eff/one_p_area
    n_p=np.floor(n_p)
    print('np = ', n_p)
    for i in range(len(mission_details['T_range'])):
        voc_t = cell_details['voc']+cell_details['t_voc']*(mission_details['T_range'][i]-28)
        vmp_t = cell_details['vmp']+cell_details['t_vmp']*(mission_details['T_range'][i]-28)
        isc_t = cell_details['isc']+cell_details['t_isc']*(mission_details['T_range'][i]-28)
        imp_t = cell_details['imp']+cell_details['t_imp']*(mission_details['T_range'][i]-28)
        voc_t_eol,vmp_t_eol,isc_t_eol,imp_t_eol = voc_t*mission_details['bol_fac_voc']*mission_details['eol_fac_voc'], vmp_t*mission_details['bol_fac_vmp']*mission_details['eol_fac_vmp'],\
                                            isc_t*mission_details['bol_fac_isc']*mission_details['eol_fac_isc'], imp_t*mission_details['bol_fac_imp']*mission_details['eol_fac_imp']
        i_sc, i_mp, v_mp, v_oc = isc_t_eol/1000,imp_t_eol/1000, vmp_t_eol/1000, voc_t_eol/1000
        v_l = (np.arange(0, mission_details['bus_vlt']+20,1)+mission_details['harn_drop'])/ns
        c3 = 0.000000001
        m = np.log(np.log((i_sc*(1+c3)-i_mp)/(c3*i_sc))/(np.log((1+c3)/c3)))/np.log(v_mp/v_oc)
        i_l[i] = i_sc*(1-c3*np.exp((np.log(((1+c3)/c3))/v_oc**m) * v_l**m - 1))
        print('Panel Current at max bus voltage = {} at T  = {}'.format( i_l[i, -20]*n_p, mission_details['T_range'][i]))
#         df = pd.DataFrame(columns= ['Bus_vlt'])
#         df['Bus_vlt'] = np.arange(0, bus_vlt+10,1)
#         df['Panel_cur'] = n_p*i_l
#         df.to_csv(cell_type+'_'+str(L)+'_'+str(W)+'_panel_current_data.csv')
    i_l[i_l<0] = 0
    plt.figure(figsize = (20,12))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l[0], lw = 2, marker = '*', label ='Panel Current at 41.5 V and {} deg C= {} A '.format(mission_details['T_range'][0], np.round(i_l[0, -20]*n_p,2)))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l[1], lw = 2, marker = '*', label ='Panel Current at 41.5 V and {} deg C= {} A '.format(mission_details['T_range'][1], np.round(i_l[1, -20]*n_p,2)))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l[2], lw = 2, marker = '*', label ='Panel Current at 41.5 V and {} deg C= {} A '.format(mission_details['T_range'][2], np.round(i_l[2, -20]*n_p,2)))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l[3], lw = 2, marker = '*', label ='Panel Current at 41.5 V and {} deg C= {} A '.format(mission_details['T_range'][3], np.round(i_l[3, -20]*n_p,2)))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l[4], lw = 2, marker = '*', label ='Panel Current at 41.5 V and {} deg C= {} A '.format(mission_details['T_range'][4], np.round(i_l[4, -20]*n_p,2)))
    plt.plot(np.arange(0, mission_details['bus_vlt']+20,1), n_p*i_l[5], lw = 2, marker = '*', label ='Panel Current at 41.5 V and {} deg C= {} A '.format(mission_details['T_range'][5], np.round(i_l[5, -20]*n_p,2)))
    plt.xlabel('Bus voltage', fontsize = 30)
    plt.ylabel('Panel current', fontsize = 30)
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    plt.legend(fontsize = 25)
    plt.axvline(mission_details['bus_vlt']-5, color = 'black', ls = '--')
    plt.axvline(mission_details['bus_vlt'], color = 'black', ls = '--')
    plt.title('Panel current for panel of {} x {} m$^2$ with {} cells at different Ts \n design temperature ={} deg C'.format(mission_details['L'],mission_details['W'], cell_type, mission_details['des_T']), fontsize = 30)
    plt.grid()
    folder_path = os.path.join(cur_path, 'Plots/', cell_type+'_'+mission_details['mission_name']+'_diff_temps_panel_current.png')
    plt.savefig(folder_path)
    return ns, n_p, n_p*i_l