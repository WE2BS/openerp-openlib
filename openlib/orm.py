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

from inspect import currentframe, getouterframes
from datetime import datetime, date, time

from . tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_TIME_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

__all__ = ['Q', 'ExtendedOsv']

class Q(object):

    """
    This class represents a *search criteria*. You can combine Q objects using operators like *&* and *|* to create
    complex expressions. Internally, OpenLib converts these Q objects to the polish notation used by OpenERP.
    """

    def __init__(self, *args, **kwargs):

        self._search_list = ['&']
        self.parse(**kwargs)

    def __or__(self, other):

        """
        Combine two Q object with a | and returns a new Q object.
        """

        if not isinstance(other, Q):
            raise TypeError('You only can use | with other Q objects.')

        new_q = Q()
        new_q._search_list = self._join_search_list('|', other._search_list)

        return new_q

    def __and__(self, other):

        """
        Combine two Q object with a & and returns a new Q object.
        """

        if not isinstance(other, Q):
            raise TypeError('You only can use & with other Q objects.')

        new_q = Q()
        new_q._search_list = self._join_search_list('&', other._search_list)

        return new_q

    def __neg__(self):

        """
        Returns the negation of the condition: -Q(name='Thibaut') means that name IS NOT Thibaut.
        """

        self._search_list.insert(0, '!')
        return self

    def _join_search_list(self, operator, other_list):

        """
        Combine the object search list with the one passed as argument :
            ['&', '&', a, b, c] or'ed with ['&', d, e]
        become :
            ['|', '&', '&', '&', a, b ,c , d ,e]
        """

        result = [operator]
        tuples = []
        for item in self._search_list + other_list:
            if item in ('&', '|'):
                result.append(item)
            else:
                tuples.append(item)
        result.extend(tuples)
        
        return result

    def _like_protect(self, string, escape_char='\\'):

        """
        Returns the string protected for use with LIKE/ILIKE.
        """

        res = string.replace(escape_char, escape_char*2)
        res = res.replace('_', '%s_' % escape_char)
        res = res.replace('%', '%s%%' % escape_char)
        
        return res

    @property
    def search_list(self):

        """
        Returns a formatted search list usable by OpenERP search() method, if you want to use Q objects with search().
        """

        return self._search_list

    def parse(self, **kwargs):

        """
        Parses the arguments of the Q object to create the final search tuple used by OpenERP. Keyword args should
        be of the form <name>__<lookup-type> where lookup-type is one of the following value :

            exact, iexact, like, ilike, gt, lt, ge, le, startswith, endswith, contains

        If no lookup-type is specified, 'exact' is used by default. Please not that you have to specify the lookup
        method for relational search: partner__age is not valid, but partner__age__exact is. This restriction avoid
        confusion if you have a column with the same name than a lookup method.
        """

        if not kwargs:
            self._search_list = []
            return

        for kwarg, value in kwargs.iteritems():

            # If kwarg name is composed of multiple '__' like 'partner__age__gt', we remplace the '__' by points :
            # name = partner.age, lookup = 'gt'. This will allow relationship query.
            kwarg_splitted = kwarg.split('__')

            if len(kwarg_splitted) > 1:
                if kwarg_splitted[-1] in ('exact', 'iexact', 'like', 'ilike', 'gt', 'lt', 'ge', 'le', 'startswith',
                                          'istartswith', 'endswith', 'iendswith', 'contains', 'icontains'):
                    # If the last element is a lookup name, we use it -- WARNING: This means that if a column
                    # have the same name than a lookup type, you must repeat it !
                    name, lookup = '.'.join(kwarg_splitted[:-1]), kwarg_splitted[-1]
                else:
                    name, lookup = '.'.join(kwarg_splitted), 'exact'
            else:
                name, lookup = kwarg, 'exact'

            if isinstance(value, datetime):
                value = value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            elif isinstance(value, date):
                value = value.strftime(DEFAULT_SERVER_DATE_FORMAT)
            elif isinstance(value, time):
                value = value.strftime(DEFAULT_SERVER_TIME_FORMAT)

            # Convertions between Q lookup methods and OpenERP methods
            if lookup == 'exact':
                openerp_lookup = '='
            elif lookup == 'iexact':
                value, openerp_lookup = self._like_protect(value), 'ilike'
            elif lookup in ('like', 'ilike'):
                openerp_lookup = lookup
            elif lookup == 'gt':
                openerp_lookup = '>'
            elif lookup == 'lt':
                openerp_lookup = '<'
            elif lookup == 'ge':
                openerp_lookup = '>='
            elif lookup == 'le':
                openerp_lookup = '<='
            elif lookup in ('startswith', 'istartswith'):
                value, openerp_lookup = self._like_protect(value) + '%', 'like' if lookup == 'startswith' else 'ilike'
            elif lookup in ('endswith', 'iendswith'):
                value, openerp_lookup = '%' + self._like_protect(value), 'like' if lookup == 'endswith' else 'ilike'
            elif lookup in ('contains', 'icontains'):
                value, openerp_lookup = '%' + self._like_protect(value) + '%', 'like' if lookup == 'contains' else 'ilike'
            else:
                raise NotImplementedError('The lookup method %s is not implemented.' % lookup)

            # We remove the implicit '&' and set it manually every 2 tuples
            if len(self._search_list) > 2 and len(self._search_list) % 3 == 0:
                self._search_list.insert(0, '&')
            self._search_list.append((name, openerp_lookup, value))

        # If we have only 1 value, we remove the '&' from the search list, because it will cause
        # problems when combining Q objects.
        if len(self._search_list) == 2:
            del self._search_list[0]

