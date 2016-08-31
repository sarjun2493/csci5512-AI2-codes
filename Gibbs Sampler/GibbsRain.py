# Module import
import sys
import random

# CPT tables defined as dictionaries. 
# These values were computed in question 1a.

# CPT Table for variable Cloudy
# Order of variables: (C,R)
CPT_C = {(True, True) : 0.44445,
		 (False, True) : 0.55556,
		 (True, False) : 0.04762,
		 (False, False) : 0.95238
		}

# CPT Table for variable Rainy
# Order of variables: R,C
CPT_R = {(True, True) : 0.81481,
		 (False, True) : 0.18512,
		 (True, False) : 0.21569,
		 (False, False) : 0.78431
		}


# The Gibbs Sampler
def GibbsRain(numSteps):

	# Samples are of the form (Cloudy, Rain)
	# Initialize x_0 to (True, True)
	current_sample = [True, True]
	
	#Counter for estimating probability P(r|w,s)
	counter = 0
	
	#Repeat the sampling process for numSteps times
	for t in xrange(1, numSteps + 1):
	
		# One step begins here
		# Update Cloudy variable with probability from the CPT table
		random_number = random.uniform(0,1)
		val = CPT_C[(current_sample[0], current_sample[1])]
		if (random_number <= val):
			current_sample = [current_sample[0], current_sample[1]]
		else:
			current_sample = [not current_sample[0], current_sample[1]]
		

		# Update Rain variable with probability from the CPT table
		random_number = random.uniform(0,1)
		val = CPT_R[(current_sample[1], current_sample[0])]
		if (random_number <= val):
			current_sample = [current_sample[0], current_sample[1]]
		else:
			current_sample = [current_sample[0], not current_sample[1]]
		
		# End of one step
		# current_sample now indicates a sample here

		# Throw away the first half of the samples
		# Use the samples for the counts from the second half
		# The first half is the burn-in time
		if (t > numSteps/2): 
			if (current_sample[1] == True):
				counter = counter + 1
		
	# Printing output to stdout	
	print str(numSteps/2) + " first samples discarded as burn-in"
	print "P(r|w,s)  =  %.4f" % (counter * 2 / float(numSteps))
	#print "P(~r|w,s)  =  %.4f" % (neg_counter * 2 / float(numSteps))


if __name__=='__main__':
	# Number of steps for the sampler is provided as a command line argument
	GibbsRain(int(sys.argv[1]))