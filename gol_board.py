# -*- coding: utf-8 -*-


class gol_board:

    '''Class represents an entire GOL sim

    This class performs all the logic and computations for advancing the
    simulation.

    attributes:
        born_numbers, list of ints where neighbor values turn 0 to a 1
        survive_numbers, list of ints where neighbor values maintain a 1 as a 1
        k_radius, int neighbors are found in a square kernel with side
                  k_radius * 2 + 1.
        boundary_condition, string used to select which bc to use in the sim
        size, list of ints [height, width] of the current sim
        generations, int number of time frames in the simulation
        states, 3d list of ints representing the state in eachtime point
                states[time][y_position][x_position]
        table, 2d list of ints represents the truth table for determining the
               next state of a cell. table[is_cell_alive][num_neighbors]
    '''

    born_numbers = [3]
    survive_numbers = [2, 3]
    k_radius = 1
    boundary_condition = 'torus'

    def __init__(self, start, gen):
        '''create a new simularion from a starting state running for some
        number of time steps.

        inputs:
            start, 2d list of ints, the starting state of the sim
            gen, int, the number of generations over which the sim is run
        '''
        self.table = []
        self.generations = gen
        self.states = [start]
        self.run()

    def run(self):
        '''advance the simulation for each time step and append the result to
        states
        '''

        self.init_rules_table()
        self.states = [self.states[0]]
        for i in range(self.generations):
            # print(i)
            board = self.states[-1]
            n_map = self.map_neighbors(board)
            self.states.append(self.step_board(board, n_map))

    def init_rules_table(self):
        '''Create a truth table describing the behavior of the simulation based
        on born_numbers and survive_numbers.  Set the reuslt to table
        '''

        self.table = [[0]*((self.k_radius*2+1)**2) for i in range(2)]

        for num in self.born_numbers:
            if num < len(self.table[0]) and num >= 0:
                self.table[0][num] = 1

        for num in self.survive_numbers:
            if num < len(self.table[1]) and num >= 0:
                self.table[1][num] = 1

#        print(self.table)

    def map_neighbors(self, board):
        '''Calculate and return a 2d list counting the number of neighbors in
        each cell.

        This function calls a sepate function where the calculation actually
        occurrs based on the value of boundary_condition.

        input:
            board, 2d list of ints (n x m), a single sim state
        output:
            n_map, 2d list of int (n x m), where each cell is the number of
                   neighbors at the corresponding location in board
        '''

        switcher = {
            'torus': self.map_neighbors_torus,
            'dead': self.map_neighbors_dead
            }

        return switcher[self.boundary_condition](board)

    def map_neighbors_torus(self, board):
        '''Calculate and return a 2d list counting the number of neighbors in
        each cell using a toroidal boundary condition.

        If board is dimension (n x m) then board[n, k] = board[0, k] etc

        input:
            board, 2d list of ints (n x m), a single sim state
        output:
            n_map, 2d list of int (n x m), where each cell is the number of
                   neighbors at the corresponding location in board
        '''

        n_map = [[0]*len(board[0]) for i in range(len(board))]

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    continue

                n_map[i][j] -= 1
                for di in range(-self.k_radius, self.k_radius+1):
                    i2 = (i+di) % len(board)
                    for dj in range(-self.k_radius, self.k_radius + 1):
                        j2 = (j+dj) % len(board[0])
                        n_map[i2][j2] += 1

        return n_map

    def map_neighbors_dead(self, board):
        '''Calculate and return a 2d list counting the number of neighbors in
        each cell using a dead boundary condition.

        If board is dimension (n x m) then board[n, k] = 0 etc

        input:
            board, 2d list of ints (n x m), a single sim state
        output:
            n_map, 2d list of int (n x m), where each cell is the number of
                   neighbors at the corresponding location in board
        '''
        n_map = [[0]*len(board[0]) for i in range(len(board))]

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    continue

                n_map[i][j] -= 1
                for di in range(-self.k_radius, self.k_radius+1):
                    i2 = i + di
                    if (i+di) % len(board) - i != di:
                        continue
                    for dj in range(-self.k_radius, self.k_radius+1):
                        j2 = j + dj
                        if (j+dj) % len(board[0]) - j != dj:
                            continue

                        n_map[i2][j2] += 1

        return n_map

    def step_board(self, board, n_map):
        '''Calculate and return the next step in the simulation.

        This function takes a board state and its neighbor map and looks up the
        next steps value in self.table.  Assumes board and n_map are the same
        size.

        e.g. if board[y][x] = is_alive and n_map[y][x] = num_neighbors
             then next_board[y][x] = self.table[is_alive][num_neighbors]

        inputs:
            board, 2d list of ints (n x m), a single sim state
            n_map, 2d list of int (n x m), where each cell is the number of
                   neighbors at the corresponding location in board
        output:
            board2, 2d list of ints (n x m), representing the next time state
            of the simulation.
        '''

        board2 = [[0]*len(board[0]) for i in range(len(board))]

        for i in range(len(board)):
            for j in range(len(board[0])):
                board2[i][j] = self.table[board[i][j]][n_map[i][j]]

        return board2
