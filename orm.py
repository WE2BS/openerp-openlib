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

import pooler
import osv

class Searcher(object):

    _last_search_pattern = None
    _last_search_ids = None

    def __init__(self, cursor, user_id, obj=None, context=None, **kwargs):

        """
        Constructs a search object call search if obj is specified.
        """

        self._cursor = cursor
        self._user_id = user_id

        if obj:
            self.search(obj, context, **kwargs)

    def search(self, obj, context=None, **kwargs):

        """
        Search objects of type "obj" based on the keywords attributes. 
        """

        obj_pool = pooler.get_pool(self._cursor.dbname).get(obj)
        obj_search_pattern = []

        if not obj_pool:
            raise osv.osv.except_osv('Error', 'Invalid object : %s' % obj)

        for keyword_name, keyword_value in kwargs.iteritems():

            try:
                field, lookup = keyword_name.split('__')
            except ValueError:
                field = keyword_name
                lookup = 'exact'

            if lookup == 'exact':
                obj_search_pattern.append((field, '=', keyword_value))
            elif lookup == 'iexact':
                obj_search_pattern.append((field, 'ILIKE', keyword_value))

        self._last_search_ids = obj_pool.search(self._cursor, self._user_id, obj_search_pattern, context=context)
        self._last_search_obj_pool = obj_pool
        self._last_search_pattern = obj_search_pattern
        self._context = context

        return self

    def browse(self, context=None):

        """
        Use browse() on the list opf ids previously get by search().     
        """

        if not self._last_search_ids:
            return []
        if not context:
            context = self._context
        return self._last_search_obj_pool.browse(self._cursor, self._user_id, self._last_search_ids, context=context)

    def browse_one(self, context=None):

        """
        Returns the first elements contained in the result, or None.     
        """

        if not self._last_search_ids:
            return None
        if not context:
            context = self._context
        result = self._last_search_obj_pool.browse(
            self._cursor, self._user_id, self._last_search_ids[0], context=context)
        return result or None
