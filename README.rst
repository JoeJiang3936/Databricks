Gene Sequencing Data Processing with Apache Spark 
########################################

|

https://thesparkgenomeproject.com/

|

The following github repo contains information assembled for our course project


|




.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/dna_rotating.gif
        :alt: HTTPie in action
        :width: 100%
        :align: center

.. class:: no-web no-pdf




|



.. contents::

.. section-numbering::


|



Gene Sequencing Explained
=============

* Genes are fancy 
* Sequencing
* Really short explanation of the biochemical tie-in
* Result is huge files and huge processing time 






.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/tom2.gif
        :alt: HTTPie in action
        :width: 100%
        :scale: 20
        :align: right


.. class:: no-web no-pdf






|




Why Apache Spark ? 
=============

* Runs workloads 100x faster
* Distributed processing
* Quasi-infinite scaling
* Standaridized and Generalized
* Capable of combining SQL, streaming, and complex analytics
* Runs everywhere:  Hadoop, Apache Mesos, Kubernetes, standalone, in the cloud (Azure, AWS, etc)





.. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/spark-runs-everywhere.png  
  :width: 200
  :alt: Alternative text





|






Background
==============

Apache Spark™ is a unified analytics engine for large-scale data processing.  Spark SQL is Apache Spark's module for working with structured data.
Spark appliations can be written in Java, Scala, R, Python, and SQL. For the purposes of this exercise we will primarily be focusing on Python and SQL approaches within Apache Spark. 

Our goal is to document how much more streamlined and efficient this system is for processing massive terabyte-sized DNA sequencing raw data, and demonstrate the usage of SparkSQL to query this datastructure. 



|








Our Approach
=============

* Research the basics of Apache Spark 
* Research SparkSQL and pyspark 
* Get Apache Spark running on laptop (local mode)
* Understand how to baseline and monitor database query and access KPIs for local mode
* Get Apache Spark running, via Databricks (local mode)
* Baseline
* Get Apache Spark running, via Databricks (distributed compute mode!)
* Baseline
* Import small datasets
* Experiment with HDFS file type versions
* Push a beyond-TB sized sequence table to cluster
* Process the table via SparkSQL, etc
* Run 3rd-party app like Hail or some other crazy complex system on Databricks
* Push further into expanding model into full cloud-hosted versions (AWS-like)
* Document the performance differences as you run these individual approaches
* I don't know, something like the above, none of us has Apache Spark experience, but i think we can pull this off 




|


.. class:: no-web



    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/spark-map-transformation-operation.gif 
        :alt: HTTPie in action
        :width: 100%
        :align: center



.. class:: no-web no-pdf






|

Jupyter Notebooks 
=========

As we progress step-by-step, we will upload jupyter notebooks

|

Notebooks Links
------------------------

The following are pertinent links to information about the processing steps we took 

* `Databricks 101 <https://github.com/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/001-pyspark.ipynb>`_
  for introductory example of how to create RDD datasets
* `Databricks 101 HTML <https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/notebooks/001-pyspark.html>`_
  if you just want to download the .html to your phone or whatever and view output


* `Databricks 201 <https://stackoverflow.com>`_
  our deeper exploration into Databricks and pyspark
* `SparkSQL 101 <https://stackoverflow.com>`_
  for introductory example of how to query and analyze datasets and databases


   
|


Sample Code 
------------------------




.. code-block:: python

    import findspark
    findspark.init()
    import pyspark
    import random
    sc = pyspark.SparkContext(appName="Pi")
    num_samples = 100000000
    def inside(p):     
        x, y = random.random(), random.random()
        return x*x + y*y < 1
    count = sc.parallelize(range(0, num_samples)).filter(inside).count()
    pi = 4 * count / num_samples
    print(pi)
    sc.stop()





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

|

Apache Spark and Pyspark
------------------------

The following are pertinent links to information about the processing steps we took 

* `GitHub issues <https://github.com/jkbr/httpie/issues>`_
  for bug reports and feature requests.
* `StackOverflow <https://stackoverflow.com>`_
  to ask questions 
* Tweet directly to us at `@TSGP <https://twitter.com/clihttp>`_.
* You can also tweet directly to `@realTomBresee`_.


|

References
----------------


Links
~~~~~~~~~~~~


* `Apache Spark <https://spark.apache.org/>`_
  — Main Apache Spark website
* `SparkSQL <https://spark.apache.org/sql/>`_
  — Main Apache Spark website 
* `Hadoop <http://python-requests.org>`_
  — Hadoop Standard Library
* `Apache Spark <https://spark.apache.org/>`_
  — Main Apache Spark website 



