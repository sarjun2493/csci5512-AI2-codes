'''
Imports
cPickle needed to read the .pkl file
numpy needed to solve the system of linear equations
'''
from grid import *
import cPickle
import numpy as np
from os import listdir
from os.path import isfile, join
'''
'''

'''
Important variables go here
Utilities, rewards, frequency of states visited, transition probabilities
'''
U = {}
R = {}
S = {}
P = {}

freq_state_action = {} 				# Variable that tells how many times a (state,action) pair was observed
freq_state_state_action = {}		# Variable that tells how many times state' was the outcome of a (state,action)

gamma = 0.9

'''
'''

# Method that solves the system of linear equations
# Set up the Ax=b format, based on the averaged out rewards and transition probability estimates

def solve_utilities(grid):

	U = {state:0 for state in grid.states}

	A = []
	B = []

	for state in grid.states:
		action = grid.policy[state]
		coeffs = {state : 1}

		rhs = R[state]
		possible_next_states = grid.T(state, action)

		if possible_next_states is None:
			pass

		else:
			possible_next_states = list(set(possible_next_states))
			for possible in possible_next_states:
				tup = tuple((possible, state, action))

				if possible in coeffs:
					if tup in P:
						coeffs[possible] -= gamma * P[tup]

				else:
					if tup in P:
						coeffs[possible] = -1 * gamma * P[tup]

		temp = []
		for state in grid.states:
			if (state in coeffs):
				temp.append(coeffs[state])
			else:
				temp.append(0)

		A.append(temp)
		B.append(rhs)


	# Solve it using numpy.
	A = np.array(A)
	B = np.array(B)

	U = np.linalg.solve(A,B)
	return U

'''
'''

# Method to print out the estimated utilities
def print_utilities(U, grid):
	for u,state in zip(U,grid.states):
		if state not in grid.terminals:
			print state, u

'''
'''

# Main method that implements Adaptive Dynamic Programming
def adp():

	# Create the grid and setup the initial information
	grid = create_grid()

	files = [f for f in listdir("./trajectories") if isfile(join("./trajectories", f))]

	# Open all trajectories
	for f in files:

		# Load the trajectories via cPickle
		trajectories = cPickle.load(open("./trajectories/" + f, "rb"))

		for trajectory in trajectories:

			for i in xrange(0, len(trajectory) - 1):
				point = trajectory[i]

				# Keep track of number of times each state has been visited
				# Cumulate the rewards obtained so that they can be averaged out later
				if point not in R.keys():
					R[point] = grid.rewards[point]
					S[point] = 1
				else:
					R[point] += grid.rewards[point]
					S[point] += 1

				# Increment the counters for state,action and transition frequencies
				if (point, grid.policy[point]) not in freq_state_action.keys():
					freq_state_action[(point, grid.policy[point])] = 1
				else:
					freq_state_action[(point, grid.policy[point])] += 1


				if tuple((trajectory[i+1], point, grid.policy[point])) not in freq_state_state_action.keys():
					freq_state_state_action[tuple((trajectory[i+1], point, grid.policy[point]))] = 1
				else:
					freq_state_state_action[tuple((trajectory[i+1], point, grid.policy[point]))] += 1


			# Handle terminal nodes
			terminal = trajectory[-1]

			if terminal not in R:
				R[terminal] = grid.rewards[terminal]
				S[terminal] = 1
			else:
				R[terminal] += grid.rewards[terminal]
				S[terminal] += 1


	# Average out the rewards seen so far
	for state in S.keys():
		R[state] /= S[state]

    # Estimate of transition probabilities
	for state, action in freq_state_action.keys():
		for result, source, policy in freq_state_state_action.keys():
			if (state,action) == (source,policy):
				P[tuple((result, source, policy))] = float(freq_state_state_action[tuple((result, source, policy))]) / freq_state_action[tuple((state,action))]


	# Solve for the utilities
	U = solve_utilities(grid)

	# Print the utilities
	print_utilities(U, grid)



if __name__=='__main__':
	adp()
