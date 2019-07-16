# -*- coding: utf-8 -*-

import unittest
import image_utility as imgu
import tkinter as tk


class test_image_utility(unittest.TestCase):
    '''Runs basic unit tests on image_utility functions.'''

    def setUp(self):
        '''Initialize a tkinter object'''
        self.TK = tk.Tk()

    def test_board2img(self):
        '''test conversion of 2d list to PhotoImage'''

        board = [[0, 1], [0, 0], [1, 1]]
        img = imgu.board2img(board)

        for i in range(len(board)):
            for j in range(len(board[0])):
                self.assertEqual((1-board[i][j])*255, img.get(j, i)[0])

    def test_img2board(self):
        '''test conversion of PhotoImage to 2d list'''

        img = tk.PhotoImage(file='./maps/test.gif')
        board = [[0, 1], [0, 0], [1, 1]]

        for i in range(len(board)):
            for j in range(len(board[0])):
                self.assertEqual((1-board[i][j])*255, img.get(j, i)[0])

    def test_craete_random_board(self):
        '''test creation of random board'''

        board1 = imgu.create_random_board(2, 3, 0.5, 0)
        board2 = [[0, 0], [1, 1], [0, 1]]

        for i in range(len(board1)):
            for j in range(len(board1[0])):
                self.assertEqual(board1[i][j], board2[i][j])


if __name__ == '__main__':
    unittest.main()
