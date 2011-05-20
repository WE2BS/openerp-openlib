============================
OpenLib Global Configuration
============================

Sometimes, you need to store data not attached to a specific object, a kind of *Global variable*. OpenLib let you
do this with ``openlib.config`` object. This is a simple table with 3 columns, ``module``, ``key`` and ``value``.

This object implements the :class:`ExtendedOsv` interface, so it can be manipulated easily. Data are stored as charfield
and have maximum size of 255 characters. You can store pickled object, if you want.

------------------------
Access a global variable
------------------------

OpenLib uses this object internally to store Github credentials, for example, if you want to get the github login: ::

    login = self.pool.get('openlib.config').get(module='openlib.github', key='GITHUB_USER').value

This is the *normal* way, but ``openlib.config`` provides a method which returns ``None`` if the key is not defined: ::

    login = self.pool.get('openlib.config').get_value('openlib.github', 'GITHUB_USER')

.. note ::

    The second way it the safest, because it won't raise an ``AtributeError`` if the key is not defined.

-------------------------
Define a  global variable
-------------------------

~~~~~~~~~~~~~~~~
With an XML file
~~~~~~~~~~~~~~~~

You can easily create yours variables thanks to an XML file :

.. code-block:: xml

      <?xml version="1.0" encoding="utf-8"?>
      <openerp>
          <data>
              <record id="config_github_user" model="openlib.config">
                  <field name="module">openlig.github</field>
                  <field name="key">GITHUB_USER</field>
                  <field name="help">GitHub user account used to report bugs.</field>
              </record>
              <record id="config_github_token" model="openlib.config">
                  <field name="module">openlig.github</field>
                  <field name="key">GITHUB_TOKEN</field>
                  <field name="help">GitHub token associated to the account. Check your account settings.</field>
              </record>
          </data>
      </openerp>

You can provide a default value, just by adding :

.. code-block :: xml

    <field name="value">default_value</field>

Into the record.

~~~~~~~~~~~~~~~~
With Python code
~~~~~~~~~~~~~~~~

You can also update/create a configuration variable with Python. Like with when you access the variable, you have
two methods to do this : The *normal* way, and the shorter and recommended way :

Using write (normal way): ::

    self.pool.get('openlib.config').write(cr, uid, config_id, {'value' : 'XXXXX'}, context=context)

Using this method implies that you already know the ID of the global variable object. If it does not exists,
you have to create it with the :meth:`create` method. To make your life simpler, OpenLib provides a ``set_value`` method: ::

    self.pool.get('openlib.config').set_value('openlib.github', 'GITHUB_USER', 'XXXXX)

This method will create the entry if it doesn't exist, and update it if it does.
