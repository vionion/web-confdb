# -*- coding: utf-8 -*-

"""
Efficient, Pythonic bidirectional map implementation
and related functionality.

.. :copyright: (c) 2015 Joshua Bronson.
.. :license: ISCL. See LICENSE for details.

"""

from ._common import BidirectionalMapping, CollapseException
from ._bidict import bidict
from ._collapsing import collapsingbidict
from ._frozen import frozenbidict
from ._named import namedbidict
from .util import pairs, inverted

__all__ = (
    'BidirectionalMapping',
    'CollapseException',
    'bidict',
    'collapsingbidict',
    'frozenbidict',
    'namedbidict',
    'pairs',
    'inverted',
)

__version__ = '0.10.0.20083b03797eab2710d12eef0eb6dc6c26c0c9a4'
