Gene Sequencing Data Processing with Apache Spark 
########################################

|

Link to our public website:   https://thesparkgenomeproject.com/

|

The following github repo contains information assembled for our course project, and contains all the details of how we completed this ambitious project


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
=========================

Some high level basics 

genome
  In the fields of molecular biology and genetics, a genome is the genetic material of an organism. It consists of DNA (or RNA in RNA viruses). The genome includes both the genes (the coding regions) and the noncoding DNA,[1] as well as mitochondrial DNA[2] and chloroplast DNA. The study of the genome is called genomics.


genome sequence
  A genome sequence is the complete list of the nucleotides (A, C, G, and T for DNA genomes) that make up all the chromosomes of an individual or a species. Within a species, the vast majority of nucleotides are identical between individuals, but sequencing multiple individuals is necessary to understand the genetic diversity.

NGS
  Next generation sequencing (NGS), massively parallel or deep sequencing are related terms that describe a DNA sequencing technology which has revolutionised genomic research. Using NGS an entire human genome can be sequenced within a single day. In contrast, the previous Sanger sequencing technology, used to decipher the human genome, required over a decade to deliver the final draft.


* Genes are incredibly complicated
* Sequencing high level is 
* Really short explanation of the biochemical tie-in
* Result is huge files and huge processing time, which we believe we can alleviate with our distributed computing approach 





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

* Runs workloads 100x+ faster than conventional approaches
* Think divide and conquer !  (good metaphor Joe) 
* Distributed processing
* Quasi-infinite scaling
* Standaridized and Generalized
* Capable of combining SQL, streaming, and complex analytics
* Runs *everywhere*: Hadoop, Apache Mesos, Kubernetes, standalone, in the cloud (Azure, AWS, etc)





.. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/spark-runs-everywhere.png  
  :width: 200
  :alt: Alternative text





|




Background
==============

Apache Spark™ is a unified analytics engine for large-scale data processing.  Spark SQL is Apache Spark's module for working with structured data, and the primary appliation we will be using to demonstrate our proficiency in our Databases course.  Spark appliations can be written in Java, Scala, R, Python, and SQL;  We focus on Python and SQL, with a splash of R for visualization images.  

Our goal is to document how much more streamlined and efficient this system is for processing massive terabyte-sized DNA sequencing raw data, and demonstrate the usage of SparkSQL to query this datastructure. 


|



Our Approach
=============

* Research the basics of Apache Spark 
* Research SparkSQL and pyspark 
* Focus on building practice notebooks along our journey
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

As we progress step-by-step, we will upload jupyter notebooks. This is the key to really understanding this complicated approach. 

|

Notebooks Links
------------------------

The following are pertinent links to information about the processing steps we took 

* `Databricks 101 <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/001-pyspark.ipynb>`_
  for introductory example of how to create RDD datasets and get familiar with the Databricks platform
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

    import hail as hl
    print(hl.cite_hail())






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

References
----------------

Links
~~~~~~~~~~~~


* `Apache Spark <https://spark.apache.org/>`_
  — Main Apache Spark website
* `SparkSQL <https://spark.apache.org/sql/>`_
  — Main SparkSQL website 
* `Hadoop <http://python-requests.org>`_
  — Hadoop Standard Library
* `Databricks Community Edition Login <https://community.cloud.databricks.com/login.html;jsessionid=auth-auth-ce-7cfd54686d-vz28zhud1bk06082eui1au33svckk.auth-auth-ce-7cfd54686d-vz28z>`_
  — where you can log in and use SparkSQL
* `Hail <https://hail.is/>`_
  — this is where it starts getting very complicated
* `.rst essentials <https://gist.github.com/ionelmc/e876b73e2001acd2140f>`_
  — more advanced .rst creation

