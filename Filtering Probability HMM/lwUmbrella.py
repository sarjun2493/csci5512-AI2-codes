import sys
import random

# The dictionary specifying the transition probability between R_{t-1} and R_{t}
transition_model = {'T':0.7, 'F':0.3}


# The dictionary specifying P(u | R) 
sensor_model = {('T', 'T') : 0.9, 
 				('T', 'F') : 0.1,
 				('F', 'T') : 0.2,
 				('F', 'F') : 0.8}


'''
Function to generate the variables involved in the network based on numSteps
Also define the order of sampling the variables
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
Function to read the evidence variable values from the provided file
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
Function that samples a binary variable based on one of the probability values
'''
def get_sample_binary(prob_true):
	rand = random.uniform(0,1);
	if (rand <= prob_true):
		return 'T'
	return 'F'


'''
Function that returns a sample and it's weight based on the likelihood weighting procedure
Weight is multiplied each time by the probability of observing an evidence variable
Else, non-evidence variables are sampled according to the given distribution
'''
def weighted_sample(order, E, evidence_vars):
	
	w  = 1

	sample = {}

	#Sample R_0 first. Hardcoded prior probability here.
	sample['r0'] = get_sample_binary(0.5);

	last_rain = sample['r0']

	for var in order:
		if var in E:
			# Evidence variable and hence weight needs to be multiplied with its corresponding probability
			w = w * sensor_model[(last_rain, evidence_vars[var])]

		else:
			#Rain variable and needs to be sampled from transition model
			sample[var] = get_sample_binary(transition_model[last_rain])
			last_rain = sample[var]

	return sample[order[-2]], w


'''
Function that consolidates the likelihood weighting procedure
numSamples represents the number of samples taken for the required variable
'''
def lwUmbrella(numSamples, numSteps, file_evidence):
	
	order, E, X = generate_vars(numSteps)
	evidence_vars = read_values(E, file_evidence)
	
	W = {}  #Will have two elements: 'T' and 'F' for the values of R_10

	for j in xrange(1, numSamples + 1):
		x, w = weighted_sample(order, E, evidence_vars)
		if x not in W.keys():
			W[x] = w
		else:
			W[x] = W[x] + w

	
	total = sum(W.values())
	
	# Return the probability value
	return (float(W['T'])/total)
	


if __name__ == '__main__':

	# Command line arguments
	numSamples = int(sys.argv[1])
	numSteps = int(sys.argv[2])
	file_evidence = sys.argv[3]
	
	lwProb = []

	# Repeat the likelihood procedure 50 times to obtain mean and variance
	for i in xrange(0,50):
		lwProb.append(lwUmbrella(numSamples, numSteps, file_evidence))

	#Calculate mean and variance
	sum_sample = sum(lwProb)
	mean = float(sum_sample) / len(lwProb)
	variance = sum((mean - i)**2 for i in lwProb) / len(lwProb)

	print 'Approximate filtering probability is {0} and sample variance is: {1}'.format(mean, variance)
