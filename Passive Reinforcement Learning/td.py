'''
Imports
'''
from grid import *
import cPickle
from os import listdir
from os.path import isfile, join
'''
'''

S = {}			# Frequency of state
U = {}			# Utilities of states
gamma = 0.9


# Learning rate alpha. Have defined it as the inverse of the number of times a state has been visited
def alpha_m(m):
	return float(1)/m


# Method that implements temporal difference learning
def td():

	# Create the grid
	grid = create_grid()

	files = [f for f in listdir("./trajectories") if isfile(join("./trajectories", f))]

	# Open all trajectories
	for f in files:

		# Load the trajectories via cPickle
		trajectories = cPickle.load(open("./trajectories/" + f, "rb"))

		for trajectory in trajectories:

			# If initial state was observed or not
			if trajectory[0] not in U:
				U[trajectory[0]] = 0

			# Observe the transitions in each trajectory
			for i in xrange(0, len(trajectory) - 1):

				# Source and destination
				s = trajectory[i]
				s_prime = trajectory[i+1]

				# Frequency of visiting a state. Used for the alpha parameter
				if s not in S:
					S[s] = 1
				else:
					S[s] += 1

				# If destination is seen first time, then its utility is initialized to its reward
				if s_prime not in U:
					U[s_prime] = grid.rewards[s_prime]


				# Update equation based on the transition
				val = U[s] + (alpha_m(S[s]) * (grid.rewards[s] + (gamma * U[s_prime]) - U[s]))
				U[s] = val


	# Print out the final utilities
	print 'Estimated utility for each cell is: '
	for state in grid.states:
		if state not in grid.terminals and state in U:
			print state, U[state]



if __name__ == '__main__':
	td()
