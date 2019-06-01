MongoDB:  Databases for real humans 
########################################

HTTPie (pronounced *aitch-tee-tee-pie*) is a command line HTTP client.
Its goal is to make CLI interaction with web services as human-friendly
as possible. It provides a simple ``http`` command that allows for sending
arbitrary HTTP requests using a simple and natural syntax, and displays
colorized output. 






.. class:: no-web


    .. image:: https://raw.githubusercontent.com/jakubroztocil/httpie/master/httpie.png
        :alt: HTTPie compared to cURL
        :width: 100%
        :align: center



    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/tom2.gif
        :alt: HTTPie in action
        :width: 100%
        :align: center





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




https://stackoverflow.com/questions/17489789/why-do-i-get-a-pymongo-cursor-cursor-when-trying-to-query-my-mongodb-db-via-pymo




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





Main features
=============

* Expressive and intuitive syntax
* Formatted and colorized terminal output
* Built-in JSON support
* Forms and file uploads
* HTTPS, proxies, and authentication





Installation
============



macOS
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


Usage
=====


Hello World:


.. code-block:: bash

    $ http httpie.org


Synopsis:

.. code-block:: bash

    $ http [flags] [METHOD] URL [ITEM [ITEM]]


See also ``http --help``.


Examples
--------

Custom `HTTP method`_, `HTTP headers`_ and `JSON`_ data:

.. code-block:: bash

    $ http PUT example.org X-API-Token:123 name=John


Submitting `forms`_:

.. code-block:: bash

    $ http -f POST example.org hello=World


See the request that is being sent using one of the `output options`_:

.. code-block:: bash

    $ http -v example.org


Use `Github API`_ to post a comment on an
`issue <https://github.com/jakubroztocil/httpie/issues/83>`_
with `authentication`_:

.. code-block:: bash

    $ http -a USERNAME POST https://api.github.com/repos/jakubroztocil/httpie/issues/83/comments body='HTTPie is awesome! :heart:'


Upload a file using `redirected input`_:

.. code-block:: bash

    $ http example.org < file.json


Download a file and save it via `redirected output`_:

.. code-block:: bash

    $ http example.org/file > file


Download a file ``wget`` style:

.. code-block:: bash

    $ http --download example.org/file

Use named `sessions`_ to make certain aspects or the communication persistent
between requests to the same host:

.. code-block:: bash

    $ http --session=logged-in -a username:password httpbin.org/get API-Key:123

    $ http --session=logged-in httpbin.org/headers


Set a custom ``Host`` header to work around missing DNS records:

.. code-block:: bash

    $ http localhost:8000 Host:example.com

..


HTTP method
===========

The name of the HTTP method comes right before the URL argument:

.. code-block:: bash

    $ http DELETE example.org/todos/7


Which looks similar to the actual ``Request-Line`` that is sent:

.. code-block:: http

    DELETE /todos/7 HTTP/1.1


When the ``METHOD`` argument is omitted from the command, HTTPie defaults to
either ``GET`` (with no request data) or ``POST`` (with request data).


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


.. code-block:: http

    GET /bar HTTP/1.1
    Host: localhost:3000


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



JSON
====

JSON is the *lingua franca* of modern web services and it is also the
**implicit content type** HTTPie uses by default.


Simple example:

.. code-block:: bash

    $ http PUT example.org name=John email=john@example.org

.. code-block:: http

    PUT / HTTP/1.1
    Accept: application/json, */*
    Accept-Encoding: gzip, deflate
    Content-Type: application/json
    Host: example.org

    {
        "name": "John",
        "email": "john@example.org"
    }


Default behaviour
-----------------


If your command includes some data `request items`_, they are serialized as a JSON
object by default. HTTPie also automatically sets the following headers,
both of which can be overwritten:

================    =======================================
``Content-Type``    ``application/json``
``Accept``          ``application/json, */*``
================    =======================================


Explicit JSON
-------------

You can use ``--json, -j`` to explicitly set ``Accept``
to ``application/json`` regardless of whether you are sending data
(it's a shortcut for setting the header via the usual header notation:
``http url Accept:'application/json, */*'``). Additionally,
HTTPie will try to detect JSON responses even when the
``Content-Type`` is incorrectly ``text/plain`` or unknown.



