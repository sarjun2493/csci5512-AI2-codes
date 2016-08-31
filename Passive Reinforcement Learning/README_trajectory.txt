/*
*CSci5512 Spring'16 Homework 4
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: Generating trajectory*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python trajectory.py <x coordinate of initial point> <y coordinate of initial point> <number of trajectories to generate>


SAMPLE INPUT INSTRUCTION
------------------------
python trajectory.py 1 1 10
python trajectory.py 3 1 10


SAMPLE RESULT
-------------
[(1, 1), (1, 2), (1, 3), (1, 2), (1, 3), (1, 3), (2, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 3), (2, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 3), (1, 2), (1, 2), (1, 3), (2, 3), (2, 3), (3, 3), (3, 2), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 2), (1, 3), (1, 2), (1, 3), (2, 3), (2, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (1, 2), (1, 2), (1, 3), (1, 3), (2, 3), (3, 3), (4, 3)]
[(1, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 3), (4, 3)]
----------------------------------------------------------


PROGRAM DESCRIPTION
-------------------
This script generates trajectories from the initial state in the grid, specified by the x and y coordinate points
It uses the fixed policy at each state to generate the next state using the transition probabilites of moving on the sides.

It writes these trajectories as a list object in .pkl (pickle format), by creating a directory called trajectories.
cPickle library is used for simple dumping and loading of objects direcly in format, to save parsing of items while reading files as plain ASCII text.


You can also execute 
python generate_trajectories.py <numtraj>
After setting numtraj parameter inside the script

This will generate all the required trajectories from all non-terminal states as required for the remaining parts