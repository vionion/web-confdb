# -*- coding: utf-8 -*-

import os
import tempfile

try:
    from Config import state_dir

except:
    state_dir = tempfile.gettempdir()
    if 'STATEDIR' in os.environ:
        state_dir = os.environ.get('STATEDIR')

