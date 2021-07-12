"""
Prerequisites: This tutorial assumes that MCell4 is installed, 
a system variable MCELL_PATH is set and that python version 3.9 is used.
"""

"""
0020
In this tutorial section, we will continue with the model 
we created in section 0010_vol_mol_diffusion_in_box
and replace it with mesh a generated using a utility method 
m.geometry_utils.create_icosphere().  
"""

#0000-1) 
import sys
import os


#0000-2)
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    sys.path.append(lib_path)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)
    
    
#0000-3)
import mcell as m
    
    
#0000-4)
species_a = m.Species(
    name = 'a', 
    diffusion_constant_3d = 1e-6
)


#0000-5)
release_site_a = m.ReleaseSite(
    name = 'rel_a', 
    complex = species_a, 
    location=(0, 0, 0), 
    number_to_release = 1
)


#0000-6)
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00001/Scene',
)


#0010-1)
"""
0020-1)
In the previous section we created a simple box inside the 
simulation. Simple primitives (cube and icosphere) can
be also created using methods provided in a submodule     
geometry_utils.
There are two commonly used types of spheres in computer 
graphics: UV spheres and icospheres. The reason why we are 
using icospheres here is that all of their triangles have
the same shape and area as opposed to tringles of an UV sphere.   
  
We will remove the previous definitions of box_vertex_list,
box_wall_list, and box. 
Then, we will create the icosphere with a single function call.

To get closer to our final organelle model, we will call our 
icosphere 'O1V' (organelle 1 volume), its radius will be 0.3 um and 
the subdivisions parameter defines smoothness of the resulting 
object.
"""
o1v = m.geometry_utils.create_icosphere(
    name = 'O1V', 
    radius = 0.3, 
    subdivisions = 4
)


"""
0020-2)
We can also move our icosphere a bit (0.2 um) to the left.
The reason why we are doing this is that we will be adding 
other objects later. 
"""
o1v.translate((0, -0.2, 0))

#0000-7)
model = m.Model()
model.add_species(species_a)
model.add_release_site(release_site_a)
model.add_viz_output(viz_output)


#0010-4)
"""
0020-2)
"""
model.add_geometry_object(o1v)


#0000-8)
model.initialize()


#0010-5)
model.export_viz_data_model()


#0010-6)
model.run_iterations(100)
model.end_simulation()


#0000-9)
#0010-7)
"""
0020-3)
Run the model:

> python3.9 model.py
"""

"""
0020-4)
And visualize it (we still have just one molecule there):

$MCELL_PATH/utils/visualize.sh viz_data/seed_00001/

This was a short section where we just replaced a box with 
an icosphere, moved it a bit and then visualized 
the model in CellBlender.  
"""    
