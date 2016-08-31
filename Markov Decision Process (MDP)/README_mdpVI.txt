/*
*CSci5512 Spring'16 Homework 3
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: Value Iteration (MDP)*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python mdpVI.py <reward>


SAMPLE INPUT INSTRUCTION
------------------------
python mdpVI.py -2


SAMPLE RESULT
-------------
1 1 r
1 2 r
1 3 r
1 4 u
2 1 u
2 3 r
3 1 r
3 2 r
3 3 r


PROGRAM DESCRIPTION
-------------------
This is a Python script that implements Value Iteration algorithm for the given Grid MDP. 

The program defined the Grid class and creates an instance of one with appropriate attributes like states, walls, terminals, actions and rewards.
Utility function U is defined as 0 for all states initially, before it is updated using the best action at each state.
This iterative procedure continues until the utility values converge (based on epsilon, delta) values

The policy is then printed out on the console as shown above


