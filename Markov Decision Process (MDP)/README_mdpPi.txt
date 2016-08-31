/*
*CSci5512 Spring'16 Homework 3
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: Policy Iteration (MDP)*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python mdpPI.py <reward>


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
This is a Python script that implements Policy Iteration algorithm for the given Grid MDP. 

The program defined the Grid class and creates an instance of one with appropriate attributes like states, walls, terminals, actions and rewards.

Utility function U is defined as 0 for all states initially, and the policy (action) at each state is randomly initialized
The policy is evaluated which translates to setting up system of linear equations in each U, based on simplified Bellman equation for utility.
Based on this solution for U, the expected utility of the best action in each state is compared against the expected utility of the current policy.
If the former is higher, then the policy is updated to reflect this. This entire procedure is repeated till the policy does not change

The policy is then printed out on the console as shown above



NOTE
----
This program requires numpy package to be installed. 
After downloading the source, the command python setup.py install can be executed.
