#!/usr/bin/env python
# -*-coding: utf-8 -*-

#post_processing_script.py
#Osman Mamun
#DATE CREATED: 10-22-2018

import numpy as np
import os

dirs = next(os.walk('.'))[1]

for di in dirs:
    ads = di.split('_')[-1]
    try:
        data = np.load(di + '/{}_rsdata.npy'.format(ads))[()]
    except FileNotFoundError:
        continue
    MAE_train = np.array([data[k]['MAE_train'] for k in data])
    MAE_test = np.array([data[k]['MAE_test'] for k in data])
    with open(di + '/out.txt', 'w') as f:
        f.write('MAE_train: {}\n'.format(MAE_train))
        f.write('MAE_train mean: {}\n'.format(MAE_train.mean()))
        f.write('MAE_train std: {}\n'.format(MAE_train.std()))
        f.write('MAE_test: {}\n'.format(MAE_test))
        f.write('MAE_test mean: {}\n'.format(MAE_test.mean()))
        f.write('MAE_test std: {}\n'.format(MAE_test.std()))



