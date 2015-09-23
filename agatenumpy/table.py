#!/usr/bin/env python

from datetime import datetime
from decimal import Decimal

import agate

import numpy

#: Maps agate data types to numpy data types
NUMPY_TYPE_MAP = {
    agate.Boolean: 'bool_',
    agate.Number: 'float_',
    agate.Date: 'datetime64[D]',
    agate.DateTime: 'datetime64[us]',
    agate.TimeDelta: 'timedelta64[us]',
    agate.Text: 'unicode_'
}

class TableNumpy(object):
    @classmethod
    def from_numpy(cls, numpy_table):
        """
        Create a new :class:`agate.Table` from a given numpy array.

        Monkey patched as class method :meth:`Table.from_numpy`.
        """
        pass

    def _make_numpy_column(self, column_name, column_type):
        """
        Creates a numpy dtype from agate column data.

        :param column_name: The name of the column.
        :param column_type: The agate type of the column.
        """
        numpy_column_type = None

        for agate_type, numpy_type in NUMPY_TYPE_MAP.items():
            if isinstance(column_type, agate_type):
                numpy_column_type = numpy_type
                break

        if numpy_column_type is None:
            raise ValueError('Unsupported column type: %s' % column_type)

        return (column_name, numpy_column_type)

    def to_numpy(self):
        """
        Convert this table to an equivalent numpy array. Note that
        :class:`.Date` columns are not supported since numpy does not have a
        corresponding data type.

        Monkey patched as instance method :meth:`.Table.to_numpy`.
        """
        numpy_types = []

        for column_name, column_type in zip(self.column_names, self.column_types):
            numpy_types.append(self._make_numpy_column(column_name, column_type))

        data = [tuple([c for c in row]) for row in self.rows]

        return numpy.array(data, dtype=numpy_types)
