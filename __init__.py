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

import inspect

from . partner import *
from . orm import *
from . localtools import *
from . search import Q

from osv import osv, fields

def test():
    current = inspect.currentframe()
    for data in inspect.getouterframes(current):
        print data[0].f_locals

class DemoObject(osv.osv):

    _name = 'openlib.demo'
    _columns = {
        'name' : fields.char('Name', size=12),
        'number' : fields.integer(),
        'text' : fields.text(),
        'number1' : fields.integer(),
    }

    def run_demo(self, cr, uid, ids, context=None):
        q = Q(name='lol', number=1, text__contains='Hi') | Q(number1=15)
        q = q & Q(number1=17)
        self.search(cr, uid, q.search_list)
    
DemoObject()
