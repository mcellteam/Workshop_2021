#!/usr/bin/env python3

#  description: Simple model of transport involving two cell organelles. 
#               Loads information from file bionetgen/organelle_transport.bngl
#               and defines custom geometry for compartments.

import sys
import os
import math

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

# parameter processing
if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])
else:
    SEED = 1

bngl_file = os.path.join('..', 'bionetgen', 'pybionetgen', 'organelle_transport.bngl')

ITERATIONS = 10000
TIME_STEP = 1e-6 

# load parameters from BNGL file
params = m.bngl_utils.load_bngl_parameters(bngl_file)
if 'vol_CYT' not in params or \
    'vol_O1V' not in params or \
    'vol_O2V' not in params:
    sys.exit("Missing expected volume parameters in " + bngl_file + ".")


# auxiliary function to compute radiuses of cell and organelles
def get_radius(volume):
    return math.pow(3*volume/(4*math.pi), 1/3)


# create the main model object
model = m.Model()

# define model geometry, use names that correspond to compartment names in the BNGL file
# Cell compartment 
CYT = m.geometry_utils.create_icosphere(
    name = 'CYT', 
    radius = get_radius(params['vol_CYT'] + params['vol_O1V'] + params['vol_O2V']), 
    subdivisions = 4
)
CYT.is_bngl_compartment = True

# Organelle 1 compartment 
radius_O1V = get_radius(params['vol_O1V'])
O1V = m.geometry_utils.create_icosphere(
    name = 'O1V', 
    radius = radius_O1V, 
    subdivisions = 4
)
O1V.translate((0, -radius_O1V + 0.1, 0)) # move from center to the left
O1V.is_bngl_compartment = True
O1V.surface_compartment_name = 'O1M'

# Organelle 2 compartment 
radius_O2V = get_radius(params['vol_O2V'])
O2V = m.geometry_utils.create_icosphere(
    name = 'O2V', 
    radius = radius_O2V,
    subdivisions = 4
)
O2V.translate((0, radius_O2V + 0.15, 0)) # move from center to the right
O2V.is_bngl_compartment = True
O2V.surface_compartment_name = 'O2M'


# add objects to our model
model.add_geometry_object(CYT)
model.add_geometry_object(O1V)
model.add_geometry_object(O2V)


# visualization output for CellBlender
viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 100
)
model.add_viz_output(viz_output)


# load bngl file - BNGL compartments et automatically associated with objects 
# that we defined above
model.load_bngl(bngl_file, './react_data/seed_' + str(SEED).zfill(5) + '/')
 

# ---- configuration ----
# use BNGL units for bimolecular reaction rates
model.config.use_bng_units = True

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS 

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.1 


model.initialize()

# export data model for visualization with CellBlender
model.export_data_model()

model.run_iterations(ITERATIONS)
model.end_simulation()


"""
To visualize the model, run:
> $MCELL_PATH/utils/visualize.sh viz_data/seed_00001/
"""


