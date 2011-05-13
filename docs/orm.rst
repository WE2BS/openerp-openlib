OpenLib ORM Extension
=====================

.. module:: openlib.orm
    :synopsis: An extension to the OpenERP ORM.
.. currentmodule :: openlib

To use the OpenLib ORM Extension, you must import ExtendedOsv and Q classes: ::

    from openlib.orm import ExtendedOsv, Q

If you want your objects to natively support the extension, make them inherit from ExtendedOsv: ::

    class MyObject(osv.osv, ExtendedOsv):
        ...

The ExtendedOsv class
---------------------

.. class: ExtendedOsv

Every object which inherit from this class can use the following methods. These methods support a django-like style
and doesn't require you to pass them  *cr*, *uid* or *context* variables. These variables are recovered from the
execution stack.

.. note::

    All the methods described below supports *_cr*, *_uid* and *_context* arguments to override the ones found.


.. method:: ExtendedOsv.find([q=None, _object=None, _cr=None, _uid=None, \
    _context=None, _offset=0, _limit=None, _order=None, _count=None,  **kwargs])

    This methods is an equivalent the builtin :meth:`search` method but let you use a django-like syntax or
    Q objects instead of the polish notation used in :meth:`search`.

    :param q: A :class:`Q` object (the query).
    :param kwargs: Search keywords if you don't use :class:`Q`.
    :returns: A list of integers, corresponding to ids found.

    Find partners with name='Agrolait': ::

        partners_ids = self.find(name='Agrolait', _object='res.partners')

    Find partners with name='Agrolait' or 'AsusTek': ::

        partners_ids = self.find(Q(name='Agrolait') | Q(name='AsusTek'), _object='res.partners')

    

