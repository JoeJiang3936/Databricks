
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

Some high level basics... 

genome
  In the fields of molecular biology and genetics, a genome is the genetic material of an organism. It consists of DNA (or RNA in RNA viruses). The genome includes both the genes (the coding regions) and the noncoding DNA, as well as mitochondrial DNA and chloroplast DNA. The study of the genome is called genomics.


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

Apache Spark is an open-source distributed general-purpose cluster computing framework with (mostly) in-memory data processing engine that can do ETL, analytics, machine learning and graph processing on large volumes of data at rest (batch processing) or in motion (streaming processing) with rich concise high-level APIs for the programming languages: Scala, Python, Java, R, and SQL.


It is fundamentally unified analytics engine for large-scale data processing.  Spark SQL is Apache Spark's module for working with structured data, and the primary appliation we will be using to demonstrate our proficiency in our Databases course.  Spark appliations can be written in Java, Scala, R, Python, and SQL;  We focus on Python and SQL, with a splash of R for visualization images.  

Our goal is to document how much more streamlined and efficient this system is for processing massive terabyte-sized DNA sequencing raw data, and demonstrate the usage of SparkSQL to query this datastructure. 


|



Our Approach
=============

* Research the basics of Apache Spark  
* Research SparkSQL and pyspark API libraries  
* Focus on building practice jupyter notebooks along our journey, step-by-step
* Get Apache Spark (with Hadoop, Scala/sbt, JVM) running on laptop (local mode)
* Understand how to baseline and monitor database query and access KPIs for local mode
* Get Apache Spark running, via Databricks online, in local mode
* Baseline with UI to see the 'performance' of SparkSQL queries, joins, actions 
* Get Apache Spark running, via Databricks (distributed cluster mode)
* Baseline
* Import small datasets into Databricks
* Experiment with HDFS file type versions
* Push 1GB+ data faile onto system 
* Push a beyond-TB sized sequence table to cluster
* Process the table via SparkSQL, convert to Dataframes/Datasets, leverage ApacheSpark 2.x version, beyond the simple concepts of RDD
* Run 3rd-party app like Hail or some other crazy complex system on Databricks
* Push further into expanding model into full cloud-hosted versions (AWS-like)
* Distribute files to multiple S3 instances, tie in 
* Document the performance differences as you run these individual approaches
* Time it:  get really good with Databricks, ApacheSpark, and Scala, and *then* pop into a free Genomics Platform from Databricks for seven day crunch
* Push hard into TB-sized genomics, next-generation DNA sequencing, genomics and informatics
* Publish all results 


|


.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/spark-map-transformation-operation.gif 
        :alt: HTTPie in action
        :width: 100%
        :align: center


.. class:: no-web no-pdf



|


If we do this efficiently, we can keep the processing optimized in batch processing:

.. class:: no-web


    .. image:: .\ENTER\images\rainbow.png
        :alt: HTTPie in action
        :width: 100%
        :align: center


.. class:: no-web no-pdf




|


Jupyter Notebooks 
==================

As we progress step-by-step, we will upload jupyter notebooks. This is the key to really understanding this complicated approach. 

|

Jupyter Notebook Links
------------------------

The following are pertinent links to information about the processing steps we took 


* `VCF  <https://faculty.washington.edu/browning/intro-to-vcf.html#example>`_
  — An introduction to the genomic Variant Call Format 



* `SparkSQL on Genomic Data <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/successful_processing_vcf_genome_spark.ipynb>`_
  — successful implementation of reading and processing via SparkSQL a .vcf genomics data fie series (Anaconda Windows10 laptop)

* `SparkSQL on Genomic Data HTML View <http://htmlpreview.github.io/?https://github.com/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/html/successful_processing_vcf_genome_spark.html>`_
— same as above but probably easier to read


* `Databricks 101 <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/001-pyspark.ipynb>`_
— for introductory example of how to create RDD datasets and get familiar with the Databricks platform
* `Databricks 101 HTML <https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/notebooks/001-pyspark.html>`_
— if you just want to download the .html to your phone or whatever and view output
* `Databricks 201 <https://stackoverflow.com>`_
— our deeper exploration into Databricks and pyspark



   
|


Think big picture.  We need to change our perception on what we consider a LOT of data...

.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/purple.jpg 
        :alt: HTTPie in action
        :width: 100%
        :align: center


.. class:: no-web no-pdf


|


Sample Code 
------------------------


.. code-block:: python

    import findspark
    findspark.init()
    import pyspark
    import random
    sc = pyspark.SparkContext()

    import hail as hl
    print(hl.cite_hail())

    # The advantage of using ‘object’ dtype is that strings can be of any length. 
    # Alternatively, you can use a fixed-length string dtype, e.g.:

    callset = allel.read_vcf('C:/SPARK/sample.vcf', types={'REF': 'S3'})
    callset['variants/REF']

    callset = allel.read_vcf('C:/SPARK/sample.vcf')
    callset['variants/REF']
    callset = allel.read_vcf('C:/SPARK/sample.vcf')
    callset['variants/ALT']

    callset = allel.read_vcf(vcf_path, fields=['numalt'], log=sys.stdout)

    allel.vcf_to_hdf5('C:/SPARK/sample.vcf', 'C:/SPARK/sample_hdf5.h5', fields='*', overwrite=True)

    spark.read.json("s3n://...").registerTempTable("json")
    results = spark.sql(
    """SELECT * 
     FROM people
     JOIN json ...""")


    

    







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
|


