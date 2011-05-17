OpenLib Tools
=============

.. module:: openlib.tools
    :synopsis: Utility functions.
.. currentmodule :: openlib.tools

This module contains functions that could be useful.

Date and time tools
-------------------

All these functions uses the OpenERP default timestamps by default as format.

.. function:: to_date(date_string, format=DEFAULT_SERVER_DATE_FORMAT)

    Converts the *date_string* passed as an argument to a :class:`datetime.date` object.

.. function:: to_time(time_string, format=DEFAULT_SERVER_TIME_FORMAT)

    Converts the *time_string* argument to a :class:`datetime.time` object.

.. function:: to_datetime(datetime_string, format=DEFAULT_SERVER_DATETIME_FORMAT)

    Converts the *datetime_string* argument to a :class:`datetime.datetime` object.
