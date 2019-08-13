
Gene Sequencing Data Processing with Apache Spark 
########################################



|
|




**What is this ?**  

The following github repo contains detailed information about utilizing Apache Spark with Genomics Analysis. 

There is also an associated public website that is in process:  https://thesparkgenomeproject.com/


|
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
|
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
|

Background
==============

Apache Spark is an open-source distributed general-purpose cluster computing framework with (mostly) in-memory data processing engine that can do ETL, analytics, machine learning and graph processing on large volumes of data at rest (batch processing) or in motion (streaming processing) with rich concise high-level APIs for the programming languages: Scala, Python, Java, R, and SQL.


It is fundamentally unified analytics engine for large-scale data processing.  Spark SQL is Apache Spark's module for working with structured data, and the primary appliation we will be using to demonstrate our proficiency in our Databases course.  Spark appliations can be written in Java, Scala, R, Python, and SQL;  We focus on Python and SQL, with a splash of R for visualization images.  

Our goal is to document how much more streamlined and efficient this system is for processing massive terabyte-sized DNA sequencing raw data, and demonstrate the usage of SparkSQL to query this datastructure. 



|


Think big picture.  We need to change our perception on what we consider a LOT of data...




|

.. class:: no-web


    .. image:: https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/images/purple.jpg 
        :alt: HTTPie in action
        :width: 100%
        :align: center


.. class:: no-web no-pdf





|
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



|
|
|

Jupyter Notebooks 
==================

As we progress step-by-step, we will upload jupyter notebooks. This is the key to really understanding this complicated approach. 

|

Jupyter Notebook Links
------------------------

The following are working jupyter notebooks as we dive deeper into Apache Spark, Databricks, etc 

|



* `Databricks 101 <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/001-pyspark.ipynb>`_
  — for introductory example of how to create RDD datasets and get familiar with the Databricks platform


|


* `SparkSQL Basics on Databricks CE <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/dbricks/Working%20with%20SQL%20at%20Scale%20-%20Spark%20SQL%20Tutorial.ipynb>`_
  — showings the basics of SparkSQL usage on the Databricks platform


|


* `SQL Notebook 1 on Databricks CE <https://rawcdn.githack.com/TomBresee/The_Spark_Genome_Project/bcccb13349bed18a85e685734e5bd3cac0bfb64f/ENTER/dbricks/beta - SQL - test.html>`_
  — for introductory example of how to use SQL notebook file directly on Databricks, NOT LINKED YET, TO BE FIXED...

|

* `SQL Notebook 2 on Databricks CE <https://rawcdn.githack.com/TomBresee/The_Spark_Genome_Project/1e07b240b348ad0925682ea422c3c94ecbd94b27/ENTER/dbricks/beta%20-%20SQL%20-%20Pop%20vs%20Price.html>`_
  — for introductory example of how to use SQL notebook file directly on Databricks


|



* `Apache Parquet file type usage on Databricks CE <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/dbricks/readingParquetFiles.ipynb>`_
  — for getting a feel for this type of file format


|



* `Working with CSV Files <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/Working%20with%20csv%20files.ipynb>`_
  — working with reading and writing .csv files in different languages


|


* `Intermediate Level Data Analysis Demo2  <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/Demo2.ipynb>`_
  — Demo-002  




|


* `SparkSQL Basics on Databricks <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/Working%20with%20SQL%20at%20Scale%20-%20Spark%20SQL%20Tutorial.ipynb>`_
  — successful implementation of core SparkSQL commands


|


* `Hail on Databricks written in Python with PCA  <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/Genomics%26Spark%20.ipynb>`_
  — Hail 0.2, Databricks, Apache Spark, production version, PCA  


|




* `SparkSQL on Genomic Data <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/notebooks/successful_processing_vcf_genome_spark.ipynb>`_
  — successful implementation of reading and processing via SparkSQL a .vcf genomics data fie series (Anaconda Windows10 laptop)



|


* `Hail running on Apache Spark running on Ubuntu <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/HAIL%20on%20Apache%20Spark.ipynb>`_
  — successful implementation of Hail 0.2 on Apache Spark (Ubuntu-based), working example (notebook kept in the 'working notebooks' sub-folder under /ENTER)



|


* `Hail running on Databricks Apache Spark written in Scala <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/hail_databricks.ipynb>`_
  — successful implementation of Hail 0.2 on the Databricks platform in Scala code  


|


* `Hail on Databricks written in Python with PCA  <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/Genomics%26Spark%20.ipynb>`_
  — Hail 0.2, Databricks, Apache Spark, production version, PCA  

|

