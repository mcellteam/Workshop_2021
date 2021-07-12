"""
Prerequisites: This tutorial assumes that MCell4 is installed, 
a system variable MCELL_PATH is set and that python3.9 
executable is available through the system variable PATH.
"""

"""
0000
This is the first tutorial where we will build a model 
where a single molecule is released and diffused for 
10 iterations.
"""

"""
0000-1) 
We will first import the sys and os Python modules.
"""
import sys
import os


"""
0000-2)
MCell Python module is distributed in the CellBlender package.
There are also other tools present, so to make them easily accessible,
a system variable MCELL_PATH needs to be set after installation 
(see MCell installation documentation).
 
On MacOS, its location is always the same:
/Applications/Blender-2.93-CellBlender/blender.app/Contents/Resources/2.93/scripts/addons/cellblender/extensions/mcell/

On Linux/Windows its value depends on the installation directory:
<blender_dir>/2.93/scripts/addons/cellblender/extensions/mcell
 
The code below reads the system variable MCELL_PATH and appends 
it to sys.path, which is a list of directories where
Python searches for modules. 
""" 
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    sys.path.append(lib_path)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)
    
    
"""
0000-3)
Now we can import the MCell4 Python module.
By convention, the module will be imported under name 'm'. 
"""    
import mcell as m
    
    
"""
0000-4)
In this first tutorial, we will release a single volume molecule 
and let it freely diffuse in space.
We need to define the molecule's species with its diffusion
constant 1e-6 cm^2/s.  
"""
species_a = m.Species(
    name = 'a', 
    diffusion_constant_3d = 1e-6
)


"""
0000-5)
Now we define a release site telling to release 1 molecule a
at x,y,z location 0, 0, 0 (units are in micrometers).

Side note: The reason why the argument that sets the species is called 
complex is due to BioNetGen terminology where a complex 
is a fully-specified type of a molecule that can represent a protein complex.
"""
release_site_a = m.ReleaseSite(
    name = 'rel_a', 
    complex = species_a, 
    location=(0, 0, 0), 
    number_to_release = 1
)


"""
0000-6)
We could define our model and run the simulation
now, but we would not get any output.
We would like to see where the molecule diffuses and 
for this, we will define a VizOutput object that then tells 
to store the locations of molecules in text files on each 
iteration. The default location for these files is 
under /viz_data/seed_00001/ (where the 1 is the default seed value) 
and a prefix Scene is used, so we will use the same convention here.
"""
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00001/Scene',
)

    
"""
0000-7)
We can build the model now by creating a Model object 
and adding the species, release site, and viz_output to it.
"""
model = m.Model()
model.add_species(species_a)
model.add_release_site(release_site_a)
model.add_viz_output(viz_output)


"""
0000-8)
The model is ready, so we can initialize it and  
run it for 10 iterations. 
The subsequent call to end_simulation stores the 
last outputs, flushes any buffers, and prints 
final simulation statistics.
"""
model.initialize()
model.run_iterations(10)
model.end_simulation()


"""
0000-9)
Open a terminal (command line), change the current directory 
to the directory where this file is stored and run:

> python3.9 model.py

Information on the progress of simulation and
final statistics are printed.
We can now take a look at the visualization output files. 
   
Under directory viz_data/seed_00001/, there are
files Scene.ascii.0000000.dat - Scene.ascii.0000010.dat
that contain the location of the molecule.   

The format of visualization data is:
species_name id x y z nx ny nz
 
Where x,y,z is the location (in um) and nx,ny,nz is the normal vector 
that is always 0,0,0 for volume molecules. 

The first location right after release is in Scene.ascii.0000000.dat:
a 0 0 0 0 0 0 0

And the final location is in Scene.ascii.0000010.dat:
a 0 -0.00204423885 0.0107041633 -0.0267571038 0 0 0
(the actual positions may differ)
"""


"""
0000-10)
We can also use CellBlender to visualize the trajectory. 
To do this:
1) start CellBlender with ./my_blender or blender.exe,
2) open file viz.blend (in the same directory as this script),
3) select panel Visualization Settings,
4) click on Read Viz Data and navigate to directory viz_data/seed_00000/,
5) click on Play Animation button (Triangle aiming to the left) 
   on the middle bottom of the CellBlender window.
   
You should see how the molecule diffuses around during the 
10 iterations.

This concludes the first section of the MCell4 Python tutorial
where we created a model that releases a single molecule and 
simulates its diffusion.
"""    
