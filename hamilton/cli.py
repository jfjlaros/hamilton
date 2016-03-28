#!/usr/bin/env python
"""
Command line interface for the Hamiltonian path or cycle finder.
"""
import argparse
import sys

import yaml

from . import Hamilton, usage, version


def hamilton(
        moves, height, width, x_start, y_start, closed, recursive, max_retries,
        output):
    """
    Find a Hamiltonian path or cycle.

    :arg handle moves: Open readable handle to a YAML file containing
        the moves.
    :arg int height: Height of the board.
    :arg int width: Width of the board.
    :arg int x_start: x-coordinate of start position.
    :arg int y_start: y-coordinate of start position,
    :arg bool closed: Find a closed path.
    :arg int max_retries: Maximum number of retries (0=disabled).
    :arg bool recursive: Use recursive solver.
    """
    hamilton_path = Hamilton(
        yaml.load(moves)['moves'],
        height, width, x_start, y_start, closed, max_retries)
    if not recursive:
        solver = hamilton_path.solve
    else:
        solver = hamilton_path.solve_recursive

    if solver():
        output.write(str(hamilton_path) + '\n')
        output.write('Number of retries: {}\n'.format(hamilton_path.retries))
    else:
        output.write('No solution found.\n')


def main():
    parser = argparse.ArgumentParser(
        description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'moves', metavar='MOVES', type=argparse.FileType('r'),
        help='game rules')
    parser.add_argument(
        'height', metavar='HEIGHT', type=int,
        help='height of the board (%(type)s)')
    parser.add_argument(
        'width', metavar='WIDTH', type=int,
        help='width of the board (%(type)s)')
    parser.add_argument(
        'x_start', metavar='X_START', type=int,
        help='x-coordinate of start position (%(type)s)')
    parser.add_argument(
        'y_start', metavar='Y_START', type=int,
        help='y-coordinate of start position (%(type)s)')
    parser.add_argument(
        '-o', dest='output', type=argparse.FileType('w'),
        default=sys.stdout, help='output file (default=<stdout>)')
    parser.add_argument(
        '-c', dest='closed', default=False, action='store_true',
        help='find a closed path')
    parser.add_argument(
        '-m', dest='max_retries', type=int, default=0,
        help='maximum number of retries (%(type)s default=%(default)s ' \
        '(disabled))')
    parser.add_argument(
        '-r', dest='recursive', default=False, action='store_true',
        help='use recursive solver')
    parser.add_argument('-v', action='version', version=version(parser.prog))

    arguments = parser.parse_args()

    hamilton(**dict((k, v) for k, v in vars(arguments).items()
        if k not in ('func', 'subcommand')))


if __name__ == '__main__':
    main()
