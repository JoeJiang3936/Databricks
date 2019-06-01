Gene Sequencing with Apache Spark 
########################################

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









|pypi| |unix_build| |coverage| |gitter|



.. contents::

.. section-numbering::













Commands 
========





.. csv-table:: Standard Commands
   :header: "command", "purpose"
   :widths: 50, 50

   "show dbs", "show all databases"
   "use <db>", "select database to work with ......................"
   "show users", "list all users"
   "db.auth('username', 'password');", "authentication steps"
   "db.logout()", "log out from system"
   "show collections;",  "list out all collections"
   "db.getCollectionNames();", "list out all collections (2)"
   "db.<collectionName>.find();", "retreive all information"
   "db.<collectionName>.find().limit(10);", "retrieve but limit to 10 total"










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


Python version
--------------

Although Python 2.7 is supported as well, it is strongly recommended to
install HTTPie against the latest Python 3.x whenever possible. That will
ensure that some of the newer HTTP features, such as
`SNI (Server Name Indication)`_, work out of the box.
Python 3 is the default for Homebrew installations starting with version 0.9.4.
To see which version HTTPie uses, run ``http --debug``.


Unstable version
----------------

You can also install the latest unreleased development version directly from
the ``master`` branch on GitHub.  It is a work-in-progress of a future stable
release so the experience might be not as smooth.


.. class:: no-pdf

|unix_build|


On macOS you can install it with Homebrew:

.. code-block:: bash

    $ brew install httpie --HEAD


Otherwise with ``pip``:

.. code-block:: bash

    $ pip install --upgrade https://github.com/jakubroztocil/httpie/archive/master.tar.gz


Verify that now we have the
`current development version identifier <https://github.com/jakubroztocil/httpie/blob/0af6ae1be444588bbc4747124e073423151178a0/httpie/__init__.py#L5>`_
with the ``-dev`` suffix, for example:

.. code-block:: bash

    $ http --version
    1.0.0-dev




Apache Spark Background
===========

Core of this will be done with Apache Spark and SparkSQL 


.. code-block:: bash

    <common Apache Spark commands here>


SparkSQL differences such as  ``insert`` here:

.. code-block:: http

    DELETE /todos/7 HTTP/1.1


Insert more here







Request URL
===========

The only information HTTPie needs to perform a request is a URL.
The default scheme is, somewhat unsurprisingly, ``http://``,
and can be omitted from the argument – ``http example.org`` works just fine.


Querystring parameters
----------------------

If you find yourself manually constructing URLs with querystring parameters
on the terminal, you may appreciate the ``param==value`` syntax for appending
URL parameters. With that, you don't have to worry about escaping the ``&``
separators for your shell. Also, special characters in parameter values,
will also automatically escaped (HTTPie otherwise expects the URL to be
already escaped). To search for ``HTTPie logo`` on Google Images you could use
this command:

.. code-block:: bash

    $ http www.google.com search=='HTTPie logo' tbm==isch


.. code-block:: http

    GET /?search=HTTPie+logo&tbm=isch HTTP/1.1



URL shortcuts for ``localhost``
-------------------------------

Additionally, curl-like shorthand for localhost is supported.
This means that, for example ``:3000`` would expand to ``http://localhost:3000``
If the port is omitted, then port 80 is assumed.

.. code-block:: bash

    $ http :/foo


.. code-block:: http

    GET /foo HTTP/1.1
    Host: localhost


.. code-block:: bash

    $ http :3000/bar



.. code-block:: bash

    $ http :


.. code-block:: http

    GET / HTTP/1.1
    Host: localhost


Custom default scheme
---------------------

You can use the ``--default-scheme <URL_SCHEME>`` option to create
shortcuts for other protocols than HTTP:

.. code-block:: bash

    $ alias https='http --default-scheme=https'


Request items
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


Escaping rules
--------------

You can use ``\`` to escape characters that shouldn't be used as separators
(or parts thereof). For instance, ``foo\==bar`` will become a data key/value
pair (``foo=`` and ``bar``) instead of a URL parameter.

