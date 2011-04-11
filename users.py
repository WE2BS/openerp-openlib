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

from osv import osv, fields
from tools.translate import _
from tools.misc import DEFAULT_SERVER_DATE_FORMAT

from . orm import Searcher

def get_user_lang(cursor, user_id, context=None):

    """
    Returns the date format used by the user language.
    """

    user_pool = pooler.get_pool(cursor.dbname).get('res.users')
    user = user_pool.browse(cursor, user_id, user_id)

    if not user:
        raise osv.except_osv(_('Error'), _("Can't find a user corresponding to ID %d." % user_id))

    search = Searcher(cursor, user_id, 'res.lang', context=context, code=user.context_lang)

    return search.browse_one()

