from trajectory import *

def generate_trajectories(numtraj):
	init_points = [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3), (4,1)]

	for points in init_points:
		trajectory(points[0], points[1], numtraj)


if __name__=='__main__':
	generate_trajectories(int(sys.argv[1]))
