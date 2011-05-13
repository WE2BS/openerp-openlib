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
execution stack. This means that you **must** have variables named *cr*, *uid*, and *context* (optional) when
you call these methods. Generally, these variables are passed by OpenERP.

.. note::

    All the methods described below supports *_cr*, *_uid* and *_context* arguments to override the ones found
    automatically in the python stack. We use '_' at the begin of arguments for methods which support django-like
    searching by arguments to avoid conflicts.

find
~~~~

.. method:: ExtendedOsv.find([q=None, _object=None, _offset=0, _limit=None, _order=None, _count=None,  **kwargs])

    This methods is an equivalent to the builtin :meth:`search` method but let you use a django-like syntax or
    :class:`Q` objects instead of the polish notation used in :meth:`search`.

    :param q: A :class:`Q` object (the query).
    :param kwargs: Search keywords if you don't use :class:`Q`.
    :returns: A list of integers, corresponding to ids found.

    .. note ::

        if you specify one of the *_limit*, *_offset*, *_order* or *_count* arguments, they will be passed to :meth:`search`.

**Examples**

Find partners with name='Agrolait': ::

    partners_ids = self.find(name='Agrolait', _object='res.partners')

Find partners with name='Agrolait' or 'AsusTek': ::

    partners_ids = self.find(Q(name='Agrolait') | Q(name='AsusTek'), _object='res.partners')

In the case you are using :meth:`find` on an object which inherit :class:`ExtendedOsv`, you can omit the *_object*
argument: ::

    objects_ids = self.find(name='OK')

filter
~~~~~~

.. method:: ExtendedOsv.filter([value=None, _object=None, **kwargs])

    This method is a kind of search-and-browse. It uses :meth:`find` to search ids and then return the result of a
    :meth:`browse` call so you can iterate over the results.

    :param value: Can be a :class:`Q` object or a list of ids.
    :param kwargs: Search keywords if you don't specify *value*.
    :returns: A list of objects as returned by :meth:`browse`.

**Examples**

Iterate over partners whose name starts with 'A': ::

    for partner in self.filter(name__startswith='A', _object='res.partner'):
        ...

Same with a :class:`Q` object: ::

    for partner in self.filter(Q(name__startswith='A') | Q(name__startswith='B'), _object='res.partner'):
        ...

Iterate over a list of ids of one of our objects: ::

    for obj in self.filter([1, 2, 3]):
        ...

get
~~~

.. method:: ExtendedOsv.get([value=None, _object=None, **kwargs])

    This method act like :meth:`filter` but returns only one object. *value* can be one of the following :

        * An integer, then the object corresponding to this id is returned
        * A string, then the object with this XMLID is returned
        * A :class:`Q` object, return the first object corresponding to the criteria.
        * None, then the first object corresponding to the search keywords is returned

    :param value: The search criteria (see above)
    :param kwargs: If *value* is None, search keywords
    :returns: An object as returned by :meth:`browse` or None.

**Examples**

Returns the group whose XMLID is 'group_employee': ::

    group = self.get('base.group_employee', _object='res.groups')

Returns the user with the id 1: ::

    admin = self.get(1, _object='res.users')

Returns the first partner whose name is 'Agrolait': ::

    partner = self.get(name='Agrolait')

xmlid_to_id
~~~~~~~~~~~

.. method:: ExtendedOsv.xmlid_to_id(cr, uid, xmlid, context=None)

    This method returns the database ID corresponding the *xmlid* passed, or None.

    .. note::

        This method does not uses automatic detection of cr, uid and context. 
