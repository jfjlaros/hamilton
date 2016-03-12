#!/usr/bin/env python

import argparse
import sys

import yaml


MOVES = yaml.load(open("moves.yml"))['moves']


def _valid_moves(board, x, y):
    moves = []

    for move in MOVES:
        _x = x + move[0]
        _y = y + move[1]
        if (_x >= 0 and _x < len(board) and _y >= 0 and _y < len(board[0]) and
                board[_x][_y] < 1):
            moves.append((_x, _y))

    return moves


def make_board(x, y):
    board = [[0] * y for _ in range(x)]

    for i in range(x):
        for j in range(y):
            board[i][j] = -len(_valid_moves(board, i, j))

    return board


def _prioritise(board, moves):
    #weights = map(lambda x: min(x[0], len(board) - x[0] - 1) +
    #    min(x[1], len(board[0]) - x[1] - 1), moves)
    weights = map(lambda x: -board[x[0]][x[1]], moves)
    print weights
    return zip(*sorted(zip(weights, moves)))[1]


def do_move(board, x, y, depth=1):
    """
    """
    board[x][y] = depth

    if depth == len(board) * len(board[0]):
        return True

    _moves = _valid_moves(board, x, y)
    for move in _moves:
        board[move[0]][move[1]] += 1
    print_board(board)

    if _moves:
        for move in _prioritise(board, _moves):
            if do_move(board, move[0], move[1], depth + 1):
                return True

    board[x][y] = -1
    for move in _moves:
        board[move[0]][move[1]] -= 1
    return False


def print_board(board, handle=sys.stdout):
    for row in board:
        for element in row:
            handle.write(' {:3d}'.format(element))
        handle.write('\n')
    handle.write('\n')


def metita(x, y, i, j):
    board = make_board(x, y)
    do_move(board, i, j)
    print_board(board)


def main():
    """
    """
    metita(19, 19, 0, 0)


if __name__ == '__main__':
    main()