* `Hail on Databricks Demo for SMU <https://nbviewer.jupyter.org/github/TomBresee/The_Spark_Genome_Project/blob/master/ENTER/working_notebooks/Genomics%26Spark%20.ipynb>`_
  — Hail 0.2, Databricks, Apache Spark, production version, PCA  




|
|
|


References
=========


|


Apache Spark
-------------


* `Apache Spark Website <https://spark.apache.org/>`_
  — the core website for Apache Spark 


* `Apache Spark Documentation <https://spark.apache.org/docs/latest/>`_
  — the main documentation link 


* `Spark SQL DataFrames and Datasets Guide <https://spark.apache.org/docs/latest/sql-programming-guide.html>`_
  — the detailed information about using SparkSQL



* `Spark Python API Docs  <https://spark.apache.org/docs/latest/api/python/index.html>`_
  — covers pyspark .methods and commands 



* `Cluster Mode Overview   <https://spark.apache.org/docs/latest/cluster-overview.html>`_
  — how Spark runs on clusters



* `Gitbook Internals of Apache Spark   <https://jaceklaskowski.gitbooks.io/mastering-apache-spark/>`_
  — really really good overview of how Apache Spark functions



* `Gitbook Internals of Apache Spark SQL  <https://jaceklaskowski.gitbooks.io/mastering-spark-sql/>`_
  — same author, but covering SparkSQL



* `Github Apache Spark  <https://github.com/apache/spark>`_
  — the main Github page for Apache Spark



* `Github Spark Examples  <https://github.com/apache/spark/tree/master/examples/src/main>`_
  — you can see specific python, scala, and r examples you can run 


* `Hadoop <https://hadoop.apache.org/>`_
  — Hadoop Standard Library



|



Databricks
-------------


* `Documentation <https://docs.databricks.com/>`_
  — the main documentation link for Databricks


* `User Guide <https://docs.databricks.com/user-guide/index.html>`_
  — the main user manual for Databricks


* `Forum for Questions <https://forums.databricks.com/index.html>`_
  — questions and answers


* `Dataframe Guide <https://docs.databricks.com/spark/latest/dataframes-datasets/index.html>`_
  — covers dataframes, used extensively with genomics and sparksql 



* `SQL Guide <https://docs.databricks.com/spark/latest/spark-sql/index.html>`_
  — covers SQL language manual for databricks



* `Delta Lake  <https://delta.io/>`_
  — delta lake is an open-source storage layer that brings ACID transactions to Apache Spark workloads


* `Github Delta Lake  <https://github.com/delta-io/delta>`_
  — github location



* `Delta Lake Guide  <https://docs.databricks.com/delta/index.html>`_
  — Delta Lake is an open source storage layer that brings reliability to data lakes. Delta Lake provides ACID transactions, scalable metadata handling, and unifies streaming and batch data processing. Delta Lake runs on top of your existing data lake and is fully compatible with Apache Spark APIs.



* `Connecting BI Tools  <https://docs.databricks.com/user-guide/bi/jdbc-odbc-bi.html>`_
  — JDBC/ODBC driver and connectivity 


* `Connecting MySQL Workbench <https://docs.databricks.com/user-guide/bi/workbenchj.html>`_
  — Connecting org.apache.hive.jdbc.HiveDriver driver definition  


* `Hipster Scala Example <https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/8497971343024764/53198984527781/2559267461126367/latest.html>`_
  — scala example with variant spark


* `Databricks Connect  <https://docs.azuredatabricks.net/user-guide/dev-tools/db-connect.html>`_
  — direct CLI access to the instance


* `Databricks Supported Instance Types <https://databricks.com/product/aws-pricing/instance-types>`_
  — direct CLI access to the instance





|

Genomics
-------------


* `Hail Scala Genomics ETL Tutorial <https://lamastex.github.io/scalable-data-science/sds/2/2/db/999_05_StudentProject_HailScalaGenomicsETLTutorial.html>`_
  — Written by Dmytro Kryvokhyzha, excellent overview of using Databricks in Scala with Hail

 
* `Variant Spark Example <https://docs.databricks.com/_static/notebooks/variant-spark-hipster-index.html>`_
  — Demo custom machine learning library for real-time genomic data analysis with synthentic 'HipsterIndex' in Scala (VariantSpark_HipsterIndex_Spark2.2)


* `Databricks Genomics Guide <https://docs.databricks.com/applications/genomics/index.html>`_
  — Tertiary datapipe


* `Databricks Genomics Guide <https://docs.databricks.com/applications/genomics/index.html>`_
  — Tertiary datapipe

 
* `Dmytro Kryvokhyzha <https://github.com/evodify>`_
  —  Outstanding github repos for hard core genomics analysis.  This guy is good. 


