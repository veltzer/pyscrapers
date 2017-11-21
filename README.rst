=======================
*pyscrapers* project by Mark Veltzer
=======================

What is it?
-----------

Scrapers for various stuff that I need off the web, maybe other people will like them too...:)

Currently supports downloading photos from the following sites:

- facebook
- instagram
- travelgirls
- vk
- mamba.ru

Installing
----------

You need python3 installed. Usually it is but if it isn't:

.. code-block:: bash

	$ sudo apt install python3

You also need pip3 installed.

.. code-block:: bash

	$ sudo apt install python3-pip

Now install pyscrapers:

.. code-block:: bash

	$ sudo -H pip3 install pyscrapers

Running
-------

.. code-block:: bash

	$ pyscrapers_photos --u [user_id] -t [type_of_site]

