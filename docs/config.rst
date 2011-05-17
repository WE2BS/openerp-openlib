OpenLib Global Configuration
============================

OpenLib provides an easy way to store database configuration values, not related to any object. It's just a simple
table with key->value pairs. You can associate each key to a module.

Read global configuration variables
-----------------------------------

The *openlib.config* object inherits of :class:`openlib.orm.ExtendedOsv` so you can directly use the django-like
syntax to make search. Here is an example : ::

    variables = self.pool.get('openlib.config').filter(module='mymodule', key__startswith='MYMOD_')

    for key, value in [(config.key, config.value) for config in variables]:
        print key, value

Of course, you can use the :meth:`get` method to retrieve an element : ::

    value = self.pool.get('openlib.config').get(module='mymodule', key='MYMOD_KEY').value

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
