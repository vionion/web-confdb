from .compat import PY26
from ._common import BidirectionalMapping
from collections import Hashable


if PY26:
    from .compat import iteritems

    class frozenbidict(BidirectionalMapping, Hashable):
        """
        Immutable, hashable bidict type.
        """
        def __hash__(self):
            if self._hash is None:
                self._hash = hash(frozenset(iteritems(self)))
            return self._hash

else:
    from .compat import viewitems

    class frozenbidict(BidirectionalMapping, Hashable):
        """
        Immutable, hashable bidict type.
        """
        def __hash__(self):
            if self._hash is None:
                self._hash = hash(frozenset(viewitems(self)))
            return self._hash
