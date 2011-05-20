===============
OpenERP OpenLib
===============

You can download OpenLib on its github page : http://github.com/WE2BS/openerp-openlib

.. note ::
    This document refers to version |release|

-------------
ORM Extension
-------------

OpenLib provides an extension to the basic OpenERP ORM. Its main goal is to simplify everyday call to the OpenERP
API. For example, you don't have to pass the ``cr``, ``uid`` or ``context`` variables anymore. The ORM Extension
is not intrusive, you can enable it on your objects if you want, but it's not mandatory at all.

.. toctree ::
    :maxdepth: 2
    :numbered:

    orm

----------------------------
Github automatic bug reports
----------------------------

OpenLib integrates very well with GitHub and supports automatic bug reporting. This means that each time an exception
is raised in your code, OpenLib will check your github project and reports the bug it hasn't been reported.

Of course, this won't report any logical bugs (Like workflow errors, or "nothing happens" bugs), but code-related
bug will be reported, without any intervention from the user.

.. toctree ::
    :maxdepth: 2
    :numbered:

    github

--------------------
Global configuration
--------------------

OpenLib let you define global variables (database-wide) easily.

.. toctree ::
    :maxdepth: 2
    :numbered:

    config

----------
Misc tools
----------

Others tools provided by OpenLib.

.. toctree ::
    :maxdepth: 2
    :numbered:

    tools

------------------
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