Non-string JSON fields
----------------------

Non-string fields use the ``:=`` separator, which allows you to embed raw JSON
into the resulting object. Text and raw JSON files can also be embedded into
fields using ``=@`` and ``:=@``:

.. code-block:: bash

    $ http PUT api.example.com/person/1 \
        name=John \
        age:=29 married:=false hobbies:='["http", "pies"]' \  # Raw JSON
        description=@about-john.txt \   # Embed text file
        bookmarks:=@bookmarks.json      # Embed JSON file


.. code-block:: http

    PUT /person/1 HTTP/1.1
    Accept: application/json, */*
    Content-Type: application/json
    Host: api.example.com

    {
        "age": 29,
        "hobbies": [
            "http",
            "pies"
        ],
        "description": "John is a nice guy who likes pies.",
        "married": false,
        "name": "John",
        "bookmarks": {
            "HTTPie": "http://httpie.org",
        }
    }


Please note that with this syntax the command gets unwieldy when sending
complex data. In that case it's always better to use `redirected input`_:

.. code-block:: bash

    $ http POST api.example.com/person/1 < person.json


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



Cookies
=======

HTTP clients send cookies to the server as regular `HTTP headers`_. That means,
HTTPie does not offer any special syntax for specifying cookies — the usual
``Header:Value`` notation is used:


Send a single cookie:

.. code-block:: bash

    $ http example.org Cookie:sessionid=foo

.. code-block:: http

    GET / HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Cookie: sessionid=foo
    Host: example.org
    User-Agent: HTTPie/0.9.9


Send multiple cookies
(note the header is quoted to prevent the shell from interpreting the ``;``):

.. code-block:: bash

    $ http example.org 'Cookie:sessionid=foo;another-cookie=bar'

.. code-block:: http

    GET / HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Cookie: sessionid=foo;another-cookie=bar
    Host: example.org
    User-Agent: HTTPie/0.9.9


If you often deal with cookies in your requests, then chances are you'd appreciate
the `sessions`_ feature.


Authentication
==============

The currently supported authentication schemes are Basic and Digest
(see `auth plugins`_ for more). There are two flags that control authentication:

===================     ======================================================
``--auth, -a``          Pass a ``username:password`` pair as
                        the argument. Or, if you only specify a username
                        (``-a username``), you'll be prompted for
                        the password before the request is sent.
                        To send an empty password, pass ``username:``.
                        The ``username:password@hostname`` URL syntax is
                        supported as well (but credentials passed via ``-a``
                        have higher priority).

``--auth-type, -A``     Specify the auth mechanism. Possible values are
                        ``basic`` and ``digest``. The default value is
                        ``basic`` so it can often be omitted.
===================     ======================================================



Password prompt
---------------

.. code-block:: bash

    $ http -a username example.org


``.netrc``
----------

Authentication information from your ``~/.netrc`` file is honored as well:

.. code-block:: bash

    $ cat ~/.netrc
    machine httpbin.org
    login httpie
    password test

    $ http httpbin.org/basic-auth/httpie/test
    HTTP/1.1 200 OK
    [...]


Auth plugins
------------

Additional authentication mechanism can be installed as plugins.
They can be found on the `Python Package Index <https://pypi.python.org/pypi?%3Aaction=search&term=httpie&submit=search>`_.
Here's a few picks:

* `httpie-api-auth <https://github.com/pd/httpie-api-auth>`_: ApiAuth
* `httpie-aws-auth <https://github.com/httpie/httpie-aws-auth>`_: AWS / Amazon S3
* `httpie-edgegrid <https://github.com/akamai-open/httpie-edgegrid>`_: EdgeGrid










HTTPS
=====


Server SSL certificate verification
-----------------------------------

To skip the host's SSL certificate verification, you can pass ``--verify=no``
(default is ``yes``):

.. code-block:: bash

    $ http --verify=no https://example.org


Custom CA bundle
----------------

You can also use ``--verify=<CA_BUNDLE_PATH>`` to set a custom CA bundle path:

.. code-block:: bash

    $ http --verify=/ssl/custom_ca_bundle https://example.org



Client side SSL certificate
---------------------------
To use a client side certificate for the SSL communication, you can pass
the path of the cert file with ``--cert``:

.. code-block:: bash

    $ http --cert=client.pem https://example.org


If the private key is not contained in the cert file you may pass the
path of the key file with ``--cert-key``:

.. code-block:: bash

    $ http --cert=client.crt --cert-key=client.key https://example.org






Output options
==============

By default, HTTPie only outputs the final response and the whole response
message is printed (headers as well as the body). You can control what should
be printed via several options:

=================   =====================================================
``--headers, -h``   Only the response headers are printed.
``--body, -b``      Only the response body is printed.
``--verbose, -v``   Print the whole HTTP exchange (request and response).
                    This option also enables ``--all`` (see below).
``--print, -p``     Selects parts of the HTTP exchange.
=================   =====================================================

``--verbose`` can often be useful for debugging the request and generating
documentation examples:

.. code-block:: bash

    this isn't bash
    but i can use it like it was 

    $ http --verbose PUT httpbin.org/put hello=world
    PUT /put HTTP/1.1
    Accept: application/json, */*
    Accept-Encoding: gzip, deflate
    Content-Type: application/json
    Host: httpbin.org
    User-Agent: HTTPie/0.2.7dev

    {
        "hello": "world"
    }



    {
        […]
    }


