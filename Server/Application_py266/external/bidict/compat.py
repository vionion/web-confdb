"""
Python 2/3 compatibility helpers.
"""

from sys import version_info

PY2 = version_info[0] == 2
PY26 = PY2 and (version_info[1] == 6)

if PY2:
    assert version_info[1] >= 6, 'Python >= 2.6 required'

    iteritems = lambda x: x.iteritems()
    if not PY26:
        viewitems = lambda x: x.viewitems()
else:
    iteritems = lambda x: iter(x.items())
    viewitems = lambda x: x.items()

iteritems.__doc__ = 'Python 2/3 compatible iteritems'
if not PY26:
    viewitems.__doc__ = 'Python 2/3 compatible viewitems'
