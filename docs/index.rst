=====================
agate-numpy |release|
=====================

About
=====

.. include:: ../README

Install
=======

To install:

.. code-block:: bash

    pip install agatenumpy

For details on development or supported platforms see the `agate documentation <http://agate.readthedocs.org>`_.

Usage
=====

agate-numpy uses agate's monkeypatching pattern to automatically add numpy support to all :class:`agate.Table <agate.table.Table>` instances.

.. code-block:: python

    import agate
    import agatenumpy

Once imported, you'll be able to use :meth:`.TableSQL.from_numpy` and :meth:`.TableSQL.to_numpy` as though they are members of :class:`agate.Table <agate.table.Table>`.

TKTK

===
API
===

.. autoclass:: agatenumpy.table.TableNumpy
    :members:

Authors
=======

.. include:: ../AUTHORS

License
=======

.. include:: ../COPYING

Changelog
=========

.. include:: ../CHANGELOG

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
