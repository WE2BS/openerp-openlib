# -*- encoding: utf-8 -*-
#
# OpenLib - A simple and easy to use OpenObject library for OpenERP
# Copyright (C) 2010-2011 Thibaut DIRLIK <thibaut.dirlik@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__all__ = ['to_date', 'to_time', 'to_datetime']

# We could have import this from OpenERP, but the docs couldn't have been built without OpenERP
# installed. Moreover, until the 6.1, we can't import from openerp.* which causes conflicts.
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT)

from datetime import datetime

def to_date(date_string, format=DEFAULT_SERVER_DATE_FORMAT):

    """
    Converts a date string to a datetime.date object.
    """

    return datetime.strptime(date_string, format).date()

def to_time(time_string, format=DEFAULT_SERVER_TIME_FORMAT):

    """
    Converts a time string to a tome object.
    """

    return datetime.strptime(time_string, format).time()

def to_datetime(datetime_string, format=DEFAULT_SERVER_DATETIME_FORMAT):

    """
    Converts a datetime string to a datetime.datetime object.
    """
    
    return datetime.strptime(datetime_string, format)