class ExtendedOsv(object):

    """
    This class adds some functionalities to the OpenERP ORM :
        - The find() method, a search-like method with support for Q objects.
        - The filter() method, a search-and-browse which supports Q objects.
        - The get() method, a search-and-browse which returns only one object. Supports XMLID search.
        - The xmlid_to_id method()
        - The get_pools() method.
    """

    def _get_cr_uid_context(self):

        """
        Returns a 3-tuple containing the cursor, user id and context thanks to introspection.
        """

        cr, uid, context = None, None, None

        for frame_no, data in enumerate(getouterframes(currentframe())):

            frame = data[0]

            if frame_no == 1:
                # We check if their are _cr, _uid and _context variables only in the direct parent
                # frame in the case this method is called from get, filter or any other ExtendedOsv method.
                if '_cr' in frame.f_locals:
                    cr = frame.f_locals['_cr']
                if '_uid' in frame.f_locals:
                    uid = frame.f_locals['_uid']
                if '_context' in frame.f_locals:
                    context = frame.f_locals['_context']
            else:
                if not cr and 'cr' in frame.f_locals:
                    cr = frame.f_locals['cr']
                if not uid and 'uid' in frame.f_locals:
                    uid = frame.f_locals['uid']
                if not context and 'context' in frame.f_locals:
                    context = frame.f_locals['context']

            if cr and uid:
                break # We stop at the first cr/uid we find

        if not cr or not uid:
            raise RuntimeError('Unable to get the "cr" or "uid" variables from the frame stack.')
            
        return cr, uid, context

    def _get_pool(self, object=None):

        """
        Returns a valid pool that can be used by ExtendedOsv methods :
        If object is None, returns the pool associated to self. Else, returns the object's pool.
        """

        if object:
            pool = self.pool.get(object)
        else:
            pool = self
        if not pool:
            raise ValueError("Unable to get pool for object '%s', does it exist ?" % object)
        return pool

    def xmlid_to_id(self, cr, uid, xmlid, context=None):

        """
        Returns the ID corresponding to the XMLID or None.
        """

        xmlid_splitted = xmlid.split('.')
        modeldata = self.pool.get('ir.model.data')

        try:
            xmlid = '.'.join(xmlid_splitted[1:])
            module = xmlid_splitted[0]
            search = [('name', '=', xmlid), ('module', '=', module)]
        except IndexError:
            search = [('name', '=', xmlid)]

        model_data_ids = modeldata.search(cr, uid, search, context=context)

        if not model_data_ids:
            return None
        
        return modeldata.browse(cr, uid, model_data_ids[0], context=context).res_id

    def find(self, q=None, _object=None, _cr=None, _uid=None, _context=None, _offset=0,
             _limit=None, _order=None, _count=None,  **kwargs):

        """
        This method uses either Q objects direcly, or create a Q object based on its kwargs :
            self.find(name='Thibaut', age=31)
            self.find(Q(name='Thibaut') & Q(age=31))
        The cursor, user id and context are found using inspection, unless manually specified.

        Returns a list of ids, like search() does.
        """

        pool = self._get_pool(_object)
        cr, uid, context = self._get_cr_uid_context()

        if not q:
            q = Q(**kwargs)

        ids = pool.search(cr, uid, q._search_list, offset=_offset, limit=_limit,
            order=_order, context=context, count=_count)
        
        return ids

    def filter(self, value=None, _object=None, _cr=None, _uid=None, _context=None, **kwargs):

        """
        This method is like a "search & browse" method. You can get objects based on search criteria
        (Q object or kwargs) or on their ids. If you specify ids, search criteria are ignored.

        Using search criteria will call find() and return the result of browse().
        """

        pool = self._get_pool(_object)
        cr, uid, context = self._get_cr_uid_context()

        if value:
            try:
                iter(value)
            except TypeError:
                # If we can't iterate on the value, it's not considered as a list of ids
                if not isinstance(value, Q):
                    raise RuntimeError('You must use filter() on Q objects or ids.')
                q = value
            else:
                # It's a list of ids, so we just browse() on it.
                return pool.browse(cr, uid, value, context=context)
        else:
            q = Q(**kwargs)

        return pool.browse(cr, uid, self.find(q, _object=_object), context=context)

    def get(self, value=None, _object=None, _cr=None, _uid=None, _context=None, **kwargs):

        """
        This method returns one object corresponding to the search criteria :
             - If value is an integer, the object with this id is returned.
             - If value is a string, the object with this XMLID is returned.
             - If value is not specified, a search is done using the kwargs, and the first result is returned.
        Returns None if no object is found.
        """

        pool = self._get_pool(_object)
        cr, uid, context = self._get_cr_uid_context()

        if isinstance(value, (int, long)):
            return pool.browse(cr, uid, value, context=context)

        if isinstance(value, basestring):
            xmlid = self.xmlid_to_id(cr, uid, value, context)
            if not xmlid:
                return None
            return pool.browse(cr, uid, xmlid, context=context)

        try:
            # If the value is not an int or a string, it should be either a Q object or None. In this case, we do
            # a find with limit=1 and we return the object or None.
            res_id = self.find(value, _object=_object, _cr=_cr, _uid=_uid, _context=_context, _limit=1, **kwargs)[0]
            return pool.browse(cr, uid, res_id, context=context)
        except IndexError:
            return None

    def get_pools(self, *args):

        """
        Returns a list of objects corresponding to the OpenERP passed as argument.     
        """

        if args:
            return map(self.pool.get, args)
        return self.pool.get(args[0])
