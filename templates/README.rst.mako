=======================
*pyscrapers* project by ${tdefs.personal_fullname}
=======================

What is it?
-----------

Scrapers for various stuff that I need off the web, maybe other people will like them too...:)

Currently supports downloading photos from the following sites:

% for a in tdefs.types:
- ${a}
% endfor

Installing
----------

Clone the repo

.. code-block:: bash

	$ git clone https://github.com/veltzer/pyscrapers.git

You need python3 installed. Usually it is but if it isn't:

.. code-block:: bash

	$ sudo apt install python3

or

.. code-block:: bash
	$ sudo yum install python3

Install requirements using:

.. code-block:: bash

	$ pip3 install --upgrade -r requirements.txt

Running
-------

.. code-block:: bash

	$ pyscrapers_photos --u [user_id] -t [type_of_site]

