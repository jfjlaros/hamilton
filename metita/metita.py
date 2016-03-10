#!/usr/bin/env python

import sys


moves = ((-3, 0), (-2, 2), (0, 3), (2, 2), (3, 0), (2, -2), (0, -3), (-2, -2))


def make_board(x, y):
    return [[0] * y for _ in range(x)]


def metita(board, x, y, depth=1):
    """
    """
    board[x][y] = depth

    if depth == len(board) * len(board[0]):
        return True

    for move in moves:
        _x = x + move[0]
        _y = y + move[1]
        if (_x >= 0 and _x < len(board) and _y >= 0 and _y < len(board[0]) and
                board[_x][_y] == 0):
            if metita(board, _x, _y, depth + 1):
                return True

    board[x][y] = 0
    return False


def print_solution(board, handle=sys.stdout):
    for row in board:
        for element in row:
            handle.write(' {:2d}'.format(element))
        handle.write('\n')
    handle.write('\n')


def main():
    """
    """
    board = make_board(10, 6)
    metita(board, 0, 0)
    print_solution(board)


if __name__ == '__main__':
    main()
