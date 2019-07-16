'''this file contains functions for converting to and from 2d lists and
PhotoImages.
Author: Nathan Willy
7/15/19
'''

import tkinter as tk
import random


def all_board2img(b_list):
    '''Run board2img on a list of 2d lists.  Return list of PhotoImage

    input:
        b_list, a list of 2d lists
    output:
        i_list, a list of PhotoImages
    '''

    i_list = []
    for board in b_list:
        i_list.append(board2img(board))
    return i_list


def board2img(board):
    '''Convert a 2d list of numericss into a PhotoImage.

    Elements in the list which are zeros (dead cells) are converted into white
    pixels.  Other elements are considered live cells and are converted to
    black pixels. The returned PhotoImage is of the same dimensions as board.
    Note: this method is the current processing bottleneck.

    input:
        board, a complete 2d list containing numeric values
    output:
        img, PhotoImage
    '''

    width = len(board[0])
    height = len(board)
    img = tk.PhotoImage(width=width, height=height)

    pix = ([255]*3 if board[j][i] == 0 else [0]*3
           for j in range(height)
           for i in range(width))

    pixels = " ".join(("{" + " ".join(('#%02x%02x%02x' %
        tuple(next(pix)) for i in range(width)))+"}" for j in range(height)))

    img.put(pixels, (0, 0, width, height))

    return img


def img2board(img):
    '''Convert a PhotoImage into a 2d list of 0s and 1s.

    It looks only at the red channel of the img, and, for pixels with a red
    value < 128 the list receives a 1, otherwise a 0.

    input:
        img, a PhotoImage
    output:
        board, a 2d list representing img
    '''

    board = [[1 if img.get(i, j)[0] < 128 else 0
              for i in range(img.width())]
             for j in range(img.height())]
    return board


def create_random_board(x_pos, y_pos, prob, seed):
    '''Create and return a random 2d list.

    The values of the list 0 or 1.

    inputs:
        x_pos, int, the width of board
        y_pos, int, the height of the board
        prob, float, the probability of a 1
        seed, float, the rng seed
    output:
        board, the randomly generated 2d list
    '''

    random.seed(seed)
    board = [[1 if random.random() < prob else 0
              for j in range(x_pos)]
             for i in range(y_pos)]
    return board
