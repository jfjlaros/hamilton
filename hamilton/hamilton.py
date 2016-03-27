#!/usr/bin/env python

import argparse
import math
import sys

import yaml


class Hamilton(object):
    """
    """
    def __init__(self, moves, x_size, y_size):
        """
        """
        self._moves = moves
        self._x_size = x_size
        self._y_size = y_size
        self._max_depth = self._x_size * self._y_size
        self._decimals = int(math.log(self._max_depth, 10) + 1)
        self._stack = []
        self.tries = 0
        self.board = [[0] * self._y_size for _ in range(self._x_size)]

        self.reset()

    def __str__(self):
        string = ''

        for row in self.board:
            for element in row:
                string += ' {{:{}d}}'.format(self._decimals).format(element)
            string += '\n'

        return string

    def _dump_stack(self):
        for element in self._stack:
            print element
        print

    def _push(self, moves):
        self._stack.append([len(moves), moves])

    def _pop(self):
        return self._stack.pop()

    def _current(self):
        return self._stack[-1][1][self._stack[-1][0]]

    def _next(self):
        if not self._stack[-1][0]:
            return ()

        self._stack[-1][0] -= 1
        return self._current()

    def _valid_moves(self, x, y):
        """
        """
        moves = []

        for move in self._moves:
            _x = x + move[0]
            _y = y + move[1]
            if (_x >= 0 and _x < self._x_size and
                    _y >= 0 and _y < self._y_size and self.board[_x][_y] < 1):
                moves.append((_x, _y))

        return moves

    def _prioritise(self, moves):
        """
        """
        if not moves:
            return []

        weights = map(lambda x: -self.board[x[0]][x[1]], moves)

        return zip(*sorted(zip(weights, moves)))[1]

    def reset(self):
        """
        """
        for i in range(self._x_size):
            for j in range(self._y_size):
                self.board[i][j] = -len(self._valid_moves(i, j))

    def solve_recursive(self, x, y, depth=1):
        """
        """
        if not self._valid_moves(0, 0):
            return False

        self.board[x][y] = depth
        self.tries += 1

        if depth == self._max_depth:
            return True

        moves = self._valid_moves(x, y)
        for move in moves:
            self.board[move[0]][move[1]] += 1

        for move in self._prioritise(moves):
            if self.solve(move[0], move[1], depth + 1):
                return True

        self.board[x][y] = -len(moves)
        for move in moves:
            self.board[move[0]][move[1]] -= 1

        return False

    def solve(self, x, y):
        """
        """
        depth = 1
        self.board[x][y] = depth
        self._push(self._valid_moves(x, y))

        while True:
            move = self._next()
            if move:
                moves = self._valid_moves(move[0], move[1])
                depth += 1
                self.board[move[0]][move[1]] = depth
                if depth == self._max_depth:
                    return
                self._push(moves)
            else:
                self._pop()
                if not self._stack:
                    return
                undo = self._current()
                self.board[undo[0]][undo[1]] = -1
                depth -= 1


def hamilton(handle, x, y, i, j):
    """
    """
    h = Hamilton(yaml.load(handle)['moves'], x, y)
    print h
    h.solve(i, j)
    print h
    print h.tries


def main():
    """
    """
    parser = argparse.ArgumentParser(
        description='', epilog='',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-m', dest='moves', type=argparse.FileType('r'),
        default=open('metita.yml'), help='game rules')
    parser.add_argument('-x', dest='x', type=int, default=10, help='height')
    parser.add_argument('-y', dest='y', type=int, default=10, help='width')
    parser.add_argument('-i', dest='i', type=int, default=0, help='x position')
    parser.add_argument('-j', dest='j', type=int, default=0, help='y position')

    arguments = parser.parse_args()

    hamilton(arguments.moves, arguments.x, arguments.y, arguments.i,
        arguments.j)


if __name__ == '__main__':
    main()