* `Tom Databricks Notes <https://raw.githubusercontent.com/TomBresee/The_Spark_Genome_Project/master/ENTER/how2/databricks.txt>`_
  —  Outstanding github repos for hard core genomics analysis.  This guy is good. 



|

Scala
--------


* `Scala <https://www.scala-lang.org/>`_
  — the main website for Scala.  There is no getting around it.  You want to push the envelope, you must learn Scala...


* `Scala examples  <http://blog.madhukaraphatak.com/introduction-to-spark-two-part-2/>`_
  — scala examples



|

R
--------


* `SparkR in Databricks <https://docs.databricks.com/spark/latest/sparkr/index.html>`_
  — the reference for SparkR





|

Hail 0.2
--------


* `Hail Site <https://hail.is/>`_
  — core page for Hail


* `Hail Github <https://github.com/hail-is/hail>`_
  — core github for Hail

  
* `Hail on AWS EMR  <https://github.com/hms-dbmi/hail-on-EMR>`_




|

Next Generation DNA Sequencing (NGS)
---------------------------------------


* `Genetics Home Reference  <https://ghr.nlm.nih.gov/>`_
  — an introduction Genetics

* `What is DNA <https://ghr.nlm.nih.gov/primer/basics/dna>`_
  — DNA breakdown

* `VCF  <https://faculty.washington.edu/browning/intro-to-vcf.html#example>`_
  — an introduction to the genomic Variant Call Format file type 

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

* `pyspark transformations <https://nbviewer.jupyter.org/github/jkthompson/pyspark-pictures/blob/master/pyspark-pictures.ipynb>`_
  — really good overviews of the transformations possible 


* `json lines (not json) <http://jsonlines.org/>`_
  —  this page describes the JSON Lines text format, also called newline-delimited JSON. JSON Lines is a convenient format for storing structured data that may be processed one record at a time. It works well with unix-style text processing tools and shell pipelines. It's a great format for log files. It's also a flexible format for passing messages between cooperating processes. SSON Lines handles tabular data cleanly and without ambiguity. Stream compressors like gzip or bzip2 are recommended for saving space, resulting in .jsonl.gz or .jsonl.bz2 files...

  



|

Explanatory Videos
-------------


* `Genetic Association Explained <https://www.youtube.com/watch?v=HIF73Hu1Vmw>`_
  — Written by Dmytro Kryvokhyzha, excellent overview of using Databricks in Scala with Hail


* `Practical Genomics with Apache Spark <https://databricks.com/session/practical-genomics-with-apache-spark>`_
  — Tom White is a data scientist at Cloudera, specializing in big data and bioinformatics. He also literally wrote the definitive guide on Hadoop, so he is solid. He goes over the big picture of genomics and that data being analyzed via parallel computing.  



|




Make Work
--------


* `error message  openCostinBytes  <https://stackoverflow.com/questions/49048212/how-to-set-spark-sql-files-conf-in-pyspark>`_



* `variant calls via scala <https://databricks.com/blog/2019/06/26/scaling-genomic-workflows-with-spark-sql-bgen-and-vcf-readers.html>`_



* `convert vcf files into delta lake <https://docs.databricks.com/_static/notebooks/genomics/vcf2delta.html>`_



* `zero point two <https://docs.databricks.com/applications/genomics/hail.html>`_



* `azurecln <https://www.blue-granite.com/blog/scaling-your-genomics-pipeline-to-the-cloud-with-azure-databricks>`_



* `colored cell insert box <https://www.ibm.com/support/knowledgecenter/en/SSGNPV_1.1.3/dsx/markd-jupyter.html>`_



* `incorporate slides from talk <https://www.slideshare.net/SparkSummit/hail-scaling-genetic-data-analysis-with-apache-spark-keynote-by-cotton-seed>`_


|
|
|


Final Notes
------------------------



Notes:: 

  

  When I got it working:
    * ENABLE_HAIL=true < - - confirm still updated .jar is pushed 
    * location of jar = = =  dbfs:/FileStore/jars/5698d3bc_4eae_4017_adc7_a960409bcd16-hail_all_spark-71440.jar
    *                                 5698d3bc_4eae_4017_adc7_a960409bcd16-hail_all_spark-71440.jar, 29914913))


  spark script init notes:  
  https://evodify.com/assets/posts/2017-11-08-big-data-tutorial/GenomicsSpark.html
  https://lamastex.github.io/scalable-data-science/sds/2/2/db/999_05_StudentProject_HailScalaGenomicsETLTutorial.html
  https://github.com/lamastex/scalable-data-science/blob/master/dbcArchives/2019/sds-2-x-geo.dbc
  http://www.wtwjasa.com/scaling-genomic-workflows-with-spark-sql-bgen-and-vcf-readers/





|
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
|
|