What parts of the HTTP exchange should be printed
-------------------------------------------------

All the other `output options`_ are under the hood just shortcuts for
the more powerful ``--print, -p``. It accepts a string of characters each
of which represents a specific part of the HTTP exchange:

==========  ==================
Character   Stands for
==========  ==================
``H``       request headers
``B``       request body
``h``       response headers
``b``       response body
==========  ==================

Print request and response headers:

.. code-block:: bash

    $ http --print=Hh PUT httpbin.org/put hello=world





Terminal output
===============

HTTPie does several things by default in order to make its terminal output
easy to read.


Colors and formatting
---------------------

Syntax highlighting is applied to HTTP headers and bodies (where it makes
sense). You can choose your preferred color scheme via the ``--style`` option
if you don't like the default one (see ``$ http --help`` for the possible
values).

Also, the following formatting is applied:

* HTTP headers are sorted by name.
* JSON data is indented, sorted by keys, and unicode escapes are converted
  to the characters they represent.

One of these options can be used to control output processing:

====================   ========================================================
``--pretty=all``       Apply both colors and formatting.
                       Default for terminal output.
``--pretty=colors``    Apply colors.
``--pretty=format``    Apply formatting.
``--pretty=none``      Disables output processing.
                       Default for redirected output.
====================   ========================================================

Binary data
-----------

Binary data is suppressed for terminal output, which makes it safe to perform
requests to URLs that send back binary data. Binary data is suppressed also in
redirected, but prettified output. The connection is closed as soon as we know
that the response body is binary,

.. code-block:: bash

    $ http example.org/Movie.mov


You will nearly instantly see something like this:

.. code-block:: http

    HTTP/1.1 200 OK
    Accept-Ranges: bytes
    Content-Encoding: gzip
    Content-Type: video/quicktime
    Transfer-Encoding: chunked

    +-----------------------------------------+
    | NOTE: binary data not shown in terminal |
    +-----------------------------------------+


Redirected output
=================

HTTPie uses a different set of defaults for redirected output than for
`terminal output`_. The differences being:

* Formatting and colors aren't applied (unless ``--pretty`` is specified).
* Only the response body is printed (unless one of the `output options`_ is set).
* Also, binary data isn't suppressed.

The reason is to make piping HTTPie's output to another programs and
downloading files work with no extra flags. Most of the time, only the raw
response body is of an interest when the output is redirected.

Download a file:

.. code-block:: bash

    $ http example.org/Movie.mov > Movie.mov


Download an image of Octocat, resize it using ImageMagick, upload it elsewhere:

.. code-block:: bash

    $ http octodex.github.com/images/original.jpg | convert - -resize 25% -  | http example.org/Octocats


Force colorizing and formatting, and show both the request and the response in
``less`` pager:

