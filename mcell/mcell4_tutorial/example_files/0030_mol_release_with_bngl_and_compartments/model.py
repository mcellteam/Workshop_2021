"""
Prerequisites: This tutorial assumes that MCell4 is installed, 
a system variable MCELL_PATH is set and that python3.9 
executable is available through the system variable PATH.
"""

"""
0030
In this tutorial section, we will continue with the model 
we created in section 0020_vol_mol_diffusion_in_icosphere,
remove previous species definitions and switch to using 
BioNetGen language (BNGL) for definition of species and
molecule releases.
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
    

"""
0030-1)
Remove definitions of objects species_a and release_site_a,
we will replace them with BioNetGen definitions.
"""  

#0000-6)
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00001/Scene',
)


#0020-1)
o1v = m.geometry_utils.create_icosphere(
    name = 'O1V', 
    radius = 0.3, 
    subdivisions = 4
)


#0020-2)
o1v.translate((0, -0.2, 0))


"""
0030-2)
Definition of species and reactions using MCell4 API in Python 
can be little too verbose, especially for complex reaction pathways.
To overcome this, MCell4 supports a commonly used domain-specific 
language called the BioNetGen lanuage (BNGL) that provides 
a concise way how to define such reaction pathways.

Create a file 'model.bngl' and follow the tutorial present in this 
directory's file also called model.bngl.
"""

#0000-7)
model = m.Model()
model.add_viz_output(viz_output)


#0020-2)
model.add_geometry_object(o1v)


"""
0030-7)
By default, the geometry objects are not associated with BNGL compartments.
To make sure that the O1V compartment from our BNGL file is 
linked to the organelle 1 object (with name 'o1v'), set 
the object's attribute is_bngl_compartment to True. 
"""
o1v.is_bngl_compartment = True


"""
0030-8)
We can load the BNGL file now. 

To make sure that we can run our model also from other directories we 
will refer to the 'model.bngl' file with a directory path that uses the location
of this Python file. E.g., if the Python model file model.py is stored in 
/Users/name/model.py (we know this from the special Python variable '__file__'), 
we will load the BNGL file /Users/name/model.bngl.
"""
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))
model.load_bngl(os.path.join(MODEL_PATH, 'model.bngl')) 


#0000-8)
model.initialize()


#0010-5)
model.export_viz_data_model()


#0010-6)
model.run_iterations(100)
model.end_simulation()


"""
0030-9)
Run the model:

> python3.9 model.py
"""

"""
0030-10)
And visualize it:

$MCELL_PATH/utils/visualize.sh viz_data/seed_00001/

Check that the molecules were correctly released in the 
organelle and that they diffuse inside.


In this section, we introduced the BNGL language and 
defined a model with one molecule type and a compartment. 
We also used BNGL to release molecules. 
"""    
