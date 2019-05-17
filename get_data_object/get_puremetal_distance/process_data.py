#!/usr/bin/env python
# -*-coding: utf-8 -*-

#SCRIPT: process_data.py
#AUTHOR: Osman Mamun
#DATE CREATED: 02-08-2019

import numpy as np
import re
import os
from cathub.query import get_logfile 
from cathub.query import get_reactions

def get_sym(A):
    ordered_metals = ['Y', 'La', 'Sc', 'Zr', 'Hf', 'Ti', 'Ta', 'Nb', 'V',
                      'Cr', 'Mo', 'W', 'Re', 'Tc', 'Os', 'Ru', 'Ir','Rh',
                      'Ni', 'Co', 'Fe', 'Mn', 'Pt', 'Pd', 'Au', 'Ag', 'Cu',
                      'Zn',  'Cd', 'Hg', 'Al',  'Ga',  'In', 'Tl', 'Pb',
                      'Sn', 'Bi']
    if '3' in A:
        return A, 'L12'
    elif A in ordered_metals:
        return A, 'A1'
    else:
        sym = []
        for i in ordered_metals:
            if i in A:
                sym += [i]

        if not len(sym) == 2:
            A = 'ERROR!!'
        else:
            return '2'.join(sorted(sym)) + '2', 'L10'

def get_info(A, D):
    adsorbate = [k for k in A['sites']][0]
    reactionenergy = A['reactionEnergy']
    symbol, sb_symbol = get_sym(A['surfaceComposition'])
    print(A['reactionSystems'])
    aseid = None
    for item in A['reactionSystems']:
        if item['name'] == D + 'star':
            aseid = item['aseId']
    try:
        site, site_type = list(A['sites'].values())[0].split('|', 1)
    except ValueError:
        return None

    if site not in ['top', 'bridge', 'hollow']:
        print('Site {} not a valid site_type.'.format(site))
        return None 
        

    if sb_symbol == 'A1':
        site_type = site_type.replace('A', symbol)
    elif sb_symbol == 'L12':
        a, b = symbol.split('3')
        site_type = site_type.replace('A', 'aaa').replace('B', 'bbb')
        site_type = site_type.replace('aaa', a).replace('bbb', b)
    else:
        a, b, _ = symbol.split('2')
        if a > b:
            a, b = b, a
        site_type = site_type.replace('A', 'aaa').replace('B', 'bbb')
        site_type = site_type.replace('aaa', a).replace('bbb', b)
    return [adsorbate, symbol, sb_symbol, site, site_type, 
            reactionenergy, aseid]

references = {}
references['C'] = 'CH4+H2'
references['H'] = 'H2'
references['N'] = 'N2'
references['O'] = 'H2O+H2'
references['S'] = 'H2S'
references['CH'] = 'CH4+H2'
references['CH2'] = 'CH4+H2'
references['CH3'] = 'CH4+H2'
references['NH'] = 'N2+H2'
references['SH'] = 'H2S+H2'
references['OH'] = 'H2O+H2'
references['OH2'] = 'H2O'

data = ['H', 'O', 'N', 'S', 'CH', 'CH2', 'CH3', 'OH', 'NH', 'SH']

for datum in data:
    w_data = get_reactions(n_results='all',
                         pubId='MamunHighT2019',
                         reactants=references[datum],
                         products=datum,
                         columns=['surfaceComposition, reactionEnergy',
                             'sites', 'reactants', 'products'],
                         subtables=['reactionSystems'])
    for i, d in enumerate(w_data['reactions']['edges']):
        info = get_info(d['node'], datum)
        if info == None:
            continue
        if not info[2] == 'A1':
            continue
        if info[6] == None:
            continue
        unique_id = '_'.join([info[1], info[3], info[4]])
        fname = '{}/{}'.format(datum, unique_id)
        if not os.path.exists(fname):
            os.makedirs(fname)
        with open(fname + '/inf.txt', 'w') as f:
            f.write('Adsorbate: {}'.format(info[0]))
            f.write('Symbol: {}'.format(info[1]))
            f.write('SB symbol: {}'.format(info[2]))
            f.write('Site: {}'.format(info[3]))
            f.write('Site type: {}'.format(info[4]))
            f.write('Reaction energy: {}'.format(info[5]))
            f.write('ASE ID: {}'.format(info[6]))
        try:
            if not os.path.exists(fname+'/pw.pwo'):
                get_logfile(aseId=info[6], fname=fname + '/pw.pwo')
            else:
                print('This data is already collected!')
        except IndexError:
            with open('debug.txt', 'a+') as ff:
                msg = 'Problem found in the following file:\n'
                msg += 'Adsorbate: {}\nSymbol: {}\nSB symbol: {}\n'
                msg += 'Site: {}\nSite type: {}\nReaction energy: {}\n'
                msg += 'ASE ID: {}\n'
                ff.write(msg.format(*info))
