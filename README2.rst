Gene Sequencing Data Processing with Apache Spark 
########################################

|

The following repo contains information assembled for our course project






.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/dna_rotating.gif
        :alt: HTTPie in action
        :width: 100%
        :align: center

.. class:: no-web no-pdf






.. class:: no-web



    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/tom2.gif
        :alt: HTTPie in action
        :width: 100%
        :align: right



.. class:: no-web no-pdf






.. contents::

.. section-numbering::





|


Our Approach
=============

* Research the basics of Apache Spark 
* Research pyspark and SparkSQL
* Get Apache Spark running on laptop (local mode)
* Understand how to baseline and monitor KPIs for local mode
* Get Apache Spark running, via Databricks (local mode)
* Baseline
* Get Apache Spark running, via Databricks (distributed compute mode!)
* Baseline
* Import small datasets
* Experiement with HDFS file type versions
* Push a beyond-TB sized sequence table to cluster
* Process the table via SparkSQL, etc
* Run 3rd-party app like Hail or some other crazy complex system on Databricks
* Push into cloud-hosted versions (AWS-like)
* Document the performance differences as you run these individual approaches
* I don't know, something like the above, none of us has Apache Spark experience


|



Background
==============

Apache Spark™ is a unified analytics engine for large-scale data processing.  Spark SQL is Apache Spark's module for working with structured data.
Spark appliations can be written in Java, Scala, R, Python, and SQL. For the purposes of this exercise we will primarily be focusing on Python and SQL approaches within Apache Spark. 

Our goal is to document how much more streamlined and efficient this system is for processing massive terabyte-sized DNA sequencing raw data, and demonstrate the usage of SparkSQL to query this datastructure. 



|













.. class:: no-web



    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/dna_rotating.gif
        :alt: HTTPie in action
        :width: 100%
        :align: center



.. class:: no-web no-pdf







User support
------------

Please check the following:

* `Click <http://portquiz.net:27017/>`_
  to confirm you can reach the right port for MongoDB and there is no firewall in play ! 

* `Our Gitter chat room <https://gitter.im/jkbrzt/httpie>`_
  to ask questions, discuss features, and for general discussion.
* `StackOverflow <https://stackoverflow.com>`_
  to ask questions (please make sure to use the
  `httpie <http://stackoverflow.com/questions/tagged/httpie>`_ tag).
* Tweet directly to `@clihttp <https://twitter.com/clihttp>`_.
* You can also tweet directly to `@jakubroztocil`_.


Related projects
----------------

Dependencies
~~~~~~~~~~~~

Under the hood, HTTPie uses these two amazing libraries:

* `Requests <http://python-requests.org>`_
  — Python HTTP library for humans






The How
============



steps
-----


On macOS, HTTPie can be installed via `Homebrew <http://brew.sh/>`_
(recommended):

.. code-block:: bash

    $ brew install httpie


A MacPorts *port* is also available:

.. code-block:: bash

    $ port install httpie




Windows, etc.
-------------

A universal installation method (that works on Windows, Mac OS X, Linux, …,
and always provides the latest version) is to use `pip`_:


.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade httpie


(If ``pip`` installation fails for some reason, you can try
``easy_install httpie`` as a fallback.)











Apache Spark Background
===========

Core of this will be done with Apache Spark and SparkSQL 


.. code-block:: bash

    <common Apache Spark commands here>


SparkSQL differences such as  ``insert`` here:

.. code-block:: http

    DELETE /todos/7 HTTP/1.1






|


JSON 
=============

There are a few different *request item* types that provide a
convenient mechanism for specifying HTTP headers, simple JSON and
form data, files, and URL parameters.

They are key/value pairs specified after the URL. All have in
common that they become part of the actual request that is sent and that
their type is distinguished only by the separator used:
``:``, ``=``, ``:=``, ``==``, ``@``, ``=@``, and ``:=@``. The ones with an
``@`` expect a file path as value.

+-----------------------+-----------------------------------------------------+
| Item Type             | Description                                         |
+=======================+=====================================================+
| HTTP Headers          | Arbitrary HTTP header, e.g. ``X-API-Token:123``.    |
| ``Name:Value``        |                                                     |
+-----------------------+-----------------------------------------------------+
| URL parameters        | Appends the given name/value pair as a query        |
| ``name==value``       | string parameter to the URL.                        |
|                       | The ``==`` separator is used.                       |
+-----------------------+-----------------------------------------------------+
| Data Fields           | Request data fields to be serialized as a JSON      |
| ``field=value``,      | object (default), or to be form-encoded             |
| ``field=@file.txt``   | (``--form, -f``).                                   |
+-----------------------+-----------------------------------------------------+
| Raw JSON fields       | Useful when sending JSON and one or                 |
| ``field:=json``,      | more fields need to be a ``Boolean``, ``Number``,   |
| ``field:=@file.json`` | nested ``Object``, or an ``Array``,  e.g.,          |
|                       | ``meals:='["ham","spam"]'`` or ``pies:=[1,2,3]``    |
|                       | (note the quotes).                                  |
+-----------------------+-----------------------------------------------------+
| Form File Fields      | Only available with ``--form, -f``.                 |
| ``field@/dir/file``   | For example ``screenshot@~/Pictures/img.png``.      |
|                       | The presence of a file field results                |
|                       | in a ``multipart/form-data`` request.               |
+-----------------------+-----------------------------------------------------+


Note that data fields aren't the only way to specify request data:
`Redirected input`_ is a mechanism for passing arbitrary request data.





|

Reference
=========

Apache Spark and Pyspark
------------------------

<insert>






User support
------------

Please use the following support channels:

* `GitHub issues <https://github.com/jkbr/httpie/issues>`_
  for bug reports and feature requests.
* `Our Gitter chat room <https://gitter.im/jkbrzt/httpie>`_
  to ask questions, discuss features, and for general discussion.
* `StackOverflow <https://stackoverflow.com>`_
  to ask questions (please make sure to use the
  `httpie <http://stackoverflow.com/questions/tagged/httpie>`_ tag).
* Tweet directly to `@clihttp <https://twitter.com/clihttp>`_.
* You can also tweet directly to `@jakubroztocil`_.


Related projects
----------------


Dependencies
~~~~~~~~~~~~

Under the hood, HTTPie uses these two amazing libraries:

* `Requests <http://python-requests.org>`_
  — Python HTTP library for humans
* `Pygments <http://pygments.org/>`_
  — Python syntax highlighter


