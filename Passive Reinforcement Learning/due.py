'''
Imports for the program
'''
from grid import *
import cPickle
from os import listdir
from os.path import isfile, join
'''
'''

# Rewards is the key,value mapping between the state and its utilities
rewards = {}
# Counts is the number of times a state has been visited so far
counts = {}


# Method that computes the utilities of the non-terminal states using direct utility estimation
def due():

	# Create the grid
	grid = create_grid()

	# Open all the files
	files = [f for f in listdir("./trajectories") if isfile(join("./trajectories", f))]

	# Move through all trajectories
	for f in files:
		# Read the trajectories via cPickle file
		trajectories = cPickle.load(open("./trajectories/" + f, "rb"))
		for trajectory in trajectories:

			# Compute reward gained as a result of moving from this current point to the next point
			# Increment counters

			for i in xrange(0, len(trajectory) - 1):
				#estimate value
				est_reward = grid.rewards[trajectory[i]]
				for j in xrange(i+1, len(trajectory)):
					est_reward += grid.rewards[trajectory[j]]

				if (trajectory[i] not in rewards.keys()):
					rewards[trajectory[i]] = est_reward
					counts[trajectory[i]] = 1
				else:
					rewards[trajectory[i]] += est_reward
					counts[trajectory[i]] += 1


    # Average out the utilities based on the number of times the state was visited
	for key in rewards.keys():
		rewards[key] /= counts[key]


	# Print out the expected utilities
	print 'Expected utilities for each state'
	for state in grid.states:
		if state not in grid.terminals:
			print state, rewards[state]


if __name__ == '__main__':
	due()
