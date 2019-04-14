#!/home/vossj/suncat/bin/python
#SBATCH -p iric,owners,normal 
#SBATCH --job-name=Co2Mn2_bulk
#SBATCH --output=Co2Mn2_bulk.out
#SBATCH --error=Co2Mn2_bulk.err
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=$USER@stanford.edu
#SBATCH --ntasks-per-node=16

import numpy as np    
import matplotlib
matplotlib.use('Agg') 
from ase.utils.eos import * 
from ase.units import kJ
from ase.lattice import bulk
from ase import *
from espresso import espresso
from ase.db import connect
from sympy import Symbol, nsolve
import sympy
import mpmath
import matplotlib.pyplot as plt
from scipy.optimize import *



name =  'Co2Mn2'

a0 = 3.59297493575    
c0 = 3.6429   
crystal = 'fcc'
lat0 = [a0, c0]
pw=500.
dw=5000.
xc='BEEF-vdW'
kpts=(9,9,9)
code='Qunatum-Espresso'
 
print '\n'
print 'Minimization specification:'
print 'Minimization method used: '
print 'Python scipy optimize fmin'
print 'Minimization algorithm used:'
print 'Nelder-Mead simplex algorithm'
print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
print '                      Minimization Data                     '
print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
print 'Lattice constant a      Lattice constant c       Energy [eV]'
print '------------------------------------------------------------'

iter_num = 0

def calc_energy(lat):
    global iter_num
    iter_num += 1
    atoms=Atoms(name,scaled_positions=[(0,0,0),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5)],cell=[lat[0],lat[0],lat[1]],pbc=True)
    atoms.set_pbc((1,1,1)) 
    for atom in atoms: 
        atom.magmom=2                 
    calc = espresso(pw=pw, 
                dw=dw,    
                xc=xc,    
                kpts=kpts,
                nbands=-10,
                sigma=0.15,
                spinpol=True,
                mode='scf',
                convergence= {'energy':1e-4*13.6,    
                              'mixing':0.1,
                              'nmix':10,
                              'mix':4,
                              'maxsteps':1000,
                              'diag':'david'
                              }, 
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',
                output = {'avoidio':True,'removewf':True,'wf_collect':False},
                outdir='calcdir-'+ str(iter_num)) 

    atoms.set_calculator(calc)          
    energy = atoms.get_potential_energy()  
    print '%18f %23f %18f'%(lat[0],lat[1],energy)
    return energy

lat = fmin(calc_energy, lat0, ftol = 1e-3)


print 'Lattice constant a: ', lat[0], 'Angstrom'
print 'Lattice constant c: ', lat[1], 'Angstrom'
