import os
import sys
from copy import deepcopy
import time
import collections

#check for the empty position	
def check_empty(grid):
	for i, j in enumerate(grid):
		for x, y in enumerate(j):
			if y == 0:
				return i, x

#number move to the left	
def left(grid, n, i, j):
	if j == n-1: #empty blk on the most right
		return None
	else:
		temp_grid = deepcopy(grid)
		temp_grid[i][j] = temp_grid[i][j+1]
		temp_grid[i][j+1] = 0
		return temp_grid
		
#number move to the right	
def right(grid, i, j):
	if j == 0: #empty blk on the most left
		return None
	else:
		temp_grid = deepcopy(grid)
		temp_grid[i][j] = temp_grid[i][j-1]
		temp_grid[i][j-1] = 0
		return temp_grid
	
#number move up	
def up(grid, n, i, j):
	if i == n-1: #empty block on the bottom
		return None
	else:
		temp_grid = deepcopy(grid)
		temp_grid[i][j] = temp_grid[i+1][j]
		temp_grid[i+1][j] = 0
		return temp_grid

#number move down
def down(grid, i, j):
	if i == 0: #empty block on the top
		return None
	else:
		temp_grid = deepcopy(grid)
		temp_grid[i][j] = temp_grid[i-1][j]
		temp_grid[i-1][j] = 0
		return temp_grid

#pop neighbor then create
def create_grid(operation, grid, n, row, col):
	if operation == 'LEFT':
		return left(grid, n, row, col)
	elif operation == 'RIGHT':
		return right(grid, row, col)
	elif operation == 'UP':
		return up(grid, n, row, col)
	elif operation == 'DOWN':
		return down(grid, row, col)
	else: return None

#trace back to get the steps			
def trace_back(current_state):
	operation_list = list()
	operation_list.append(current_state.operation)
	
	while current_state.parent.operation is not None: #do not iterate the initial state
		operation_list.append(current_state.parent.operation)
		current_state = current_state.parent	
	
	operation_list.reverse()
	return operation_list
		
#check if the current_state is the goal_state 
def is_goal_state(current_state, goal_state):
	if current_state.grid == goal_state:
		return True
	else:
		return False
		
#check if the puzzle is solvable
def is_Solvable(init_state):
	a = list()
	for i, j in enumerate(init_state):
		for x, y in enumerate(j):
			a.append(y)
	count = 0;
	for i in range(len(a)-1):
		j = i + 1
		while (j < len(a)):
			if a[i] != 0 and a[j] != 0:
				if a[i] > a[j]:
					count += 1
			j += 1
	if count%2 == 0:
		return True
	else: 
		return False
			
def to_tuple(grid):
	return tuple(tuple(i) for i in grid)

class State:
	def __init__(self, grid, operation, parent):
		self.grid = grid
		self.operation = operation
		self.parent = parent

class Puzzle(object):
	def __init__(self, init_state, goal_state, n): #constructor
		# you may add more attributes if you think is useful
		self.init_state = init_state
		self.goal_state = goal_state
		self.n = n
		self.totalNodes = 1
		self.maxFrontier = 1
		self.frontierSize = 1

	def solve(self):
		#TODO
		# implement your search algorithm here
		start = time.time()
		
		if is_Solvable(self.init_state) == False:
			return ["UNSOLVABLE"]
		
		state = State(self.init_state, None, None)
		operations = ["UP", "DOWN", "LEFT", "RIGHT"]
		q = collections.deque() #a queue to store unexplored states
		q.append(state)
		visited = set() #store explored states
		
		while len(q) > 0:
			current_state = q.popleft()
			self.totalNodes += 1
			self.frontierSize -= 1
			current_grid = current_state.grid
			visited.add(to_tuple(current_grid))
		
			row, col = check_empty(current_grid)
			for i in operations:
				child_grid = create_grid(i, current_grid, self.n, row, col) #check can move in which direction
				if child_grid is not None:
					if to_tuple(child_grid) not in visited:
						#create a new State
						child_state = State(child_grid, i, current_state)
						#check for goal state
						is_goal = is_goal_state(child_state, self.goal_state)
						if is_goal is True:
							operation_list = trace_back(child_state)
							end = time.time()
							return operation_list
						else:
							#store the unexplore state to queue
							q.append(child_state)
							self.frontierSize += 1
							if (self.frontierSize > self.maxFrontier):
								self.maxFrontier = self.frontierSize
		
	def getSolutionTime(self):
		start_time = time.time()
		self.solve()
		return time.time() - start_time	

if __name__ == "__main__":
	# do NOT modify below

	# argv[0] represents the name of the file that is being executed
	# argv[1] represents name of input file
	# argv[2] represents name of destination output file
	if len(sys.argv) != 3:
		raise ValueError("Wrong number of arguments!")

	try:
		f = open(sys.argv[1], 'r')
	except IOError:
		raise IOError("Input file not found!")

	lines = f.readlines()
	
	# n = num rows in input file
	n = len(lines)
	# max_num = n to the power of 2 - 1
	max_num = n ** 2 - 1

	# Instantiate a 2D list of size n x n
	init_state = [[0 for i in range(n)] for j in range(n)]
	goal_state = [[0 for i in range(n)] for j in range(n)]
	

	i,j = 0, 0
	for line in lines:
		for number in line.split(" "):
			if number == '':
				continue
			value = int(number , base = 10)
			if  0 <= value <= max_num:
				init_state[i][j] = value
				j += 1
				if j == n:
					i += 1
					j = 0

	for i in range(1, max_num + 1):
		goal_state[(i-1)//n][(i-1)%n] = i
	goal_state[n - 1][n - 1] = 0

	puzzle = Puzzle(init_state, goal_state, n)
	ans = puzzle.solve()

	with open(sys.argv[2], 'a') as f:
		for answer in ans:
			f.write(answer+'\n')