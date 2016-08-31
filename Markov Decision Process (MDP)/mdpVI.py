from itertools import chain
import sys
import operator

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
Function to perform value iteration based on the Grid and terminating epsilon values
Initialize all utility values to zero first
'''
def value_iteration(grid, epsilon):
	
	U = {state : 0 for state in grid.states if ((state not in grid.walls) and (state not in grid.terminals))}
	for terminal in grid.terminals:
		U[terminal] = grid.rewards[terminal]
	
	U1 = U.copy()
	iteration = 1

	while True:
		U = U1.copy()
		delta = 0
		
		for state in grid.states:
			if ((state not in grid.walls) and (state not in grid.terminals)):
				max_r = -1 * float("inf")

				# Find best action for the current state based on current utility values in this iteration
				for action in grid.actions:
				 	possible_next_states = grid.T(state, action)
				 	r = 0
				 	for prob, next_state in possible_next_states:
				 		r = r + prob * U[next_state]
				 	
				 	if (r > max_r):
				 		max_r = r
				 
				# Update the utility of the state based on this best action found
				U1[state] = grid.rewards[state] + grid.gamma * max_r
				
				# If there is significant change in the utility in this iteration compared to previous one				
				if abs(U1[state] - U[state]) > delta:				
					delta = abs(U1[state] - U[state])
					

		# Test for breaking the loop
		test = epsilon * (1 - grid.gamma) / grid.gamma
		if (delta < test):
			break
		iteration = iteration + 1

	return U


'''
Finally based on the utility values obtained aboce, decide the policy based on the action that leads to the state with maximum expected utility
'''
def get_policy(grid, U):
	policy = {state : 'Up' for state in grid.states if ((state not in grid.walls) and (state not in grid.terminals))}
	for state in grid.states:
		if ((state not in grid.walls) and (state not in grid.terminals)):
			max_r = -1 * float("inf")
			best_action = 'Up'
			for action in grid.actions:
				possible_next_states = grid.T(state, action)
				r = 0
				for prob, next_state in possible_next_states:
					r = r + prob * U[next_state]
				if (r > max_r):
					max_r = r
					best_action = action
			policy[state] = best_action
			

	return policy


'''
Print the policy in the required format
'''
def print_policy(pi_star):
	for row in xrange(1,4):
		for column in xrange(1,5):
			if (column, row) in pi_star.keys():
				print "{0} {1} {2}".format(row, column, list(pi_star[(column, row)])[0].lower())



'''
Function that consolidates the value iteration algorithm for this MDP
'''
def mdpVI(reward):
	
	#The grid
	states = []
	for j in xrange(1,4):
		states.append([(i,j) for i in xrange(1,5)])
	
	states = list(chain(*states))
	
	# Walls
	walls = [(2,2)]

	#Terminals
	terminals = [(4,3), (4,2)]

	#Actions
	actions = {'Up' : (0,1), 'Left' : (-1,0), 'Down' : (0,-1), 'Right' : (1,0)}
	
	rewards = {state : reward for state in states}
	rewards[(2,2)] = None
	rewards[(4,3)] = 1
	rewards[(4,2)] = -1

	grid = Grid(states, walls, terminals, actions, rewards)
	epsilon = 0.0001

	U = value_iteration(grid, epsilon)
	#print U
	pi_star = get_policy(grid, U)
	
	print_policy(pi_star)
    

if __name__ == '__main__':
	mdpVI(float(sys.argv[1]))