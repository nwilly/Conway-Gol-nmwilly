# -*- coding: utf-8 -*-

import unittest
import gol_board


class test_gol_board(unittest.TestCase):
    '''Runs basic unit tests on gol_board functions.'''

    def setUp(self):
        '''create test board and initialize a gol_board'''
        self.start = [[0, 1], [0, 0], [1, 1]]
        self.gb = gol_board.gol_board(self.start, 2)

    def test_init_rules_table(self):
        '''test initialization of the rules table using B2/S23'''
        table = [[0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0]]

        self.assertEqual(table, self.gb.table)

    def test_map_neighbors_torus(self):
        '''tests the neighbor counting under toroidal boundary condition'''
        n_map1 = [[5, 3], [5, 4], [4, 3]]
        n_map2 = self.gb.map_neighbors_torus(self.start)
        self.assertEqual(n_map1, n_map2)

    def test_map_neighbors_dead(self):
        '''test the neighbor counting under dead boundary condition'''
        n_map1 = [[1, 0], [3, 3], [1, 1]]
        n_map2 = self.gb.map_neighbors_dead(self.start)
        self.assertEqual(n_map1, n_map2)

    def test_step_board(self):
        '''test calculation of next state assuming correct (toroidal) n_map.'''
        n_map = [[5, 3], [5, 4], [4, 3]]
        board1 = [[0, 1], [0, 0], [0, 1]]
        board2 = self.gb.step_board(self.board, n_map)

        self.assertEqual(board1, board2)

    board = [[0, 1], [0, 0], [1, 1]]
    if __name__ == '__main__':
        unittest.main()
