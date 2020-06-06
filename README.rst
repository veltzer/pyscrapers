============
*pyscrapers*
============

.. image:: https://img.shields.io/github/license/veltzer/pydmt   :alt: GitHub

![build](https://github.com/veltzer/pyscrapers/workflows/build/badge.svg)

project website: https://veltzer.github.io/pyscrapers

author: Mark Veltzer

version: 0.0.30

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

