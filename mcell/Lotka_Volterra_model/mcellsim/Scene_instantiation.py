# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from Scene_parameters import *
from Scene_subsystem import *
from Scene_geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# ---- instantiation ----

# ---- release sites ----

# ---- surface classes assignment ----

# ---- compartments assignment ----
release_prey_1 = m.ReleaseSite(
     name = 'release_prey_1',
     complex = m.Complex('prey'),
     location=(-0.2, 0.2, 0),
     number_to_release = 100
 )
release_prey_2 = m.ReleaseSite(
     name = 'release_prey_2',
     complex = m.Complex('prey'),
     location=(0, 0.2, 0),
     number_to_release = 100
 )
release_prey_3 = m.ReleaseSite(
     name = 'release_prey_3',
     complex = m.Complex('prey'),
     location=(0.2, 0.2, 0),
     number_to_release = 100
 )

release_prey_4 = m.ReleaseSite(
     name = 'release_prey_4',
     complex = m.Complex('prey'),
     location=(-0.2, 0, 0),
     number_to_release = 100
 )
release_prey_5 = m.ReleaseSite(
     name = 'release_prey_5',
     complex = m.Complex('prey'),
     location=(0, 0, 0),
     number_to_release = 200
 )
release_prey_6 = m.ReleaseSite(
     name = 'release_prey_6',
     complex = m.Complex('prey'),
     location=(0.2, 0, 0),
     number_to_release = 100
 )
release_prey_7 = m.ReleaseSite(
     name = 'release_prey_7',
     complex = m.Complex('prey'),
     location=(-0.2, -0.2, 0),
     number_to_release = 100
 )
release_prey_8 = m.ReleaseSite(
    name = 'release_prey_8',
    complex = m.Complex('prey'),
    location=(0, -0.2, 0),
    number_to_release = 100
)

release_prey_9 = m.ReleaseSite(
   name = 'release_prey_9',
   complex = m.Complex('prey'),
   location=(0.2, -0.2, 0),
   number_to_release = 100
)
rel_predator = m.ReleaseSite(
    name = 'rel_predator',
    complex = m.Complex('predator'),
    region = Cube,
    number_to_release = 1000
)

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(Cube)
instantiation.add_release_site(release_prey_1)
instantiation.add_release_site(release_prey_2)
instantiation.add_release_site(release_prey_3)
instantiation.add_release_site(release_prey_4)
instantiation.add_release_site(release_prey_5)
instantiation.add_release_site(release_prey_6)
instantiation.add_release_site(release_prey_7)
instantiation.add_release_site(release_prey_8)
instantiation.add_release_site(release_prey_9)
instantiation.add_release_site(rel_predator)
# load seed species information from bngl file
#instantiation.export_viz_data_model()

instantiation.load_bngl_compartments_and_seed_species(os.path.join(MODEL_PATH, 'Scene_model.bngl'), None, shared.parameter_overrides)
