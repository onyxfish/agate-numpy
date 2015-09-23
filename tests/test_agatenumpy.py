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
        pass

    def test_to_numpy(self):
        numpy_table = self.table.to_numpy()

        self.assertEqual(len(numpy_table), len(self.table.rows))
        numpy.testing.assert_array_equal(numpy_table['number'], [1, 2, numpy.nan])
        # numpy.testing.assert_array_equal(numpy_table['text'], [u'a', u'b', ''])
        # numpy.testing.assert_array_equal(numpy_table['boolean'], [1, 0, numpy.nan])
        numpy.testing.assert_array_equal(numpy_table['date'], [date(2015, 10, 1), date(2015, 11, 1), None])
        numpy.testing.assert_array_equal(numpy_table['datetime'], [datetime(2015, 10, 1, 12, 30), datetime(2015, 11, 1, 12, 45), None])
        numpy.testing.assert_array_equal(numpy_table['timedelta'], [timedelta(hours=4, minutes=45), timedelta(hours=3, minutes=25), None])
