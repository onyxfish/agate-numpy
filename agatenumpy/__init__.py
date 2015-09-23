#!/usr/bin/env python

import agate
from agatenumpy.table import TableNumpy

# Monkeypatch!
agate.Table.monkeypatch(TableNumpy)
