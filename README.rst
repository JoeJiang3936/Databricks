
Gene Sequencing Data Processing with Apache Spark 
########################################



|



Link to our public website:   

https://thesparkgenomeproject.com/



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
* Accidentally a perfect fit for NGS and precision medicine





.. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/spark-runs-everywhere.png  
  :width: 200
  :alt: Alternative text















|
|
Background
==============

Apache Spark is an open-source distributed general-purpose cluster computing framework with (mostly) in-memory data processing engine that can do ETL, analytics, machine learning and graph processing on large volumes of data at rest (batch processing) or in motion (streaming processing) with rich concise high-level APIs for the programming languages: Scala, Python, Java, R, and SQL.


It is fundamentally unified analytics engine for large-scale data processing.  Spark SQL is Apache Spark's module for working with structured data, and the primary appliation we will be using to demonstrate our proficiency in our Databases course.  Spark appliations can be written in Java, Scala, R, Python, and SQL;  We focus on Python and SQL, with a splash of R for visualization images.  

Our goal is to document how much more streamlined and efficient this system is for processing massive terabyte-sized DNA sequencing raw data, and demonstrate the usage of SparkSQL to query this datastructure. 















|
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
|
Our Technical Approach
==================

|

- **All input sequenced files will be .VCF format (or .BAM)**
   - Standard file format for DNA sequenced files


=====   ===========
File    Description
=====   ===========
VCF     VCF stands for Variant Call Format. It is a standardized text file format for representing SNP, INDEL, SV and CNV variation calls. SNPs (Single Sucleotide Polymorphisms, pronounced “snips”), are the most common type of genetic variation among people. Each SNP represents a difference in a single DNA building block, called a nucleotide. This is the most used VCF.

BAM     Binary Alignment Map (BAM) is the comprehensive raw data of genome sequencing; it consists of the lossless, compressed binary representation of the Sequence Alignment Map. BAM files are 90-100 gigabytes in size. They are generated by aligning the FASTQ files to the reference genome.

FASTQ   FASTQ files contain billions of entries and are about 90-100 gigabytes in size.  Truly raw data.           
=====   ===========  


 Note:  VCF files include SNPs, INDELs, CNV and SV


- **All files are stored during the process in Apache Parquet format**
   - This format has advantages of compressed, efficient columnar data storage format and representation
   - Interop with Hadoop
   - Built from the ground up with complex nested data structures in mind
   - Uses record shredding and assembly algorithm
   - Very efficient compression and encoding schemes
   - We want compression but not at the cost of reading ! 
   - We also will demonstrate the performance impact of applying the right compression and encoding scheme to the data
   - Parquet allows compression schemes to be specified on a per-column level, and is future-proofed to allow adding more encodings as they are invented and implemented
   - File format image `here <https://github.com/TomBresee/The_Spark_Genome_Project/raw/master/ENTER/images/FileFormat.gif>`_ and file metadata format image `here <https://github.com/TomBresee/The_Spark_Genome_Project/raw/master/ENTER/images/FileLayout.gif>`_  

- **Philosopy - Keep I/O to a minimum**
   -  Parquet 2.0   

- **Parallelize everywhere we can**
   -  process instructions in parallel
   -  avoid jumps like 'if'  

- **Minimize shuffles !**
   -  Spark shuffles will call to io process, so we try to avoid  

- **Misc**
   -  Focus on defining workload behavior
   -  Fully utilize 
   -  compute vs io
   -  Spark shuffles will call to io process, so we try to avoid  
   -  Parquet creates a compression format for each Avro-defined data model
   -  Avro and Parquet for data models and file formats ! 






https://github.com/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/dbricks/Working%20with%20SQL%20at%20Scale%20-%20Spark%20SQL%20Tutorial.ipynb



|
|
Jupyter Notebooks 
==================

As we progress step-by-step, we will upload jupyter notebooks. This is the key to really understanding this complicated approach. 

|

Jupyter Notebook Links
------------------------

The following are pertinent links to information about the processing steps we took 