Often it is necessary to quote the values, e.g. ``foo='bar baz'``.

If any of the field names or headers starts with a minus
(e.g., ``-fieldname``), you need to place all such items after the special
token ``--`` to prevent confusion with ``--arguments``:

.. code-block:: bash

    $ http httpbin.org/post  --  -name-starting-with-dash=foo -Unusual-Header:bar

.. code-block:: http

    POST /post HTTP/1.1
    -Unusual-Header: bar
    Content-Type: application/json

    {
        "-name-starting-with-dash": "foo"
    }




Forms
=====

Submitting forms is very similar to sending `JSON`_ requests. Often the only
difference is in adding the ``--form, -f`` option, which ensures that
data fields are serialized as, and ``Content-Type`` is set to,
``application/x-www-form-urlencoded; charset=utf-8``. It is possible to make
form data the implicit content type instead of JSON
via the `config`_ file.


Regular forms
-------------

.. code-block:: bash

    $ http --form POST api.example.org/person/1 name='John Smith'


.. code-block:: http

    POST /person/1 HTTP/1.1
    Content-Type: application/x-www-form-urlencoded; charset=utf-8

    name=John+Smith


File upload forms
-----------------

If one or more file fields is present, the serialization and content type is
``multipart/form-data``:

.. code-block:: bash

    $ http -f POST example.com/jobs name='John Smith' cv@~/Documents/cv.pdf


The request above is the same as if the following HTML form were
submitted:

.. code-block:: html

    <form enctype="multipart/form-data" method="post" action="http://example.com/jobs">
        <input type="text" name="name" />
        <input type="file" name="cv" />
    </form>

Note that ``@`` is used to simulate a file upload form field, whereas
``=@`` just embeds the file content as a regular text field value.


HTTP headers
============

To set custom headers you can use the ``Header:Value`` notation:

.. code-block:: bash

    $ http example.org  User-Agent:Bacon/1.0  'Cookie:valued-visitor=yes;foo=bar'  \
        X-Foo:Bar  Referer:http://httpie.org/


.. code-block:: http

    GET / HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Cookie: valued-visitor=yes;foo=bar
    Host: example.org
    Referer: http://httpie.org/
    User-Agent: Bacon/1.0
    X-Foo: Bar


Default request headers
-----------------------

There are a couple of default headers that HTTPie sets:

.. code-block:: http

    GET / HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    User-Agent: HTTPie/<version>
    Host: <taken-from-URL>



Any of these except ``Host`` can be overwritten and some of them unset.





Reference
====

Interface design
----------------

The syntax of the command arguments closely corresponds to the actual HTTP
requests sent over the wire. It has the advantage  that it's easy to remember
and read. It is often possible to translate an HTTP request to an HTTPie
argument list just by inlining the request elements. For example, compare this
HTTP request:

.. code-block:: http

    hi
    its me
    hello 
    tom:  123




with the HTTPie command that sends it:







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


HTTPie friends
~~~~~~~~~~~~~~

HTTPie plays exceptionally well with the following tools:

* `jq <https://stedolan.github.io/jq/>`_
  — CLI JSON processor that
  works great in conjunction with HTTPie
* `http-prompt <https://github.com/eliangcs/http-prompt>`_
  —  interactive shell for HTTPie featuring autocomplete
  and command syntax highlighting







.. |pypi| image:: https://img.shields.io/pypi/v/httpie.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/httpie
    :alt: Latest version released on PyPi

.. |coverage| image:: https://img.shields.io/coveralls/jakubroztocil/httpie/master.svg?style=flat-square&label=coverage
    :target: https://coveralls.io/r/jakubroztocil/httpie?branch=master
    :alt: Test coverage

.. |unix_build| image:: https://img.shields.io/travis/jakubroztocil/httpie/master.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/jakubroztocil/httpie
    :alt: Build status of the master branch on Mac/Linux

.. |gitter| image:: https://img.shields.io/gitter/room/jkbrzt/httpie.svg?style=flat-square
    :target: https://gitter.im/jkbrzt/httpie
    :alt: Chat on Gitter