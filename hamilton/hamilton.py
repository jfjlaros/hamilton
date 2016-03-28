#!/usr/bin/env python

"""
Find a Hamiltonian path or cycle in a graph that is induced by a rectangular
board and a list of moves.


Copyright (c) 2016 Jeroen F.J. Laros <jlaros@fixedpoint.nl>

Licensed under the MIT license, see the LICENSE file.
"""

import argparse
import math
import sys

import yaml


class Hamilton(object):
    """
    Find a Hamiltonian path or cycle in a graph that is induced by a
    rectangular board and a list of moves.
    """
    def __init__(self, moves, x_size, y_size, x_start, y_start, closed=False):
        """
        :arg list moves: Definition of allowed moves.
        :arg int x_size: Height of the board.
        :arg int y_size: Width of the board.
        :arg int x: x-coordinate.
        :arg int y: y-coordinate.
        :arg bool closed: Find a closed path.
        """
        self._moves = moves
        self._x_size = x_size
        self._y_size = y_size

        self._max_depth = self._x_size * self._y_size
        self._decimals = int(math.log(self._max_depth, 10) + 1)

        self.reset(x_start, y_start, closed)

    def __str__(self):
        return '\n'.join(
            map(lambda r: ''.join(
            map(lambda e: ' {{:{}d}}'.format(self._decimals).format(e), r)),
            self.board)) + '\n'

    def _push(self, moves):
        self._stack.append([len(moves), moves])

    def _pop(self):
        return self._stack.pop()[1]

    def _current(self):
        return self._stack[-1][1][self._stack[-1][0]]

    def _next(self):
        if not self._stack[-1][0]:
            return ()

        self._stack[-1][0] -= 1
        return self._current()

    def _valid_moves(self, x, y):
        """
        Determine all valid moves, given a position.

        :arg int x: x-coordinate.
        :arg int y: y-coordinate.

        :returns list: List of valid moves.
        """
        moves = []

        for move in self._moves:
            _x = x + move[0]
            _y = y + move[1]
            if (_x >= 0 and _x < self._x_size and
                    _y >= 0 and _y < self._y_size and self.board[_x][_y] < 1):
                moves.append((_x, _y))

        return moves

    def _update(self, moves, amount):
        """
        Update accessibility of a list of moves.

        :arg list moves: List of moves.
        :arg int amount: Increase or decrease accessibility (1 or -1).
        """
        for move in moves:
            self.board[move[0]][move[1]] += amount

    def _prioritise(self, moves):
        """
        Prioritise a list of moves based on accessibility.

        :arg list moves: List of moves.

        :returns list: List of moves sorted by accessibility.
        """
        if not moves:
            return []

        weights = map(lambda x: self.board[x[0]][x[1]], moves)

        return zip(*sorted(zip(weights, moves)))[1]

    def _solve_recursive(self, x, y, depth=1):
        """
        :arg int x: x-coordinate.
        :arg int y: y-coordinate.
        :arg int depth: Move number.

        :returns bool: True for success, False for failure.
        """
        # Making any field inaccessible would be a better check.
        if self._closed and not self._valid_moves(
                self._x_start, self._y_start):
            return False

        self.board[x][y] = depth

        if depth == self._max_depth:
            return True

        moves = self._valid_moves(x, y)
        self._update(moves, 1)

        for move in self._prioritise(moves)[::-1]:
            if self._solve_recursive(move[0], move[1], depth + 1):
                return True

        self.retries += 1
        self.board[x][y] = -len(moves)
        self._update(moves, -1)

        return False

    def reset(self, x, y, closed=False):
        """
        Initialise the board and set the parameters for the path finding.

        :arg int x: x-coordinate.
        :arg int y: y-coordinate.
        :arg bool closed: Find a closed path.
        """
        self.board = [[0] * self._y_size for _ in range(self._x_size)]

        for i in range(self._x_size):
            for j in range(self._y_size):
                self.board[i][j] = -len(self._valid_moves(i, j))

        self._x_start = x
        self._y_start = y
        self._closed = closed
        self._stack = []
        self.retries = 0

    def solve_recursive(self):
        """
        Find a Hamiltonian path or cycle.

        :returns bool: True for success, False for failure.
        """
        return self._solve_recursive(self._x_start, self._y_start)

    def solve(self):
        """
        Find a Hamiltonian path or cycle.

        :returns bool: True for success, False for failure.
        """
        depth = 1
        self.board[self._x_start][self._y_start] = depth

        moves = self._prioritise(
            self._valid_moves(self._x_start, self._y_start))
        self._update(moves, 1)
        self._push(moves)

        while True:
            move = self._next()
            if move and not self._closed or self._valid_moves(
                    self._x_start, self._y_start):
                depth += 1
                self.board[move[0]][move[1]] = depth
                if depth == self._max_depth:
                    return True
                moves = self._prioritise(self._valid_moves(move[0], move[1]))
                self._update(moves, 1)
                self._push(moves)
            else:
                self.retries += 1
                moves = self._pop()
                if not self._stack:
                    return False
                undo = self._current()
                self.board[undo[0]][undo[1]] = -len(moves)
                self._update(moves, -1)
                depth -= 1


def hamilton(
        moves, height, width, x_start, y_start, closed, recursive, output):
    """
    Find a Hamiltonian path or cycle.

    :arg handle moves: Open readable handle to a YAML file containing
        the moves.
    :arg int height: Height of the board.
    :arg int width: Width of the board.
    :arg int x_start: x-coordinate of start position.
    :arg int y_start: y-coordinate of start position,
    :arg bool closed: Find a closed path.
    :arg bool recursive: Use recursive solver.
    """
    hamilton_path = Hamilton(
        yaml.load(moves)['moves'],
        height, width, x_start, y_start, closed)
    if not recursive:
        hamilton_path.solve()
    else:
        hamilton_path.solve_recursive()
    output.write(str(hamilton_path) + '\n')
    output.write('Number of retries: {}\n'.format(hamilton_path.retries))


def main():
    usage = __doc__.split('\n\n\n')
    parser = argparse.ArgumentParser(
        description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-m', dest='moves', type=argparse.FileType('r'),
        default=open('metita.yml'), help='game rules')
    parser.add_argument(
        '-o', dest='output', type=argparse.FileType('w'),
        default=sys.stdout, help='output file (default=<stdout>)')
    parser.add_argument(
        '-X', dest='height', type=int, default=10,
        help='height of the board (%(type)s default=%(default)s)')
    parser.add_argument(
        '-Y', dest='width', type=int, default=10,
        help='width of the board (%(type)s default=%(default)s)')
    parser.add_argument(
        '-x', dest='x_start', type=int, default=0,
        help='x-coordinate of start position (%(type)s default=%(default)s)')
    parser.add_argument(
        '-y', dest='y_start', type=int, default=0,
        help='y-coordinate of start position (%(type)s default=%(default)s)')
    parser.add_argument(
        '-c', dest='closed', default=False, action='store_true',
        help='find a closed path')
    parser.add_argument(
        '-r', dest='recursive', default=False, action='store_true',
        help='use recursive solver')

    arguments = parser.parse_args()

    hamilton(**dict((k, v) for k, v in vars(arguments).items()
        if k not in ('func', 'subcommand')))


if __name__ == '__main__':
    main()
