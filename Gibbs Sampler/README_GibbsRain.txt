/*
*CSci5512 Spring'16 Homework 2
*login: subra174
*date: 04/03/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: GibbsRain*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python GibbsRain.py <number of steps>


SAMPLE INPUT INSTRUCTION
------------------------
python GibbsRain.py 100


SAMPLE RESULT
-------------
P(r|w,s)  =  0.3600 


PROGRAM DESCRIPTION
-------------------
This is a Python script that builds a Gibbs sampler for the Rain network (involving variables Cloudy, Rain, Sprinker and WetGrass).

First up, the Conditional Probability Tables (CPT) of the variables Cloudy and Rain are initialized as dictionaries, using the values from Answer 1.a
Then take samples and compute the required probability according to the following algorithm:

Initialize (Cloudy,Rain) to (True, True)

For i = 1 to numSteps
	
	Sample the variable Cloudy using the CPT for Cloudy
	(If C=True and R=False, then take a random number between 0 and 1. If that is <= the corresponding CPT value for (True, False), then C=True, else False)

	Sample the variable Rain using the CPT for Rain
	(Same as above, but use CPT for R)

	//This is end of one step
	If more than half the total steps are covered and the current sample has Rain = True
		Increment counter

Report P(r|w,s) as the division of counter and (numSteps/2) since we throw one half of the samples



