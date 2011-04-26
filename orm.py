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
import logging

LOOKUPS_METHOD = ('exact', 'iexact', 'like', 'ilike', 'xmlid')

class Searcher(object):

    _last_search_pattern = None
    _last_search_ids = []

    def __init__(self, cursor, user_id, obj, context=None, **kwargs):

        """
        Constructs a search object call search if obj is specified.
        """

        self._cursor = cursor
        self._user_id = user_id
        self._obj = obj

        if obj:
            self.search(context, **kwargs)

    def __len__(self):

        """
        Returns the len of the last result returned by search().
        """
        
        return len(self._last_search_ids)

    def search(self, context=None, **kwargs):

        """
        Search objects of type "obj" based on the keywords attributes. 
        """

        obj_pool = pooler.get_pool(self._cursor.dbname).get(self._obj)
        obj_search_pattern = []

        if not obj_pool:
            raise osv.osv.except_osv('Error', 'Invalid object : %s' % obj)

        for keyword_name, keyword_value in kwargs.iteritems():

            # The keyword_name is of the form field__lookuptype, where field can contains multiple parts
            # separated by '_' to represent relations, like: partner_id__name__exact='Agrolait'.
            field_parts = keyword_name.split('__')
            if len(field_parts) == 1:
                field = field_parts[0]
                lookup = 'exact' # Default lookup
            else:
                if field_parts[-1] in LOOKUPS_METHOD:
                    # The last field part is a lookup method (like 'partner_id__name__ilike=')
                    field = '.'.join(field_parts[:-1])
                    lookup = field_parts[-1]
                else:
                    field = '.'.join(field_parts)
                    lookup = 'exact'

            if lookup == 'exact':
                obj_search_pattern.append((field, '=', keyword_value))
            elif lookup == 'iexact' or lookup == 'ilike':
                obj_search_pattern.append((field, 'ILIKE', keyword_value))
            elif lookup == 'like':
                obj_search_pattern.append((field, 'LIKE', keyword_value))
            elif lookup == 'xmlid':
                # This option improve the basic search method, and allow searching by XMLID
                # for related field. 'partner_id__xmlid' will be replaced by 'partner_id.id'
                # with the ID corresponding to the XML ID.
                module = False
                xmlid = keyword_value
                keyword_value_splitted = keyword_value.split('.')
                if len(keyword_value_splitted) > 1:
                    module = keyword_value_splitted[0]
                    xmlid = '.'.join(keyword_value_splitted[1:])
                search_data = Searcher(self._cursor, self._user_id, 'ir.model.data')
                if module:
                    result = search_data.search(module=module, name=xmlid).browse_one()
                else:
                    result = search_data.search(name=xmlid)
                    if len(result) > 1:
                        logging.warning('An XMLID search returned more than one result: %s' % xmlid)
                        logging.warning('Only the first one has been returned, please specify a module.')
                    result = result.browse_one()
                if result:
                    obj_search_pattern.append((field + '.id', '=', int(result.res_id)))
                else:
                    # We didn't find a corresponding XMLID in the DB.
                    raise ValueError("The XMLID '%s' doesn't exists." % xmlid)

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
        Returns the first element contained in the result, or None.
        """

        if not self._last_search_ids:
            return None
        if not context:
            context = self._context
        result = self._last_search_obj_pool.browse(
            self._cursor, self._user_id, self._last_search_ids[0], context=context)
        return result or None

    @property
    def ids(self):
        return self._last_search_ids
