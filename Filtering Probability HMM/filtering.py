import sys
import random

transition_model = {'T':0.7, 'F':0.3}

#Order is R_t, U_t
sensor_model = {('T', 'T') : 0.9, 
 				('T', 'F') : 0.1,
 				('F', 'T') : 0.2,
 				('F', 'F') : 0.8}

prior_probability = 0.5

filtering_probs = {}


def generate_vars(numSteps):
	rains = ['r' + str(i) for i in xrange(1, numSteps+1)]
	X = rains[-1];
	umbrellas = ['u' + str(i) for i in xrange(1, numSteps+1)]
	return rains, umbrellas

def read_values(E, file_evidence):
	with open(file_evidence, 'r') as f:
		for line in f:
			e = line

	e = list("".join(e.split()))
	
	evidence_vars = {}
	
	for e_vars,u_values in zip(E, e):
		evidence_vars[e_vars] = u_values

	return evidence_vars




def filtering(numSteps, fileEvidence):
	R,U = generate_vars(numSteps)
	u = read_values(U, fileEvidence)

	#calculate P(R1|u1)
	a = sensor_model[('T', u['u1'])] * prior_probability
	b = sensor_model[('F', u['u1'])] * (1 - prior_probability)
	
	filtering_probs[('r1', 'u1')] = float(a) / (a + b)
	
	for i in xrange(2, numSteps + 1):
		a = sensor_model['T', u['u' + str(i)]] * ((transition_model[('T')] * filtering_probs[('r'+str(i-1), 'u'+str(i-1))]) + ((1 - transition_model[('T')]) * (1 - filtering_probs[('r'+str(i-1), 'u'+str(i-1))])))
		b = sensor_model['F', u['u' + str(i)]] * ((transition_model[('F')] * filtering_probs[('r'+str(i-1), 'u'+str(i-1))]) + ((1 - transition_model[('F')]) * (1 - filtering_probs[('r'+str(i-1), 'u'+str(i-1))])))
		test = float(a) / (a + b)		
		print test
		filtering_probs[('r' + str(i), 'u' + str(i))] = test


if __name__=='__main__':
	filtering(int(sys.argv[1]), sys.argv[2])