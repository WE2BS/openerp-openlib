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

import urllib2, urllib
import inspect
import sys
import json
import logging
import traceback

API_URL = 'https://api.github.com/repos/%s/%s/issues/'

_logger = logging.getLogger('openlib.github')

def report_bugs(func):

    """
    This decorator can be used on any function to automatically report a bug on github when an error orccurs.
    """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except:
            if wrapper.config['GITHUB_ENABLED'] and wrapper.config['GITHUB_USER'] and wrapper.config['GITHUB_REPO']:
                # We catch the exception and create a github issue if enabled
                type, value, tb = sys.exc_info()

                # We have to check that an issue with this name doesn't already exist. The name of the issue is
                # the exception string + file name and line number.
                name = "%s: %s (Line %d, in %s)" % (type.__name__, value, tb.tb_next.tb_lineno,
                    tb.tb_next.tb_frame.f_code.co_name)
                error = False
                url = API_URL % (wrapper.config['GITHUB_USER'], wrapper.config['GITHUB_REPO'])

                # Get a list of issues and check if our issue exists.
                try:
                    data = urllib2.urlopen(url)
                    issues = json.load(data)
                except (urllib2.URLError, urllib2.HTTPError):
                    error = True
                    _logger.exception('Unable to get a list of existing issues on github. Skipping issue report.')

                if error: # If we can't connect to github, we just raise the initial exception
                    raise

                for issue in issues:
                    if issue['title'] == name:
                        _logger.warning("Bug won't reported on github, an issue with the same name exists :")
                        _logger.warning(issue['url'])
                        raise # We stop here and raise the initial exception

                # Else, we will post the issue on github !
                data = {
                    'title' : name,
                    'body' : json.dumps('\n'.join(traceback.format_tb(tb))),
                }
                auth_handler = urllib2.HTTPBasicAuthHandler()
                auth_handler.add_password(None, 'api.github.com', 'thibautd', 'XXX')
                urllib2.install_opener(urllib2.build_opener(auth_handler))
                urllib2.urlopen(url, urllib.urlencode(data))

            raise
        return result
    
    # We look for GITHUB_USER, GITHUB_REPO and GITHUB_DISABLED in global variables of the frame stack.
    # These variables defines where the report should be done. The inspection is done at loading.
    frames = inspect.getouterframes(inspect.currentframe())
    frames.reverse()

    config = {
        'GITHUB_USER' : None,
        'GITHUB_REPO' : None,
        'GITHUB_ENABLED' : True,
    }

    for data in frames:
        for varname in config.keys():
            if varname in data[0].f_locals:
                config[varname] = data[0].f_locals[varname]
            elif varname in data[0].f_globals:
                config[varname] = data[0].f_globals[varname]

    # We save the config into the wrapper, to let him acces it later
    wrapper.config = config
    
    return wrapper
