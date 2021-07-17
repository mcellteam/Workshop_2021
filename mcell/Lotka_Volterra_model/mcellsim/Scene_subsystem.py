# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from Scene_parameters import *

# ---- subsystem ----

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules(os.path.join(MODEL_PATH, 'Scene_model.bngl'), shared.parameter_overrides)

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    prey = subsystem.find_elementary_molecule_type('prey')
    assert prey, "Elementary molecule type 'prey' was not found"
    prey.diffusion_constant_3d = 6e-8

    predator = subsystem.find_elementary_molecule_type('predator')
    assert predator, "Elementary molecule type 'predator' was not found"
    predator.diffusion_constant_3d = 6e-8

set_bngl_molecule_types_info(subsystem)
