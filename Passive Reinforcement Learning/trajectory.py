'''
Imports for this program
'''
import sys
import random
import cPickle
import os
from grid import *
'''
'''

# Method that generates numTraj trajectories, based on the initial point (x,y) and
# the fixed policy in the grid
def trajectory(x, y, numtraj):

	# Create the grid
	grid = create_grid()

	# Generate the trajectories
	start = tuple((x,y))
	trajectories = []

	# For each trajectory, decide next state by using probabilities of transition based on fixed action
	for i in xrange(1,numtraj+1):
		curr_state = start
		curr_traj = [start]
		while (curr_state not in grid.terminals):

			# Find what the policy says
			action_to_take = grid.policy[curr_state]

			# Toss a coin and decide based on the probabilities of transition
			rand = random.uniform(0,1)

			if (rand <= 0.8):
				pass
			elif (rand <= 0.9):
				action_to_take = grid.left_action[action_to_take]
			else:
				action_to_take = grid.right_action[action_to_take]

			curr_state = grid.next_state(curr_state, action_to_take)
			curr_traj.append(curr_state)

		trajectories.append(curr_traj)


	# Print it out on stdout
	for trajectory in trajectories:
		print trajectory

	# Write all these trajectories onto a file inside a directory called trajectories

	directory = 'trajectories'

	if not os.path.exists(directory):
		os.makedirs(directory)


	filename = directory + '/trajData-' + str(x) + ',' + str(y) + '-' + str(numtraj) + '.pkl'

	# Write it onto file in pickle format
	cPickle.dump(trajectories, open(filename, 'wb'))

	print '----------------------------------------------------------'



if __name__ == '__main__':
	trajectory(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
