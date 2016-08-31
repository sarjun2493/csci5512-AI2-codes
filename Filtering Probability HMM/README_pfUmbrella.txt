/*
*CSci5512 Spring'16 Homework 3
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: Particle Filtering*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python pfUmbrella.py <numSamples> <numSteps> <file containing evidence values>


SAMPLE INPUT INSTRUCTION
------------------------
python pfUmbrella.py 100 10 u1.txt


SAMPLE RESULT
-------------
Approximate filtering probability is 0.674427696182 and sample variance is: 0.0181742764105 


PROGRAM DESCRIPTION
-------------------
This is a Python script that performs particle filtering sampling method to compute the filtering probability P(R_{numSteps} | u_{1 : numSteps})

All the required variables are generated and put in the order in which they will be sampled from.
An initial sample is generated using the prior probability of R0. Then the samples for next time step is drawn.
Finally each of these particles are weighed by the probability of observing an evidence variable of that value. These weights on the particles
are used to sample the particles for next time step. 

This sample and weight is accumulated for numSamples times. The counts are normalized to give the required probability

The above procedure is repeated 50 times (can be changed in line 147) to then provide a mean and variance of these measures.