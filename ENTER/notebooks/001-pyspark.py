# Databricks notebook source
# MAGIC %md # Databricks 101

# COMMAND ----------

# Welcome to Databricks 

# COMMAND ----------

# MAGIC %md <br><br>

# COMMAND ----------

# MAGIC %md ### libraries: 

# COMMAND ----------

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyspark import SparkContext, SparkConf

# COMMAND ----------

# MAGIC %md <br><br>

# COMMAND ----------

# MAGIC %md ### some good links

# COMMAND ----------

# MAGIC %md
# MAGIC `
# MAGIC https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/346304/2168141618055043/484361/latest.html 
# MAGIC 
# MAGIC https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/346304/2168141618055194/484361/latest.html
# MAGIC `

# COMMAND ----------

# MAGIC %md <br><br>

# COMMAND ----------

# MAGIC %md ### Lets look at our pre-created spark session information:

# COMMAND ----------

# import pyspark
# from pyspark import SparkContext, SparkConf

# COMMAND ----------

"""existing SparkContext(app=Databricks Shell, master=local[8]) created by __init__ at /local_disk0/tmp/1559414106996-0/PythonShell.py:1060 """

# COMMAND ----------

# MAGIC %md ### sc. type commands:

# COMMAND ----------

print(sc)  # what is your current spark context ? 

# COMMAND ----------

print(sc.appName)

# COMMAND ----------

# to list all of the spark context sc. type commands possible
commands = dir(sc)
for i in commands: 
  if not i.startswith("_"): 
    print(i)

# COMMAND ----------

dir(sc)  # long version

# COMMAND ----------

sc.environment

# COMMAND ----------

sc.uiWebUrl   # this is the URL

# COMMAND ----------

sc.version   # spark version 

# COMMAND ----------

sc.getConf()

# COMMAND ----------

sc.startTime

# COMMAND ----------

sc.pythonVer   # python version 

# COMMAND ----------

print("You are running python version: ", sc.pythonVer)

# COMMAND ----------

# MAGIC %md <br><br><br>

# COMMAND ----------

# MAGIC %md ### Creating RDDs:

# COMMAND ----------

# MAGIC %md Parallelized collections are created by calling SparkContext’s parallelize method on an existing iterable or collection in your driver program. The elements of the collection are copied to form a distributed dataset that can be operated on in parallel. For example, here is how to create a parallelized collection holding the numbers 1 to 10:

# COMMAND ----------

data = [1, 2, 3, 4, 5, 6, 7, 8, 9,10]
distData = sc.parallelize(data)

# COMMAND ----------

distData.sum()  # add all the values in the RDD

# COMMAND ----------

distData.values()

# COMMAND ----------

distData.context   # context information 

# COMMAND ----------

distData.name

# COMMAND ----------

# nice way of listing all commands possible
for i in dir(distData):
  if not i.startswith("_"):
    print(i)

# COMMAND ----------

distData.count()      # how many elements do you have 
distData.min()        # min values 
distData.max()        # max value
distData.mean()       # mean value
distData.sum()        # sum of values
distData.stdev()      # standard deviation of the values in the dataset 
distData.variance()   # variance of the data 
distData.first()      # output the first value 
distData.id()         # id ? 
distData.isEmpty()    # are you empty dataset ?
distData.stats()      # like a python describe ish command 

# COMMAND ----------

print(distData.take(5))  # take first five values that we have in our DF

# COMMAND ----------

# MAGIC %md ### another RDD

# COMMAND ----------

firstDataFrame = spark.range(1000000)
print(firstDataFrame)

# COMMAND ----------



# COMMAND ----------

sc

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

# MAGIC %md # spark 

# COMMAND ----------

print(spark)

# COMMAND ----------

# command options:
for i in dir(spark): 
  if not i.startswith("_"):  
    print(i) 

# COMMAND ----------

spark.version

# COMMAND ----------

print(spark.sparkContext)

# COMMAND ----------

# MAGIC %md ### Creating a RDD by opening and importing a text file

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

# MAGIC %md ### Creating a RDD by paralellizing an existing list

# COMMAND ----------

a = range(100)
data = sc.parallelize(a)

# COMMAND ----------

# how many entries do i have ? 
data.count()

# COMMAND ----------

data.take(5)   # take first few elements

# COMMAND ----------



# COMMAND ----------

# MAGIC %md <br><br><br>

# COMMAND ----------

# MAGIC %md # sqlContext Information

# COMMAND ----------



# COMMAND ----------

# MAGIC %md <br><br><br>

# COMMAND ----------

# MAGIC %md # File Systems

# COMMAND ----------

# MAGIC %fs ls /databricks-datasets/Rdatasets/data-001/datasets.csv

# COMMAND ----------

dataPath = "/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv"
diamonds = sqlContext.read.format("com.databricks.spark.csv")\
  .option("header","true")\
  .option("inferSchema", "true")\
  .load(dataPath)
  

# COMMAND ----------

display(diamonds)

# COMMAND ----------

display(diamonds)

# COMMAND ----------

df1 = diamonds.groupBy("cut", "color").avg("price") # a simple grouping

df2 = df1\
  .join(diamonds, on='color', how='inner')\
  .select("`avg(price)`", "carat")
# a simple join and selecting some columns

# COMMAND ----------

df2.explain()

# COMMAND ----------

df2.count()

# COMMAND ----------

# MAGIC %md <br><br>

# COMMAND ----------

# MAGIC %md # Reading external files

# COMMAND ----------

# MAGIC %md PySpark can create distributed datasets from any storage source supported by Hadoop, including your local file system, HDFS, Cassandra, HBase, Amazon S3, etc. Spark supports text files, SequenceFiles, and any other Hadoop InputFormat.
# MAGIC 
# MAGIC Text file RDDs can be created using SparkContext’s textFile method. This method takes an URI for the file (either a local path on the machine, or a hdfs://, s3a://, etc URI) and reads it as a collection of lines. Here is an example invocation:

# COMMAND ----------

distFile = sc.textFile("data.txt")

# COMMAND ----------

print(lines)

# COMMAND ----------

lines.values()

# COMMAND ----------

lines.stats
