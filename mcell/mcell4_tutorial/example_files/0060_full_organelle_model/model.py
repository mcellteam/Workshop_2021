"""
Prerequisites: This tutorial assumes that MCell4 is installed, 
a system variable MCELL_PATH is set and that python3.9 
executable is available through the system variable PATH.
"""

"""
0060
In this tutorial section, we will continue with the model 
we created in section 0050_counting,
add one more sphere representing another organelle,
and add transporters and two more reactions that transport 
molecules into this new organelle.

In this section, we will build the full organelle model
similar to the CellBlender Organelle example with only one 
difference that we won't be using surface regions to place the 
surface molecules but rather place these molecules uniformly
on the area of the organelles.
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
    

#0000-6)
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00001/Scene',
)


#0030-1)
o1v = m.geometry_utils.create_icosphere(
    name = 'O1V', 
    radius = 0.3, 
    subdivisions = 4
)


#0030-2)
o1v.translate((0, -0.2, 0))


#0040-1)
cyt = m.geometry_utils.create_icosphere(
    name = 'CYT', 
    radius = 0.6, 
    subdivisions = 4
)


"""
0060-1)
We will add a second organelle and move it a bit to the right.
"""
o2v = m.geometry_utils.create_icosphere(
    name = 'O2V', 
    radius = 0.2, 
    subdivisions = 4
)
o2v.translate((0, 0.35, 0))


#0000-7)
model = m.Model()
model.add_viz_output(viz_output)


#0020-2)
model.add_geometry_object(o1v)


#0030-11)
model.add_geometry_object(cyt)


"""
0060-2)
We must add the new organelle to the model.
"""
model.add_geometry_object(o2v)


#0030-6)
#0040-11)
o1v.is_bngl_compartment = True
o1v.surface_compartment_name = 'O1M'

cyt.is_bngl_compartment = True


"""
0060-3)
Now we must link the BNGL compartment names with the new organelle 2
object the same way as we did for other geometry objects.
""" 
o2v.is_bngl_compartment = True
o2v.surface_compartment_name = 'O2M'


"""
0060-4)
We will define new reactions, releases and observables using the 
BioNetGen language. 
Open file 'model.bngl' and follow the tutorial present in this 
directory's file called model.bngl.
"""

#0030-7)
#0040-11)
#0050-3)
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))
model.load_bngl(
    file_name = os.path.join(MODEL_PATH, 'model.bngl'),
    observables_path_or_file = './react_data/seed_00001/'
)    


"""
0060-13)
We are going to increase the number of simulated iterations to 1000.
Also, one can set the total number of iterations to be simulated so 
that MCell reports progress when it runs.
"""
ITERATIONS = 1000
model.config.total_iterations = ITERATIONS 


#0000-8)
model.initialize()


#0010-5)
model.export_viz_data_model()


#0010-6)
"""
0060-14)
Use the variable ITERATIONS as the argument to run_iterations 
instead of the previous constant 100. 
"""
model.run_iterations(ITERATIONS)
model.end_simulation()


"""
0060-15)
That's it, we've build the whole organelle model!
Let's run it now:

> python3.9 model.py
"""

"""
0060-16)

First we will take a look at the model visualization.

> $MCELL_PATH/utils/visualize.sh viz_data/seed_00001/

When you run the animation, you can see that the blue 
molecules ('c') are being created inside organelle 1
and over time they get transported to the outside.
And around iteration 800 there are already some yellow 
molecules inside the smaller organelle 2, those
the molecules 'd' created when 'c' is transported 
with the transporter 't2'.   

Let's check the plots now:

> python3.9 $MCELL_PATH/utils/plot_single_run.py react_data/seed_00001/

You can see there how the number of specific molecules evolves over 
time, for instance, you can zoom on to the lower counts 
(using the Zoom to rectangle button) and see how the molecules 'd'
are being slowly created.


Congratulations, you just created a complete organelle model! 

In this section, we did not introduce any new features, but 
used things that we already did in the previous sections such 
as a creation of a geometry object, definition of compartments, 
adding new reaction rule and new observables. 

The tutorial is almost finished, one more thing we will do
in the next section is that we are going to explore some 
performance-related options to make the simulation run faster.    
"""    
