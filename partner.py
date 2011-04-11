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

def get_partner_lang(cursor, user_id, partner, context=None):

    """
    Returns the res.lang object associated to the specified partner (id or browse result).
    """

    if isinstance(partner, int):
        partner_pool = pooler.get_pool(cursor.dbname).get('res.partner')
        partner = partner_pool.browse(cursor, user_id, partner_id)
        if not partner:
            raise osv.except_osv(_('Error'), _("Can't find a partner corresponding to ID %d." % partner_id))

    search = Searcher(cursor, user_id, 'res.lang', context=context, code=partner.lang)

    return search.browse_one()