.. code-block:: bash

    $ http --pretty=all --verbose example.org | less -R


The ``-R`` flag tells ``less`` to interpret color escape sequences included
HTTPie`s output.

You can create a shortcut for invoking HTTPie with colorized and paged output
by adding the following to your ``~/.bash_profile``:

.. code-block:: bash

    function httpless {
        # `httpless example.org'
        http --pretty=all --print=hb "$@" | less -R;
    }







Resuming downloads
------------------

If ``--output, -o`` is specified, you can resume a partial download using the
``--continue, -c`` option. This only works with servers that support
``Range`` requests and ``206 Partial Content`` responses. If the server doesn't
support that, the whole file will simply be downloaded:

.. code-block:: bash

    $ http -dco file.zip example.org/file

Other notes
-----------

* The ``--download`` option only changes how the response body is treated.
* You can still set custom headers, use sessions, ``--verbose, -v``, etc.
* ``--download`` always implies ``--follow`` (redirects are followed).
* HTTPie exits with status code ``1`` (error) if the body hasn't been fully
  downloaded.
* ``Accept-Encoding`` cannot be set with ``--download``.







Examples use cases
------------------

Prettified streamed response:

.. code-block:: bash

    $ http --stream -f -a YOUR-TWITTER-NAME https://stream.twitter.com/1/statuses/filter.json track='Justin Bieber'


Streamed output by small chunks alá ``tail -f``:

.. code-block:: bash

    # Send each new tweet (JSON object) mentioning "Apple" to another
    # server as soon as it arrives from the Twitter streaming API:
    $ http --stream -f -a YOUR-TWITTER-NAME https://stream.twitter.com/1/statuses/filter.json track=Apple \
    | while read tweet; do echo "$tweet" | http POST example.org/tweets ; done

Sessions
========

By default, every request HTTPie makes is completely independent of any
previous ones to the same host.


However, HTTPie also supports persistent
sessions via the ``--session=SESSION_NAME_OR_PATH`` option. In a session,
custom `HTTP headers`_ (except for the ones starting with ``Content-`` or ``If-``),
`authentication`_, and `cookies`_
(manually specified or sent by the server) persist between requests
to the same host.


.. code-block:: bash

    # Create a new session
    $ http --session=/tmp/session.json example.org API-Token:123

    # Re-use an existing session — API-Token will be set:
    $ http --session=/tmp/session.json example.org


All session data, including credentials, cookie data,
and custom headers are stored in plain text.
That means session files can also be created and edited manually in a text
editor—they are regular JSON. It also means that they can be read by anyone
who has access to the session file.




Anonymous sessions
------------------

Instead of a name, you can also directly specify a path to a session file. This
allows for sessions to be re-used across multiple hosts:

.. code-block:: bash

    $ http --session=/tmp/session.json example.org
    $ http --session=/tmp/session.json admin.example.org
    $ http --session=~/.httpie/sessions/another.example.org/test.json example.org
    $ http --session-read-only=/tmp/session.json example.org


Readonly session
----------------

To use an existing session file without updating it from the request/response
exchange once it is created, specify the session name via
``--session-read-only=SESSION_NAME_OR_PATH`` instead.






Scripting
=========

When using HTTPie from shell scripts, it can be handy to set the
``--check-status`` flag. It instructs HTTPie to exit with an error if the
HTTP status is one of ``3xx``, ``4xx``, or ``5xx``. The exit status will
be ``3`` (unless ``--follow`` is set), ``4``, or ``5``,
respectively.

.. code-block:: bash

    #!/bin/bash

    if http --check-status --ignore-stdin --timeout=2.5 HEAD example.org/health &> /dev/null; then
        echo 'OK!'
    else
        case $? in
            2) echo 'Request timed out!' ;;
            3) echo 'Unexpected HTTP 3xx Redirection!' ;;
            4) echo 'HTTP 4xx Client Error!' ;;
            5) echo 'HTTP 5xx Server Error!' ;;
            6) echo 'Exceeded --max-redirects=<n> redirects!' ;;
            *) echo 'Other Error!' ;;
        esac
    fi


Meta
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