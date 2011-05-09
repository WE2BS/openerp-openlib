This library has been developped to simplify some tasks when working with the OpenObject framework.

ORM Extention
=============

OpenLib provides an extension to the OpenERP basic ORM and adds 4 methods :

    * xmlid_to_id()
    * find()
    * filter()
    * get()

Moreover, OpenLib adds a 'Q' object, which can be used to manipulate search criteria. The three main methods uses
introspection to get the 'cr', 'uid' and 'context' variables automatically, so you don't have to pass it.

To illustrate this, here is an example of a method called by OpenERP when pressing a button ::

    def on_button_clicked(self, cr, uid, ids, context=None):
        for object in self.filter(ids):
            print object.name

As you can see in this example, we don't have to pass any cr, uid or context. Let's extend this example and make
some search on partners throught the filter() API ::

    partners = self.filter(name__startswith='A', _object='res.partners')

The *partners* variable will contain all the partners which name starts with the letter 'A'. As before, we didn't use
the cr, uid or context variable. You can see that we used a _object argument to specify the object. That's because
OpenERP object doesn't supports the ExtendedOsv extension, and I didn't want to monkey patch the code. So, if you want
to use the OpenLib features on basic OpenERP objects, you have to use _objects.

Now, let's use a more complicated query, with OR, AND en NOT ::

    partners = self.filter(
        (Q(name__startswith='A') & Q(country_id__code='fr')) | Q(name='Agrolait'), _objects='res.partner')

This example show you the power of the Q objects. Internally, OpenLib converts this into polish notation,
like in search(). This examples will return partners whose (name starts with 'A' AND country is fr) OR name is agrolait.

If you want to get only one object, you can use the get() method ::

    agrolait = self.get(name='Agrolait', _object='res.partner')

The get() method let you retrieve objects from their XMLID ::

    group_stock = self.get('stock.group_stock_user', _object='res.group')

Or their ID::

    obj = self.get(15)
