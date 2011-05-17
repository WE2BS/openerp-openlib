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

from __future__ import unicode_literals

from osv import osv, fields
from .. orm import ExtendedOsv

import pickle

class Config(osv.osv, ExtendedOsv):

    """
    This class simply defines a table in which you can store database-wide data. The data is automatically pickled.
    """

    _name = 'openlib.config'
    _columns = {
        'module' : fields.char('Module', size=255, required=True),
        'key' : fields.char('Key', size=255, required=True),
        'value' : fields.char('Value', size=255),
        'help' : fields.char('Help', size=255, readonly=True),
    }

Config()