* `SparkSQL Basics on Databricks CE <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/dbricks/Working%20with%20SQL%20at%20Scale%20-%20Spark%20SQL%20Tutorial.ipynb>`_
  — showings the basics of SparkSQL usage on the Databricks platform

* `SparkSQL on Genomic Data HTML View <http://htmlpreview.github.io/?https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/dbricks/Working%20with%20SQL%20at%20Scale%20-%20Spark%20SQL%20Tutorial.html>`_
  — HTML view of the above jupyter notebook

|


* `SparkSQL on Genomic Data <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/successful_processing_vcf_genome_spark.ipynb>`_
  — successful implementation of reading and processing via SparkSQL a .vcf genomics data fie series (Anaconda Windows10 laptop)

* `SparkSQL on Genomic Data HTML View <http://htmlpreview.github.io/?https://github.com/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/html/successful_processing_vcf_genome_spark.html>`_
  — HTML view of the above jupyter notebook


http://htmlpreview.github.io/?https://github.com/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/dbricks/Working%20with%20SQL%20at%20Scale%20-%20Spark%20SQL%20Tutorial.html



|


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




Connecting to Databricks
~~~~~~~~~~~~

* `Connecting BI Tools  <https://docs.databricks.com/user-guide/bi/jdbc-odbc-bi.html>`_
  — JDBC/ODBC driver and connectivity 
* `Connecting MySQL Workbench <https://docs.databricks.com/user-guide/bi/workbenchj.html>`_
  — Connecting org.apache.hive.jdbc.HiveDriver driver definition  
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


* `Genetics Home Reference  <https://ghr.nlm.nih.gov/>`_
  — An introduction Genetics

* `What is DNA <https://ghr.nlm.nih.gov/primer/basics/dna>`_
  — DNA breakdown

* `VCF  <https://faculty.washington.edu/browning/intro-to-vcf.html#example>`_
  — An introduction to the genomic Variant Call Format file type 
* `VCF Specification  <https://samtools.github.io/hts-specs/VCFv4.3.pdf>`_
  — the variant call format specification, its written like a clean engineering breakout doc, its only 36 pages dude, just read it 
* `Genetic Data VCF BAM FASTQ  <https://us.dantelabs.com/blogs/news/genetic-data-fastq-bam-and-vcf>`_
  — The big picture view of the file format options and their place in sequencing
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
* `Spark Accelerated Genomics Processing <https://github.com/TomBresee/The_Spark_Genome_Project/raw/master/ENTER/txt_based_info/summit-talk_2019.pdf>`_
  — Spark Summit Slides about next generation sequencing and Spark










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
Appendix - Variant Call Format (VCF) fields breakout
=========



.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/screengrab.png
        :alt: HTTPie in action
        :width: 100%
        :align: center

.. class:: no-web no-pdf




|
|
|





|
ToDo
=========

-  create databricks account . . . . . . . . . . . . . . . . . . . . . . . . [complete]

-  create public databricks notebook test `post <https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/7001951515152566/3688659401164340/6475682490817878/latest.html>`_ . . . . . . . . [complete]

-  get adam and hail both up in spark environment (this is not expected to be easy)

-  create image of the whole set up

-  baseline and comparisons

-  pipelines up and working

-  db benchmark entire approach up and running 

-  queries to baseline 

-  databricks notebooks url links capture to unlist 

-  https://cdn2.hubspot.net/hubfs/438089/notebooks/Samples/Data_Exploration/Data_Exploration_on_Databricks_Setup.html

-  https://docs.databricks.com/_static/notebooks/mlflow/mlflow-quick-start-python.html

-  https://github.com/evodify

-  https://github.com/evodify/genomic-analyses_in_apache-spark

-  hail scala here ?   https://github.com/evodify/genomic-analyses_in_apache-spark/tree/master/hail-scala

-  databricks documentation:  https://docs.databricks.com/index.html



-  https://docs.databricks.com/applications/genomics/hls-runtime.html#dbr-hls
-  really good cluster information:
   https://community.cloud.databricks.com/driver-proxy/o/7001951515152566/0611-033207-may118/80/?c=cluster


