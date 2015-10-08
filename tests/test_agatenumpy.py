#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import date, datetime, timedelta

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import agate
import numpy

import agatenumpy

agatenumpy.patch()

class TestNumpy(unittest.TestCase):
    def setUp(self):
        self.rows = (
            ('1', 'a', 'True', '10/01/2015', '10/01/2015 12:30 PM', '4h45m'),
            ('2', 'b', 'False', '11/01/2015', '11/01/2015 12:45 PM', '3h25m'),
            ('', '', '', '', '', '')
        )

        self.number_type = agate.Number()
        self.text_type = agate.Text()
        self.boolean_type = agate.Boolean()
        self.date_type = agate.Date()
        self.datetime_type = agate.DateTime()
        self.timedelta_type = agate.TimeDelta()

        self.column_names = ('number', 'text', 'boolean', 'date', 'datetime', 'timedelta')
        self.column_types = (self.number_type, self.text_type, self.boolean_type, self.date_type, self.datetime_type, self.timedelta_type)

        self.table = agate.Table(self.rows, zip(self.column_names, self.column_types))

    def test_from_numpy(self):
        data = [
            (1, u'a', True, date(2015, 10, 1), datetime(2015, 10, 1, 12, 30), timedelta(hours=4, minutes=45)),
            (2, u'b', False, date(2015, 11, 1), datetime(2015, 11, 1, 12, 45), timedelta(hours=3, minutes=25)),
            (numpy.nan, u'', False, None, None, None)
        ]

        numpy_types = [
            'float_',
            'U1',
            'bool_',
            'datetime64[D]',
            'datetime64[us]',
            'timedelta64[us]'
        ]

        numpy_table = numpy.rec.array(data, dtype=zip(self.column_names, numpy_types))

        # for name, dtype in numpy_table.dtype:

        print numpy_table

        for column_name in numpy_table.dtype.names:
            numpy_type = numpy_table.dtype.fields[column_name][0]

            print numpy_type.type, numpy_type.descr

        table = agate.Table.from_numpy(numpy_table)

        self.assertEqual(len(table.rows), len(numpy_table))
        self.assertEqual(table.columns['number'], [1, 2, None])
        self.assertEqual(table.columns['text'], [u'a', u'b', u''])
        self.assertEqual(table.columns['boolean'], [True, False, False])
        self.assertEqual(table.columns['date'], [date(2015, 10, 1), date(2015, 11, 1), None])
        self.assertEqual(table.columns['datetime'], [datetime(2015, 10, 1, 12, 30), datetime(2015, 11, 1, 12, 45), None])
        self.assertEqual(table.columns['timedelta'], [timedelta(hours=4, minutes=45), timedelta(hours=3, minutes=25), None])

    def test_to_numpy(self):
        numpy_table = self.table.to_numpy()

        print type(numpy_table)

        self.assertEqual(len(numpy_table), len(self.table.rows))
        numpy.testing.assert_array_equal(numpy_table['number'], [1, 2, numpy.nan])
        numpy.testing.assert_array_equal(numpy_table['text'], [u'a', u'b', u''])
        numpy.testing.assert_array_equal(numpy_table['boolean'], [True, False, False])
        numpy.testing.assert_array_equal(numpy_table['date'], [date(2015, 10, 1), date(2015, 11, 1), None])
        numpy.testing.assert_array_equal(numpy_table['datetime'], [datetime(2015, 10, 1, 12, 30), datetime(2015, 11, 1, 12, 45), None])
        numpy.testing.assert_array_equal(numpy_table['timedelta'], [timedelta(hours=4, minutes=45), timedelta(hours=3, minutes=25), None])
