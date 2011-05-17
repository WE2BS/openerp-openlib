OpenERP OpenLib
===============

I've been working on the OpenERP framework for a year, and I realized that I repeat some tasks everyday. That's why
I decided to write OpenLib. Now, everytime I see something which could be simplified/improved, I add it to OpenLib.

Using OpenLib might add a small performance overhead (**very** small... you won't notice it in everyday use) , but you'll
get a more readable code. If you have critical parts in your code, you still can use basic OpenERP methods.

Modules provided by OpenLib :
    * :mod:`openlib.orm` - An extension to the OpenERP ORM
    * :mod:`openlib.tools` - Tools functions (like date manipulation)
    * :mod:`openlib.github` - Automatic github bug reports for your modules

Moreover, OpenLib add some objects to OpenERP :

    * :doc:`openlib.config <config>`  - A global configuration object, used to store database based variables.

Index
=====

.. toctree::

    orm
    tools
    config
    github

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

