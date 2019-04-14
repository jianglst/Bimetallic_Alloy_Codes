#!/home/vossj/suncat/bin/python
#SBATCH -p iric,owners,normal 
#SBATCH --job-name=Mo2Pb2_bulk
#SBATCH --output=Mo2Pb2_bulk.out
#SBATCH --error=Mo2Pb2_bulk.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=$USER@stanford.edu
#SBATCH --ntasks-per-node=16

import numpy as np    #vectors, matrices, lin. alg., etc.
import matplotlib
matplotlib.use('Agg') #turn off screen output so we can plot from the cluster
from ase.utils.eos import *  # Equation of state: fit equilibrium latt. const
from ase.units import kJ
from ase.lattice import bulk
from ase import *
from espresso import espresso
from ase.optimize import BFGS
from ase.constraints import StrainFilter
from ase.db import connect

pw=500.
dw=5000.
xc='BEEF-vdW'
kpts=(9,9,9)
code='Qunatum-Espresso'

metal =  'Mo'
metal2 =  'Pb'
a=4.4352083766
c=4.4852083766
crystal = 'fcc'
name=metal+'2'+metal2+'2'
atoms=Atoms(name,scaled_positions=[(0,0,0),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5)],cell=[a,a,c],pbc=True)
atoms.set_pbc((1,1,1)) 

calc = espresso(pw=pw,
                dw=dw,   
                xc=xc,   
                kpts=kpts, 
                nbands=-10, 
                sigma=0.1,
                calcstress=True,
                spinpol=False,
                convergence= {'energy':1e-5,    #convergence parameters
                              'mixing':0.1,
                              'nmix':10,
                              'mix':4,
                              'maxsteps':500,
                              'diag':'david'
                              }, 
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',
                outdir='cell_relax',
                mode='vc-relax',cell_factor=3,
                cell_dynamics='bfgs',
                opt_algorithm='bfgs',
                output = {'avoidio':True,'removewf':True,'wf_collect':False})

atoms.set_calculator(calc) 

print 'Potential_Energy:', atoms.get_potential_energy(), 'eV'
print 'Kinetic_Energy:', atoms.get_kinetic_energy(), 'eV'
print 'Total_Energy:', atoms.get_total_energy(), 'eV'

