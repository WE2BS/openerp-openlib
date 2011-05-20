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

Set global configuration variables
----------------------------------

A good practice is too create the key via an XML file, like this :

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

.. note ::

    Please not that values are string, you have to convert them manually.
