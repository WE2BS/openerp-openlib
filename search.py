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
import logging

logger = logging.getLogger('openlib.orm')

class Q(object):

    """
    This class represents an abstract query and let you combine search options. Query objects can be combined
    using operator | and &. Combinations return a Query object, which can be combined again.

    Examples:
        query = Q(name__startswith='T', firstname='Thibaut') | Q(age__gt=31)
    """

    def __init__(self, *args, **kwargs):

        self._search_list = ['&']
        self.parse(**kwargs)

    def __or__(self, other):

        """
        Combine to Q object with a | and returns a new Q object.
        """

        if not isinstance(other, Q):
            raise TypeError('You only can use | with other Q objects.')

        new_q = Q()
        new_q._search_list = self._join_search_list('|', other._search_list)

        return new_q

    def __and__(self, other):

        """
        Combine to Q object with a & and returns a new Q object.
        """

        if not isinstance(other, Q):
            raise TypeError('You only can use & with other Q objects.')

        new_q = Q()
        new_q._search_list = self._join_search_list('&', other._search_list)

        return new_q

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

        return string.replace('_', '%s_' % escape_char)\
            .replace('%', '%s%%' % escape_char).replace(escape_char, escape_char*2)

    @property
    def search_list(self):
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

        for kwarg, value in kwargs.iteritems():

            # If kwarg name is composed of multiple '__' like 'partner__age__gt', we remplace the '__' by points :
            # name = partner.age, lookup = 'gt'. This will allow relationship query.
            kwarg_splitted = kwarg.split('__')
            if len(kwarg_splitted) > 1:
                name, lookup = '.'.join(kwarg_splitted[:-1]), kwarg_splitted[-1]
            else:
                name, lookup = kwarg, 'exact'

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


if __name__ == '__main__':
    
    q0 = Q(name='Thibaut')
    print(q0.search_list)

