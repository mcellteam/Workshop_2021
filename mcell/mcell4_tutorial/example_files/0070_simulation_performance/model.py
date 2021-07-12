"""
Prerequisites: This tutorial assumes that MCell4 is installed, 
a system variable MCELL_PATH is set and that python3.9 
executable is available through the system variable PATH.
"""

"""
0070
In this tutorial section, we will continue with the model 
we created in section 0060_full_organelle_model. 

We are going to take a look at ways how to increase performance. 

To get a better idea how each change impacts performance, 
run the model after each modification and note down the
Simulation CPU time printed after the simulation is finished.
Example:

> python3.9 model.py

...
Simulation CPU time = 8.60072(user)...
...

The starting simulation time is 8.6 seconds (on a particular machine). 
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
"""
0070-1)
Visualization output may have the highest impact
on performance. 

These are several options on how to lower this impact:
- simply disable it, i.e., remove this line in the code 
  below:
    # model.add_viz_output(viz_output)
  
  VizOuput.output_file_prefix is used in export_viz_data_model 
  to provide location, so we can disable it as well 
  (or provide a output file name)
  
    # model.export_viz_data_model()
  
  Of course, you won't be able to visualize the locations of 
  molecules in CellBlender afterwards.  

  (Simulation CPU time = 5.2)

- we may set the interval to 100 iterations with: 
  
    every_n_timesteps = 100
  
  This is the variant that is used here so that the model can be 
  automatically tested.
  Note: changing the sampling interval (here or later in 
  counts/observables later may change the simulation results 
  because a sampling event may create a simulation barrier.
  The results will be still correct but may represent a different 
  trajectory because an internal random number generator is called 
  lower or higher number of times.     
  
  We are going to use this variant because it is the easiest to test
  automatically.
  (Simulation CPU time = 5.3)
  
- or set output to a more compact binary format instead of the ASCII
  format:
    
    mode = VizMode.CELLBLENDER
  
  This can be combined with the every_n_timesteps settings.
  
  (Simulation CPU time = 5.5)
""" 
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00001/Scene',
    every_n_timesteps = 100
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


#0060-1)
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


#0060-2)
model.add_geometry_object(o2v)


#0030-6)
#0040-11)
o1v.is_bngl_compartment = True
o1v.surface_compartment_name = 'O1M'

cyt.is_bngl_compartment = True


#0060-3)
o2v.is_bngl_compartment = True
o2v.surface_compartment_name = 'O2M'

#0030-7)
#0040-11)
#0050-3)
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))
model.load_bngl(
    file_name = os.path.join(MODEL_PATH, 'model.bngl'),
    observables_path_or_file = './react_data/seed_00001/'
)    


"""
0070-2)
Sampling interval of observables can be lowered 
in a similar way as the viz output interval.
Since we are loading the observables from a BNGL 
file, we must access the Count objects created for 
each observable (they are present in an array model.counts).
We are going to change the interval to 100 iterations
(time steps).

To see the impact, run simulation and open for instance 
react_data/seed_00001/a.dat:

0 1000
0.0001 983
0.0002 928
...

The count of 'a' is stored every 100 us instead of every 1us.  

The impact on performance here is low, but it may be useful for 
more complex models, especially when they run for a long time and 
the observables data would take up too much of hard drive space.

(Simulation CPU time = 5.2)
"""  
for count in model.counts:
    count.every_n_timesteps = 100



#0060-13)
ITERATIONS = 1000
model.config.total_iterations = ITERATIONS 


"""
0070-4)
An important setting is subpartition_dimension.

The whole simulation happens in a cube called partition.
No molecule can escape this partition otherwise the 
simulation terminates with an error. 
This cannot happen in our this because all molecules are 
enclosed inside the geometry object Cell. 


For the purpose of collision detection, the partition 
is subdivided into smaller cubes called subpartitions 
(also sometimes called subvolumes).

The default size is usually not the best one and 
finding a good size requires experimentation. 
There is also a lower limit defined by 3d reaction radius,
but MCell will report an error if you set the subpartition
dimension lower than what is allowed. 

Back to the whole partition size, the default value 
is 10 and we don't need such a large one.
With small subpartitions, memory requirements might be high
so it is a good idea to set the partition_dimension such 
that all the objects fit in. We will use 1.4 um here
because the largest object is the sphere Cell with radius 
0.6 um.

(Simulation CPU time = 0.9)
"""
model.config.partition_dimension = 1.4 # um
model.config.subpartition_dimension = 0.07


"""
0070-5)
One can also change the time step (or space step for each molecule).
This may cause imprecisions in simulation, so a validation is needed. 
Also, reaction probabilities are computed from the molecule's 
time step and may overflow 1 meaning that some reactions are missed. 
This will for sure lead to simulation errors.

You can try to set a custom time step for molecule 'a' by finding the 
elementary molecule type definition loaded from BNGL and setting it:

em_a = model.find_elementary_molecule_type('a')
em_a.custom_time_step = 2e-6 # in us

A warning will be printed:

Warning: total probability of reaction is > 1 (1.24871), for reactant(s) 
t1@Organelle_1_surface (4) + a@Cell (3).

Also a file reports/warnings_report_00001.txt will be created that contains
more details.

In this model, it is safe to change the time step of the surface 
molecules 't1' and 't2'. 

The impact on performance here is low, but in some cases 
the performance difference may be substantial (but again, be 
aware that this may increase the simulation error).

Setting custom time step has impact only if the sampling frequency
of viz outputs or counts is higher. 

(Simulation CPU time = 0.8)
"""
em_t1 = model.find_elementary_molecule_type('t1')
em_t1.custom_time_step = 10e-6 # us 

em_t2 = model.find_elementary_molecule_type('t2')
em_t2.custom_time_step = 10e-6 


#0000-8)
"""
0070-6)
All the changes we did above must be done before 
model initialization because in initialization
all the input data are read and used to create the 
internal MCell4 simulation model. 
""" 
model.initialize()


#0010-5)
model.export_viz_data_model()


#0010-6)
#0060-14)
model.run_iterations(ITERATIONS)
model.end_simulation()


"""
0070-7)
We went through several options that influence simulation 
performance and made the model run about 10x faster!
Of course, we lowered the sampling frequency substantially, 
but we can still see the visualization and    

Let's run the model again:

> python3.9 model.py

Take a look at the model visualization:

> $MCELL_PATH/utils/visualize.sh viz_data/seed_00001/

And check the plots:

> python3.9 $MCELL_PATH/utils/plot_single_run.py react_data/seed_00001/


Congratulations, you just finished the MCell4 Python API 
Organelle tutorial!

"""
