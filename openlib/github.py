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

import urllib
import httplib2
import inspect
import sys
import json
import logging
import traceback
import platform

import pooler

_logger = logging.getLogger('openlib.github')

# Github APIv2 URLs
API_URL = 'https://github.com/api/v2/json'
OPEN_ISSUES_URL = API_URL + '/issues/list/%s/%s/open'
CLOSED_ISSUES_URL = API_URL + '/issues/list/%s/%s/closed'
CREATE_ISSUE_URL = API_URL + '/issues/open/%s/%s'

# Exceptions to report
EXCEPTIONS = (
    BufferError, ArithmeticError, AssertionError, AttributeError, ImportError, LookupError,
    MemoryError, NameError, ReferenceError, RuntimeError, SyntaxError, TypeError, ValueError
)

# Message that will be posted into the issue
BUG_MESSAGE = """
Automatic bug report :

```
%(traceback)s
```

Platform: %(platform)s
Python Version: %(version)s
"""

def report_bugs(func):

    """
    This decorator can be used on any function to automatically report a bug on github when an error orccurs.
    """

    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
        except:

            if not wrapper.config['GITHUB_ENABLED'] or not wrapper.config['GITHUB_USER'] or not wrapper.config['GITHUB_REPO']:
                raise

            # We catch the exception and create a github issue if enabled
            type, value, tb = sys.exc_info()
            repo_user, repo_name = wrapper.config['GITHUB_USER'],  wrapper.config['GITHUB_REPO']

            # We ignore not builtins exceptions
            if not isinstance(value, EXCEPTIONS):
                raise

            # This http object will be used to make request to github
            h = httplib2.Http()

            _logger.exception('An exception occured, it will be reported to github.')
            _logger.info('Checking if the bug has already been reported...')

            source_function = tb.tb_next.tb_frame.f_code.co_name
            source_line = tb.tb_next.tb_lineno

            issue_title = '%s: %s (Line %d, %s)' % (type.__name__, value, source_line, source_function)
            issue_exception = '\n'.join(traceback.format_exception(type, value, tb))
            issue_message = BUG_MESSAGE % {
                'traceback' : issue_exception,
                'platform' : platform.platform(),
                'version' : platform.python_version(),
            }

            response, content = h.request(OPEN_ISSUES_URL % (repo_user, repo_name))
            response1, content1 = h.request(CLOSED_ISSUES_URL % (repo_user, repo_name))

            for r in (response, response1):
                if r.status != 200:
                    _logger.error('Unable to connect to github: %s' % str(response.human))
                    raise

            issues = json.loads(content)['issues']
            issues.extend(json.loads(content1)['issues'])

            for issue in issues:
                if issue['title'] == issue_title:
                    _logger.info('This bug has already been reported. Consult bug report here :')
                    _logger.info(issue['html_url'])
                    raise

            _logger.info('Bug not reported - Trying to report the bug on github: %s/%s',
                wrapper.config['GITHUB_USER'], wrapper.config['GITHUB_REPO'])

            # If we are here, we have to report the issue on github. First of all, we have to search
            # a cursor variable in the python stack, and a pooler, no matter where they are,
            # to be able to access the database and read the github user/password configuration of the database.
            current_frame = inspect.currentframe()
            cr, uid = None, 1
            for data in inspect.getouterframes(current_frame):
                if 'cr' in data[0].f_locals:
                    cr = data[0].f_locals['cr']
                elif 'cr' in data[0].f_globals:
                    cr = data[0].f_globals['cr']

            if not cr:
                _logger.warning('Unable to find a valid cursor in the Python stack. Aborting bug reporting.')
                raise

            pool = pooler.get_pool(cr.dbname)
            pool_config = pool.get('openlib.config')

            user = pool_config.get(module='openlib.github', key__iexact='GITHUB_USER')
            token = pool_config.get(module='openlib.github', key__iexact='GITHUB_TOKEN')

            if not user or not token:
                _logger.warning('Unable to report bug: You must configure a github username/token.')
                _logger.warning('Go to: Administraton->Customization->Variables to do this.')
                raise

            # Reports the bug
            resp, content = h.request(CREATE_ISSUE_URL % (repo_user, repo_name), method='POST', body=urllib.urlencode({
                'title':issue_title,
                'body':issue_message,
                'login' : user.value,
                'token' : token.value,
            }))

            if resp.status != 201:
                _logger.error('Error while reporting the bug on github: %s' % resp.human)
            else:
                data = json.loads(content)
                _logger.info('Bug reported here: %s' % data['issue']['html_url'])

            raise

        return result
    
    # We look for GITHUB_USER, GITHUB_REPO and GITHUB_DISABLED in global variables of the frame stack.
    # These variables defines where the report should be done. The inspection is done at loading.
    frames = inspect.getouterframes(inspect.currentframe())
    frames.reverse()

    config = {
        'GITHUB_USER' : None,
        'GITHUB_REPO' : None,
        'GITHUB_ENABLED' : False,
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
