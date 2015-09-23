#!/usr/bin/env python

import agate
import agatenumpy

table = agate.Table.from_numpy('TKTK')

print table.column_names
print table.column_types
print len(table.columns)
print len(table.rows)

table.to_numpy('TKTK')
