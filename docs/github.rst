OpenLib Github Integration
==========================

.. module:: openlib.github
    :synopsis: Github automatic bug reporting.
.. currentmodule:: openlib.github

OpenLib provides an easy way to automatically report bugs which happen in your modules on github. You have to configure
the github repository you want to report bugs on, and it will work.

Github module configuration
---------------------------

For the example, we will imagine you are writing a module named ``example``, hosted in a github repository named
``openerp-example`` by the organization ``orga``. You just have to add three variables to your module's ``__init__.py`` : ::

    GITHUB_ENABLED = True
    GITHUB_REPO = 'openerp-example'
    GITHUB_USER = 'orga'

.. note::

    Setting ``GITHUB_ENABLED`` to ``False`` will disable github bug reporting. Remember to unset it during developpement.

Define the functions you want to watch
--------------------------------------

OpenLib can't watch all your module's method. You must tell it the one you want to watch. To do this, you just have
to import the :func:`report_bugs` function for :mod:`openlib.github` : ::

    from openlib.github import report_bugs

    class MyObject(osv.osv):

        @report_bugs
        def on_change_product(...):
            ...

Each time an exception is raised in this method, OpenLib will check if it has already been reported. If it's not the case,
a new issue will be opened on the github project you specified in ``__init__.py``.

.. note::

    Using this decorator on a lot of functions won't cause any performance problem. The only overhead is a ``try .. except``
    block around your method call, you won't see the difference.

Define the account used to report bugs
--------------------------------------

To be able to report bugs, you must have a GitHub account. This configuration is done by database, and must be set
by the administrator into the menu *Administration->Customization->Variables*. There are two variables, named
``GITHUB_USER`` and ``GITHUB_TOKEN`` you must fill.

You can find you token on your github account settings : *Account settings->Account admin->API Token*.

.. note ::

    OpenLib provides an installation wizard which does that automatically.