References
=========


Links
----------------


|

General
~~~~~~~~~~~~


* `Apache Spark <https://spark.apache.org/>`_
  — Main Apache Spark website
* `Hadoop <https://hadoop.apache.org/>`_
  — Hadoop Standard Library
* `Databricks Community Edition Login <https://community.cloud.databricks.com/login.html;jsessionid=auth-auth-ce-7cfd54686d-vz28zhud1bk06082eui1au33svckk.auth-auth-ce-7cfd54686d-vz28z>`_
  — where you can log in and use SparkSQL and other Databricks APIs




|




SparkSQL
~~~~~~~~~~~~


* `SparkSQL <https://spark.apache.org/sql/>`_
  — Main SparkSQL website 
* `SparkSQL Apache Guide <https://spark.apache.org/docs/latest/sql-programming-guide.html>`_
  — Spark SQL, DataFrames and Datasets Guide
  
  

|




Scala
~~~~~~~~~~~~


* `Scala <https://www.scala-lang.org/>`_
  — Main website for Scala.  There is no getting around it.  You want to push the envelope, you must learn Scala...



|



Next Generation DNA Sequencing (NGS)
~~~~~~~~~~~~~~~~~~~~~~~~~~


* `VCF  <https://faculty.washington.edu/browning/intro-to-vcf.html#example>`_
  — An introduction to the genomic Variant Call Format 
* `VCF Specification  <https://samtools.github.io/hts-specs/VCFv4.3.pdf>`_
  — the variant call format specification, its written like a clean engineering breakout doc, its only 36 pages dude, just read it. 
  * `Hail <https://hail.is/>`_
  — this is where it starts getting very complicated
* `Big Data Genomics <http://bdgenomics.org/>`_
  — Variant Calling with Cannoli, ADAM, Avocado, and DECA
* `Genomics in the Cloud <https://aws.amazon.com/health/genomics/>`_
  — Amazon information about how to simplify and securely scale genomic analysis with AWS platform 
* `Workflows  <https://docs.opendata.aws/genomics-workflows/>`_
  — Genomics workflows on AWS
* `Igenomix  <https://aws.amazon.com/solutions/case-studies/igenomix/>`_
  — AWS-based case study of Igenomix and NGS
* `Data Slicer  <http://grch37.ensembl.org/Homo_sapiens/Tools/DataSlicer?db=core>`_
  — subset of extremely large datasets VCF BAM etc 
* `Databricks Pipeline  <https://databricks.com/blog/2018/09/10/building-the-fastest-dnaseq-pipeline-at-scale.html>`_
  — Building the Fastest DNASeq Pipeline at Scale
* `Databricks Unified Analytics Platform for Genomics <https://github.com/TomBresee/The_Spark_Genome_Project/raw/master/ENTER/txt_based_info/Unified_Analytics_Platform_for_Genomics_Databricks.pdf>`_
  — Blueprint data for new Databricks Genomics platform 
* `Google Genomics Home <https://cloud.google.com/genomics/#>`_
  — Main page overview of Google Genomics program for processing petabytes of genomic data
* `Google Whitepaper <https://github.com/TomBresee/The_Spark_Genome_Project/raw/master/ENTER/txt_based_info/google-genomics-whitepaper.pdf>`_
  — Using Google Genomics API to query massive bioinformational datasets



|




Solid Links
~~~~~~~~~~~~~~~~~~~~~~~~~~


* `pyspark transformations <https://nbviewer.jupyter.org/github/jkthompson/pyspark-pictures/blob/master/pyspark-pictures.ipynb>`_
  — really good overviews of the transformations possible 

* `gitbook mastering sparksql <https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql.html>`_
  — great gitbook, very detailed

* `scala examples  <http://blog.madhukaraphatak.com/introduction-to-spark-two-part-2/>`_
  — scala examples

* `json lines (not json) <http://jsonlines.org/>`_
  —  this page describes the JSON Lines text format, also called newline-delimited JSON. JSON Lines is a convenient format for storing structured data that may be processed one record at a time. It works well with unix-style text processing tools and shell pipelines. It's a great format for log files. It's also a flexible format for passing messages between cooperating processes. SSON Lines handles tabular data cleanly and without ambiguity. Stream compressors like gzip or bzip2 are recommended for saving space, resulting in .jsonl.gz or .jsonl.bz2 files...

  


|
|



Appendix - Variant Call Format (VCF) file field breakout
=========



.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/screengrab.png
        :alt: HTTPie in action
        :width: 100%
        :align: center

.. class:: no-web no-pdf






