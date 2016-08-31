import sys
import random

# The dictionary specifying the transition model, i.e from R_{t-1} to R_{t}
transition_model = {'T':0.7, 'F':0.3}

# The dictionary specifying P(u | R). The tuple order is R_t and u_t
sensor_model = {('T', 'T') : 0.9, 
 				('T', 'F') : 0.1,
 				('F', 'T') : 0.2,
 				('F', 'F') : 0.8}

# Denotes prior probability of network or R_0
prior_probability = 0.5

'''
Function to generate the required variables in the network, based on numSteps
And also to generate the order in which the variables will be sampled
'''
def generate_vars(numSteps):
	rains = ['r' + str(i) for i in xrange(1, numSteps+1)]
	X = rains[-1];
	umbrellas = ['u' + str(i) for i in xrange(1, numSteps+1)]
		
	order = []
	j = 0
	for i in xrange(0,numSteps):
		order.append(rains[i])
		order.append(umbrellas[i])
	order.insert(0, 'r0')
	
	return order, umbrellas, X


'''
Function to read the evidence values from the file provided
'''
def read_values(E, file_evidence):
	with open(file_evidence, 'r') as f:
		for line in f:
			e = line

	e = list("".join(e.split()))
	
	evidence_vars = {}
	
	for e_vars,u_values in zip(E, e):
		evidence_vars[e_vars] = u_values

	return evidence_vars


'''
Function to get the initial sample from the prior probability
'''
def initial_sample(numSamples):
	S = []
	for i in xrange(1, numSamples+1):
		rand = random.uniform(0,1)
		if (rand <= prior_probability):
			S.append('T')
		else:
			S.append('F')
	return S


'''
Function to sample the points for the next time step (1st step of Particle Filtering)
'''
def sample_transition(S):
	S1 = []
	for sample in S:
		rand = random.uniform(0,1)
		if (rand <= transition_model[sample]):
			S1.append('T')
		else:
			S1.append('F')
	return S1


'''
Function to perform weighted sample with replacement based on the particles and their weights (3rd step of Particle Filtering)
'''
def resample(numSamples, W):
	S2 = []
	total = sum(w for sample,w in W)
	
	for i in xrange(1, numSamples + 1):
		rand = random.uniform(0, total)
		cum = 0
		for sample, w in W:
			if (cum + w >= rand):
				S2.append(sample)
				break
			cum += w

	return S2		


'''
Function that performs particle filtering and its constituting steps together
'''
def pfUmbrella(numSamples, numSteps, file_evidence):
	
	order, E, X = generate_vars(numSteps)
	evidence_vars = read_values(E, file_evidence)

	# initial sample from prior
	S = initial_sample(numSamples)
	

	for i in xrange(1, numSteps+1):
		# sample from transition
		S1 = sample_transition(S)
		
		#Weigh the observations with probability of evidence
		W = [(rain, sensor_model[(rain, evidence_vars['u' + str(i)])]) for rain in S1]
		
		#Resample
		S = resample(numSamples, W)
		
	# Return the probability of R_{numSteps} = True
	return float(S.count('T')) / numSamples
	


if __name__ == '__main__':

	# Command line arguments
	numSamples = int(sys.argv[1])
	numSteps = int(sys.argv[2])
	file_evidence = sys.argv[3]
	
	pfProb = []

	# Repeat particle filtering 100 times and take a mean and variance measures

	for i in xrange(0,50):
		pfProb.append(pfUmbrella(numSamples, numSteps, file_evidence))

	#Calculate mean and variance
	sum_sample = sum(pfProb)
	mean = float(sum_sample) / len(pfProb)
	variance = sum((mean - i)**2 for i in pfProb) / len(pfProb)

	# Output the result
	print 'Approximate filtering probability is {0} and sample variance is: {1}'.format(mean, variance)
