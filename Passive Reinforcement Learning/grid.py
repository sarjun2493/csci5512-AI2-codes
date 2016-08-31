import operator
from itertools import chain

'''
Class that represents the Grid or the states 
Attributes include states, walls (unreachable states), terminals, actions, rewards, gamma for discounted rewards, start state
'''
class Grid():
	def __init__(self, states, walls, terminals, actions, rewards, policy, gamma = 0.9):
		self.states = states
		self.walls = walls
		self.terminals = terminals
		self.actions = actions
		self.rewards = rewards
		self.policy = policy
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
			# return [(0.8, self.next_state(state, action)),
			# 	    (0.1, self.next_state(state, self.left_action[action])),
			# 	    (0.1, self.next_state(state, self.right_action[action]))]
			return [self.next_state(state, action), self.next_state(state, self.left_action[action]), self.next_state(state, self.right_action[action])]

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
		return "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(self.states, self.terminals, self.actions, self.rewards, self.gamma, self.policy)




def create_grid():
	
	#The grid
	states = []
	for j in xrange(1,4):
		states.append([(i,j) for i in xrange(1,5)])
	
	states = list(chain(*states))
	states.remove((2,2))
	
	# Walls
	walls = [(2,2)]

	#Terminals
	terminals = [(4,3), (4,2)]

	#Actions
	actions = {'Up' : (0,1), 'Left' : (-1,0), 'Down' : (0,-1), 'Right' : (1,0)}

	#Rewards in each state
	rewards = {state : -0.04 for state in states}
	rewards[(2,2)] = None
	rewards[(4,3)] = 1
	rewards[(4,2)] = -1

	#Policy as given in figure 1a.
	policy = {(1,1):'Up', (2,1):'Left', (3,1):'Left', (4,1):'Left',
			  (1,2):'Up', (2,2):None, (3,2):'Up', (4,2):None,
			  (1,3):'Right', (2,3):'Right', (3,3):'Right', (4,3):None}


	return Grid(states, walls, terminals, actions, rewards, policy, gamma = 1)
