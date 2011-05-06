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

from __future__ import unicode_literals, print_function

import inspect

class Search(object):

    """
    This class is an helper to the OpenObject search/browse methods. Is uses auto-inspection to avoid passing
    recurrent arguments like cursor, user id and context to each calls. Its syntax is easier but less powerful than
    the manual syntax used in search(). Anyway, it covers most of the usual cases.

    When you initialize this object, it will get the cursor, user id and context from the current execution
    context and store it. Each method will use the stored values, unless you explicitly uses others.

    Search objects are lazy, and the real query is executed only when you use search(), get() or len().

    Get the first object corresponding to a search :
        agrolait = Search('res.partners', name='Agrolait').get()

    Get a list of elements corresponding to a search :
        partners = Search('res.partners', phone__startswith='+33')

    You can combine conditions easily :
        partners = Search('res.partners', name__startswith='T').or(name='Paul')
        Correspond to: ['|', '&', ('name', 'ilike', 'T%'), ('name', '=', 'Paul')]
    """
