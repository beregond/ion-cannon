Ion Cannon
==========

This software is simple http recorder able to record request at given port, and
later send these recorded request to target address. While sending original
relative url and headers are preserved.

Requirements
------------

You will need to have access to **MongoDB** database, preferably also
**invoke** installed (for automatizaton of deploy).

Installation
------------

All you need to do is:

.. code-block:: bash

    invoke deploy

And later fill in just created ``settings.py`` with proper data.

Usage
-----

To record incomming requests:

.. code-block:: bash

    python cannon.py reload

Optionally you can add ``--force`` if there are existing existing records, or
``--append`` to continue previous recording.

To send your requests to target (that is set in settings) just type:

.. code-block:: bash

    python cannon.py fire

To start Ion Cannon as proxy:

.. code-block:: bash

    python cannon.py tunnel

Just remember to set ``target`` in ``settings.py`` to forward requests.

You can use ``--force`` or ``--append`` options like described above.

Debug
-----

There is also ``monitor`` option to for debugging purpose. Just give proper
``port`` argument.

.. code-block:: bash

    python cannon.py monitor port

Help
----

To get help just type:

.. code-block:: bash

    python cannon.py help

Test
----

.. code-block:: bash

    invoke test
