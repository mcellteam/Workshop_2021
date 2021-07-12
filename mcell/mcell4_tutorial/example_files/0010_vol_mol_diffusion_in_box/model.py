"""
Prerequisites: This tutorial assumes that MCell4 is installed, 
a system variable MCELL_PATH is set and that python3.9 
executable is available through the system variable PATH.
"""

"""
0010
In this tutorial section, we will start from 
0000_vol_mol_diffusion/model.py and add a box that reflects molecules.
We will also export the geometry so the model can be visualized in 
CellBlender directly just using information provided in this 
model file. 

All the explanations from the previous version are removed and 
only their code is being kept for reference. 
The new code blocks and explanations are marked with index 0010-X.  
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


"""
0010-1)
The main difference from our previous tutorial section is 
that we will create a geometry object in the shape of a cube.
Geometry objects are defined using a list of vertices and 
a list of walls.

The easiest way how to create definitions of more complex 
objects is to create a CellBlender model and export it
through Run Simulation -> Export & Run, and then 
use the generated definition in file <project base name>_geometry.py 
located in directory 
<.blend file location>/<project_name>_files/mcell/output_data/.

In this tutorial, we can use this prepared object definition.

The box_vertex_list contains triplets of x, y, z coordinates 
and uses um (micrometer) units.
"""
box_vertex_list = [
    [-0.1, -0.1, -0.1],   # 0
    [-0.1, -0.1, 0.1],    # 1
    [-0.1, 0.1, -0.1],    # 2
    [-0.1, 0.1, 0.1],     # 3
    [0.1, -0.1, -0.1],    # 4
    [0.1, -0.1, 0.1],     # 5
    [0.1, 0.1, -0.1],     # 6
    [0.1, 0.1, 0.1]       # 7
] 


"""
0010-2)
A wall is a triangle in 3D space and it is defined using 
three vertices. 
"""
box_wall_list = [
    # [1, 2, 0] defines a triangle connecting vertices 
    # [-0.1, -0.1, 0.1], [-0.1, 0.1, -0.1], and
    # [-0.1, -0.1, -0.1]
    [1, 2, 0],  
    [3, 6, 2], 
    [7, 4, 6], 
    [5, 0, 4], 
    [6, 0, 2], 
    [3, 5, 7], 
    [1, 3, 2], 
    [3, 7, 6], 
    [7, 5, 4], 
    [5, 1, 0], 
    [6, 4, 0], 
    [3, 1, 5]
] 


"""
0010-3)
We use the previously defined list of vertices and walls 
to create an object of class GeometryObject.
"""
box = m.GeometryObject(
    name = 'box',
    vertex_list = box_vertex_list,
    wall_list = box_wall_list
)

    
#0000-7)
model = m.Model()
model.add_species(species_a)
model.add_release_site(release_site_a)
model.add_viz_output(viz_output)


"""
0010-4)
In addition to the previous components, we also add our box 
to the model.
"""
model.add_geometry_object(box)


#0000-8)
model.initialize()


"""
0010-5)
In the previous tutorial model 0000, there was a prepared 
CellBlender project file viz.blend file used to visualize
the simulation. Since the model including its geometry 
is defined by the Python code, we need a way how to export 
this information so that CellBlender can read and display it.

The method export_viz_data_model when not arguments are given,
it uses output_files_prefix from the first VizOutput object 
present in the model (we have just one), and generates 
a JSON file (Data Model) into the visualization directory.  
"""
model.export_viz_data_model()


"""
0010-6)
Now let's run the simulation for 100 iterations. 
"""
model.run_iterations(100)
model.end_simulation()


#0000-9)
"""
0010-7)
Open a terminal (command line), change the current directory 
to the directory where this file is stored and run:

> python3.9 model.py

Information on the progress of simulation and
final statistics are printed.
We can now take a look at the visualization output files. 
   
Under directory viz_data/seed_00001/, there are
the usual files Scene.ascii.0000000.dat - Scene.ascii.0000100.dat
that contain the location of the molecule.   

Additionally, there is also Scene.data_model.0000000.json
than contains information about model's geometry.
"""


#0000-10)
"""
0010-8)
We can also use CellBlender to visualize the trajectory 
but we will use the data model fiel instead of the viz.blend file in 
the previous tutorial section.
  
To do this:
1) start CellBlender with ./my_blender or blender.exe,
2) through File -> Import -> CellBlender Model and Geometry (JSON)
   import file viz_data/seed_00001/Scene.data_model.0000000.json
3) select panel Visualization Settings,
4) select checkbox Manually Select Viz Directory
5) click on Read Viz Data and navigate to directory viz_data/seed_00000/,
6) click on Play Animation button (Triangle aiming to the left) 
   on the middle bottom of the CellBlender window.
   
You should see how the molecule diffuses around during the 
100 iterations and how it reflects from the walls of our box.
"""


"""
0010-9)
The process above that uses the CellBlender's graphical interface 
may be too time consuming, especially when debugging the model. 
There is also a way to run it from the terminal by executing:

$MCELL_PATH/utils/visualize.sh viz_data/seed_00001/

This way, one can visualize the model simply by runing a single 
command. 

This concludes the second section of the MCell4 Python tutorial
where we added a box to our existing model, exported the 
geometry in the format of a data model and visualized it in 
CellBlender.  
"""    
