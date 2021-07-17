import os,sys
import subprocess as sp
import bionetgen
import numpy as np
import matplotlib.pyplot as plt

'''This script runs mcell & bionetgen for the same system & plot the results together
GCG
07.14.21
'''

python_path ='/Applications/Blender-2.93-CellBlender/blender.app/Contents/Resources/2.93/python/bin/python3.9'
run_file = 'Scene_model.py'
tdir = './mcellsim/'
#run mcell
Proc = sp.call([python_path, run_file],cwd = tdir)
if Proc != 0:
 print('MCell did not run')
else:
 print('MCell sim done')

# for Windows:
# replace C:\\cmw2021\\ with the actual path where you unpacked CellBlender
# python_path = 'C:\\cmw2021\\Blender-2.93-CellBlender\\2.93\\python\\bin\\python3.9.exe'

#directories for bionetgen files
dir =  'Scene_model.bngl'
outdir = './output_folder/'
tdir = './bngl/'
# #run bionetgen
Proc = sp.call(['bionetgen','run','-i',dir,'-o',outdir],cwd = tdir)
if Proc != 0:
    print('BIONETGEN did not run')
else:
    print('BIONETGEN run')

## for Windows:
#exe_ext = ''
#if os.name == 'nt':
#    exe_ext = '.exe'
#Proc = sp.call(['bionetgen' + exe_ext,'run','-i',dir,'-o',outdir],cwd = tdir)

#Load mcell output
mcell_pre = np.genfromtxt('./mcellsim/react_data/seed_00001/predator_World.dat',
                      dtype=float,
                      delimiter=' ')
#
mcell_prey = np.genfromtxt('./mcellsim/react_data/seed_00001/prey_World.dat',
                      dtype=float,
                      delimiter=' ')
#
# #Load bionetgen output
rb_d = np.genfromtxt('./bngl/output_folder/Scene_model.gdat',
                      skip_header=1,
                       dtype=float,
                       delimiter=' ')
rb_d_ode = np.genfromtxt('./bngl/output_folder/Scene_model.gdat',
                      skip_header=1,
                       dtype=float,
                       delimiter=' ')
#
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.9, left = 0.15, bottom =0.15, top = 0.95)
#
ax.plot(rb_d_ode[:,0],rb_d_ode[:,4],'g',linestyle = 'dashdot',label = 'BioNetGen ODE predator')
ax.plot(rb_d_ode[:,0],rb_d_ode[:,2],'g',label = 'BioNetGen ODE prey')
#
ax.plot(mcell_pre[:,0],mcell_pre[:,1],'b',linestyle = '--',label = 'MCell predator')
ax.plot(mcell_prey[:,0],mcell_prey[:,1],'b',label = 'MCell prey')
#
plt.legend(loc='upper left')
plt.ylim(0,8000)
plt.xlim(0,3.5e-4)
#
plt.xlabel('Time (sec)')
plt.ylabel('# Preys or predators')
# #plt.savefig('prey_pred_set3.png')
plt.show()
