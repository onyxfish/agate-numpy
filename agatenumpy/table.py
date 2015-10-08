#!/usr/bin/env python

import agate
import numpy

#: Maps agate data types to numpy data types
NUMPY_TYPE_MAP = {
    agate.Boolean: 'bool_',
    agate.Number: 'float_',
    agate.Date: 'datetime64[D]',
    agate.DateTime: 'datetime64[us]',
    agate.TimeDelta: 'timedelta64[us]',
    # agate.Text: object    # See :meth:`TableNumpy._make_numpy_column`
}

CONVERSION_FUNCS = {
    agate.Boolean: lambda v: v,
    agate.Number: lambda v: v,
    agate.Date: lambda v: v,
    agate.DateTime: lambda v: v,
    agate.TimeDelta: lambda v: v,
    agate.Text: lambda v: u'' if v is None else v,  # No
}

class TableNumpy(object):
    @classmethod
    def from_numpy(cls, numpy_table):
        """
        Create a new :class:`agate.Table` from a given numpy array.

        Monkey patched as class method :meth:`Table.from_numpy`.
        """
        pass

    def _make_numpy_column(self, column):
        """
        Creates a numpy dtype from agate column data.

        :param column_name: The name of the column.
        :param column_type: The agate type of the column.
        """
        numpy_column_type = None

        # Text specification requires max value length
        if isinstance(column.data_type, agate.Text):
            max_length = column.aggregate(agate.MaxLength())
            numpy_column_type = 'U%i' % max_length
        else:
            for agate_type, numpy_type in NUMPY_TYPE_MAP.items():
                if isinstance(column.data_type, agate_type):
                    numpy_column_type = numpy_type
                    break

        if numpy_column_type is None:
            raise ValueError('Unsupported column type: %s' % column.data_type)

        return (column.name, numpy_column_type)

    def to_numpy(self):
        """
        Convert this table to an equivalent numpy array.

        This conversion is lossless with a couple notable exceptions:

        - :code:`None` in :class:`.Boolean` columns is converted to
          :code:`False`.
        - :code:`None` in :class:`.Text` columns is converted to an empty
          string.

        Monkey patched as instance method :meth:`.Table.to_numpy`.
        """
        numpy_types = []
        conversion_funcs = []

        for i, column in enumerate(self.columns):
            numpy_types.append(self._make_numpy_column(column))

            for agate_type, func in CONVERSION_FUNCS.items():
                if isinstance(column.data_type, agate_type):
                    conversion_funcs.append(func)
                    break

        data = []

        for row in self.rows:
            data.append(tuple(conversion_funcs[i](v) for i, v in enumerate(row)))

        return numpy.array(data, dtype=numpy_types)
