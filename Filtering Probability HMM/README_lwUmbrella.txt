/*
*CSci5512 Spring'16 Homework 3
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: Likelihood weighting*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python lwUmbrella.py <numSamples> <numSteps> <file containing evidence values>


SAMPLE INPUT INSTRUCTION
------------------------
python lwUmbrella.py 100 10 u1.txt


SAMPLE RESULT
-------------
Approximate filtering probability is 0.0660539836388 and sample variance is: 0.0032612353809 


PROGRAM DESCRIPTION
-------------------
This is a Python script that performs likelihood weighting sampling method to compute the filtering probability P(R_{numSteps} | u_{1 : numSteps})

All the required variables are generated and put in the order in which they will be sampled from.
For each variable, if it is a non-evidence variable, then it is sampled according to the transition model specified,
else the weight of the sample is multiplied by the probabilty of observing the evidence given the value of its parent (rain variable)

This sample and weight is accumulated for numSamples times. These cumulative weights are normalized to give us an estimate of the probability

The above procedure is repeated 50 times (can be changed in line 136) to then provide a mean and variance of these measures.



