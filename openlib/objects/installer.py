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

from osv import osv, fields
from .. orm import ExtendedOsv

class GithubInstaller(osv.osv_memory, ExtendedOsv):

    """
    A simple installer wizard for the github configuration.
    """

    def execute(self, cr, uid, ids, context=None):

        """
        Simply stores the Github login/token in the global config items if specified.
        """

        data = self.get(ids[0])
        pconfig = self.pool.get('openlib.config')

        if data.login and data.token:
            pconfig.set_value('openlib.github', 'GITHUB_USER', data.login)
            pconfig.set_value('openlib.github', 'GITHUB_TOKEN', data.token)

    def default_login(self, cr, uid, context=None):
        return self.pool.get('openlib.config').get_value('openlib.github', 'GITHUB_USER')

    def default_token(self, cr, uid, context=None):
        return self.pool.get('openlib.config').get_value('openlib.github', 'GITHUB_TOKEN')

    _name = 'openlib.github_installer'
    _inherit = 'res.config'
    
    _columns = {
        'login' : fields.char('Github Login', size=255),
        'token' : fields.char('Github Token', size=255),
        'url' : fields.char('Github URL', size=255, readonly=1),
    }

    _defaults = {
        'login' : default_login,
        'token' : default_token,
        'url' : 'http://github.com',
    }

GithubInstaller()
