import os
import sys
from random import randrange
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import CS3243_P1_46_1 as bfs
import CS3243_P1_46_2 as hamming
import CS3243_P1_46_3 as euclidean
import CS3243_P1_46_4 as manhattan

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

    if n == 3 :
	    puzzle1 = bfs.Puzzle(init_state, goal_state, n)
	    print('BFS TIME: ')
	    print(puzzle1.getSolutionTime())
	    print('TOTAL NODES EXPLORED: ')
	    print(puzzle1.totalNodes)
	    print('MAX FRONTIER SIZE: ')
	    print(puzzle1.maxFrontier)

    puzzle2 = hamming.Puzzle(init_state, goal_state, n)
    print('HAMMING TIME: ')
    print(puzzle2.getSolutionTime())
    print('TOTAL NODES EXPLORED: ')
    print(puzzle2.totalNodes)
    print('MAX FRONTIER SIZE: ')
    print(puzzle2.maxFrontier)

    puzzle3 = euclidean.Puzzle(init_state, goal_state, n)
    print('EUCLIDEAN TIME: ')
    print(puzzle3.getSolutionTime())
    print('TOTAL NODES EXPLORED: ')
    print(puzzle3.totalNodes)
    print('MAX FRONTIER SIZE: ')
    print(puzzle3.maxFrontier)

    puzzle4 = manhattan.Puzzle(init_state, goal_state, n)
    print('MANHATTAN TIME: ')
    print(puzzle4.getSolutionTime())
    print('TOTAL NODES EXPLORED: ')
    print(puzzle4.totalNodes)
    print('MAX FRONTIER SIZE: ')
    print(puzzle4.maxFrontier)

    '''with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')'''