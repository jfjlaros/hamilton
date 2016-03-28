#!/usr/bin/env python
"""
Command line interface for the Hamiltonian path or cycle finder.
"""
import argparse
import sys

import yaml

from . import Hamilton, usage, version


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
    parser.add_argument('-v', action='version', version=version(parser.prog))

    arguments = parser.parse_args()

    hamilton(**dict((k, v) for k, v in vars(arguments).items()
        if k not in ('func', 'subcommand')))


if __name__ == '__main__':
    main()
