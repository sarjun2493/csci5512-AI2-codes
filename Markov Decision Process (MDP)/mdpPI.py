from itertools import chain
import sys
import operator
import random
import numpy as np

'''
Class that represents the Grid or the states of the MDP
Attributes include states, walls (unreachable states), terminals, actions, rewards, gamma for discounted rewards, start state
'''
class Grid():
	def __init__(self, states, walls, terminals, actions, rewards, gamma = 0.9, start = (1,1)):
		self.states = states
		self.walls = walls
		self.terminals = terminals
		self.start = start
		self.actions = actions
		self.rewards = rewards
		self.gamma = gamma

		self.left_action = {'Up':'Left', 'Right':'Up', 'Down' : 'Right', 'Left' : 'Down'}
		self.right_action = {'Up':'Right', 'Right':'Down', 'Down' : 'Left', 'Left' : 'Up'}


	'''
	Method that returns the possible next states for an action and current state with their probability values
	'''
	def T(self, state, action):
		if (state in self.terminals):
			return None
		else:
			return [(0.8, self.next_state(state, action)),
				    (0.1, self.next_state(state, self.left_action[action])),
				    (0.1, self.next_state(state, self.right_action[action]))]

	'''
	Method that returns the next state for a particular action
	'''
	def next_state(self, state, action):
		next = tuple(map(operator.add, state, self.actions[action]))
   		if ((next in self.states) and (next not in self.walls)):
	   		return next
   		else:
   			return state

   	def __str__(self):
		return "{0}\n{1}\n{2}\n{3}\n{4}\n".format(self.states, self.terminals, self.start, self.actions, self.rewards, self.gamma)


'''
Function to evaluate a policy based on the grid.
Setup a system of linear equations of the form Ax = b, based on the simplified Bellman equation
'''
def policy_evaluation(pi, U, grid):

	A = []
	B = []
	
	#Build the matrices for Ax = B
	
	for state in grid.states:
		if (state not in grid.walls):
			
			action = pi[state]

			B.append(grid.rewards[state])
						
			coeffs = {state : 1}

			possible_next_configs = grid.T(state, action)

			if possible_next_configs is None:
				# Terminal
				pass
			else:
				for item in grid.T(state, action):
					if (item[1] in coeffs):
						val = coeffs[state]
						val = val - (grid.gamma * item[0])
						coeffs[item[1]] = val
					else:
						coeffs[item[1]] = -grid.gamma * item[0]

			temp = []
			for state in grid.states:
				if (state not in grid.walls):
					if (state in coeffs):
						temp.append(coeffs[state])
					else: 
						temp.append(0)

			A.append(temp)
			
			
	#Solve it using numpy. 
	A = np.array(A)
	B = np.array(B)
	U = np.linalg.solve(A,B)

	return U


'''
Function to calculate the expected utility of a state based on an action and utility function for each state
'''
def expected_utility(state, action, grid, U):
	possible_next_states = grid.T(state, action)
	
	if (possible_next_states is None):
		return 0

	r = 0
	for item in possible_next_states:
		r += item[0] * U[item[1]]
	return r


'''
Function to find the best action from current state in the grid based on utility values
The best action is based on the expected utility values
'''
def find_best_action(state, U, grid):

	best_action = random.choice(grid.actions.keys())
	max_r = -1 * float("inf")
	for action in grid.actions:
		r = expected_utility(state, action, grid, U)
		if (r > max_r):
			max_r = r
			best_action = action

	return best_action, max_r


'''
Function that consolidates all components of policy iteration
Initialize utility of all states to 0
Initialize a random policy for each state
Evaluate the current policy and check if better action can be taken at each state
Repeat this until policy does not change
'''
def policy_iteration(grid):

	U = {state : 0 for state in grid.states if ((state not in grid.walls))}
	
	#random initialization of pi
	actions_list = grid.actions.keys()
	pi = {state : random.choice(actions_list) for state in grid.states if (state not in grid.walls)}

	while True:

		#Evaluate current policy
		U1 = policy_evaluation(pi, U, grid)
		unchanged = True

		U = {}
		i = 0
		for state in grid.states:
			if ((state not in grid.walls)):
				U[state] = U1[i]
				i += 1

		for state in grid.states:
			if (state not in grid.walls):
				best_action, EU = find_best_action(state, U, grid)
				current = expected_utility(state, pi[state], grid, U)
				if (EU > current):
					pi[state] = best_action
					unchanged = False


		if unchanged == True:
			# Print U
			return pi
	

'''
Print the final policy
'''
def print_policy(grid, pi_star):
	for row in xrange(1,4):
		for column in xrange(1,5):
			if ((column, row) in pi_star.keys()) and ((column, row) not in grid.terminals):
				print "{0} {1} {2}".format(row, column, list(pi_star[(column, row)])[0].lower())


def mdpPI(reward):
	
	# The grid
	states = []
	for j in xrange(1,4):
		states.append([(i,j) for i in xrange(1,5)])
	states = list(chain(*states))
	
	walls = [(2,2)]

	# Terminals
	terminals = [(4,3), (4,2)]

	# Actions
	actions = {'Up' : (0,1), 'Left' : (-1,0), 'Down' : (0,-1), 'Right' : (1,0)}
	
	# Rewards
	rewards = {state : reward for state in states}
	rewards[(2,2)] = None
	rewards[(4,3)] = 1
	rewards[(4,2)] = -1

	grid = Grid(states, walls, terminals, actions, rewards)
	
	pi = policy_iteration(grid)
	print_policy(grid, pi)


if __name__ == '__main__':
	mdpPI(float(sys.argv[1]))