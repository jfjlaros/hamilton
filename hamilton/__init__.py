"""
Find a Hamiltonian path or cycle in a graph that is induced by a rectangular
board and a list of moves.


Copyright (c) 2016 Jeroen F.J. Laros <jlaros@fixedpoint.nl>

Licensed under the MIT license, see the LICENSE file.
"""
from .hamilton import Hamilton


__version_info__ = ('0', '0', '1')

__version__ = '.'.join(__version_info__)
__author__ = 'Jeroen F.J. Laros'
__contact__ = 'jaros@fixedpoint.nl'
__homepage__ = 'https://github.com/jfjlaros/hamilton'


usage = __doc__.split('\n\n\n')


def doc_split(func):
    return func.__doc__.split("\n\n")[0]


def version(name):
    return '{} version {}\n\nAuthor   : {} <{}>\nHomepage : {}'.format(
        name, __version__, __author__, __contact__, __homepage__)
