# Databricks notebook source
# MAGIC %md 
# MAGIC # Purpose

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC    Create a databricks notebook (as base python)
# MAGIC    
# MAGIC    Investigate the Databricks DBFS 
# MAGIC    
# MAGIC    Create and read Parquet files, and understand them better 
# MAGIC    
# MAGIC    Create and read JSON files, display etc 
# MAGIC    
# MAGIC    ```

# COMMAND ----------

# MAGIC %md  <br>

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Spark SQL provides support for both reading and writing Parquet files that automatically preserves the schema of the original data ! 

# COMMAND ----------

# Parquet is a columnar format that is supported by many other data processing systems. 

# Spark SQL provides support for both reading and writing Parquet files that automatically 
# preserves the schema of the original data. 

# When writing Parquet files, all columns are automatically converted to be nullable for compatibility reasons.

# COMMAND ----------

# MAGIC %md 

# COMMAND ----------

# MAGIC %md # Examine the spark context

# COMMAND ----------

# return all of the methods possible under this particular input object
def list_out_object_methods(your_object):
  for method in dir(your_object):
    if not method.startswith("_"):
      print(method)
      
# i.e. i create a spark object, but i want to see all the methods possible on 
# it, use this function.  It helps to list out ALL methods you can enter ! 

# COMMAND ----------

spark

# COMMAND ----------

# lets confirm we have a spark context created
# if you know me, u know i always do these first couple steps
sc

# COMMAND ----------

list_out_object_methods(spark)

# COMMAND ----------

# list all the methods for the spark context, in case you want to look around
list_out_object_methods(sc)   # then you just enter sc.<the method>

# COMMAND ----------

def gather_up_my_spark_session_infor_for_me(s):
  print("Apache Spark Version . . . . . . . . . . . ",s.version)
  print("Spark master . . . . . . . . . . . . . . . ",s.master)
  print("Core Python Version . . .  . . . . . . . . ",s.pythonVer)
  print("App Name . . . . . . . . . . . . . . . . . ",s.appName)
  print("spark URL  . . . . . . . . . . . . . . . . ",s.uiWebUrl)
  print("Spark Home . . . . . . . . . . . . . . . . ",s.sparkHome)
  print("Spark session started at   . . . . . . . . ",s.startTime)
  print("Spark defaultMinPartitions . . . . . . . . ",s.defaultMinPartitions)
  print("Spark defaultParallelism . . . . . . . . . ",s.defaultParallelism)
  print("Spark hadoopFile . . . . . . . . . . . . . ",s.hadoopFile)
  print("Spark user . . . . . . . . . . . . . . . . ",s.sparkUser)  

# COMMAND ----------

gather_up_my_spark_session_infor_for_me(sc)

# COMMAND ----------

# MAGIC %md <br>

# COMMAND ----------

# MAGIC %md  # Let's look at Parquet Files: 

# COMMAND ----------

# MAGIC %md
# MAGIC THE standard i think:
# MAGIC *  https://github.com/apache/parquet-format

# COMMAND ----------

# side note:  
# upload image to databricks DBFS
# it will show up under DBFS /FileStore/tables/<yourfilename>
# and then from there, IF you want to access the file for HTML image view:
#  /files/svm.jpg
# but for writing, it would be:
#  /FileStore/svm.jpg

# COMMAND ----------

# MAGIC %md
# MAGIC Parquet is a columnar file format that provides optimizations to speed up queries and is a far more efficient file format than CSV or JSON.
# MAGIC 
# MAGIC Parquet stores binary data in a column-oriented way, where the values of each column are organized so that they are all adjacent, enabling better compression. It is especially good for queries which read particular columns from a “wide” (with many columns) table since only needed columns are read and IO is minimized. 

# COMMAND ----------

# MAGIC %md
# MAGIC <img src ='/files/tables/parquet.gif'>

# COMMAND ----------

dbutils.fs.ls("/tmp")

# COMMAND ----------

dbutils.fs.ls("/databricks-datasets")

# COMMAND ----------

# path to file (flight data)
path = "/tmp/flights_parquet/Origin=DFW/part-00004-tid-6689744057697969040-c960f890-badf-4220-9b06-f4058ede2b08-105-79.c000.snappy.parquet"

# read and display the parquet file
parquetDF = spark.read.parquet(path)
display(parquetDF.head(7))


# COMMAND ----------

# side note
#   to completely remove a file:
#     -  dbutils.fs.rm("/tmp/databricks-df-example.parquet", True)

# COMMAND ----------

# MAGIC %md 
# MAGIC * Good link that talks about why parquet is awesome: https://databricks.com/glossary/what-is-parquet

# COMMAND ----------

# You have spark context running, but you also have sqlContext as well...
sqlContext  # confirm it is running...

# COMMAND ----------

# these are all the things i can 'do' to my DF:
list_out_object_methods(parquetDF)

# COMMAND ----------

# i want to know how many rows of data are in my parquet file:
parquetDF.count()

# COMMAND ----------

print(type(parquetDF))  # this is a DataFrame fyi 

# COMMAND ----------

# listing out the columns in the actual dataframe
parquetDF.columns

# very handy to use...

# COMMAND ----------

# i wish to output the column of 'Dest' that are unique entries:
parquetDF.select('Dest').distinct().show()  # like using show, it automatically limits output...

# COMMAND ----------

parquetDF.schema

# COMMAND ----------

list_out_object_methods(parquetDF)

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC 
# MAGIC All the methods on the DF that are possible:
# MAGIC 
# MAGIC agg
# MAGIC alias
# MAGIC approxQuantile
# MAGIC cache
# MAGIC checkpoint
# MAGIC coalesce
# MAGIC colRegex
# MAGIC collect
# MAGIC columns
# MAGIC corr
# MAGIC count
# MAGIC cov
# MAGIC createGlobalTempView
# MAGIC createOrReplaceGlobalTempView
# MAGIC createOrReplaceTempView
# MAGIC createTempView
# MAGIC crossJoin
# MAGIC crosstab
# MAGIC cube
# MAGIC describe
# MAGIC distinct
# MAGIC drop
# MAGIC dropDuplicates
# MAGIC drop_duplicates
# MAGIC dropna
# MAGIC dtypes
# MAGIC exceptAll
# MAGIC explain
# MAGIC fillna
# MAGIC filter
# MAGIC first
# MAGIC foreach
# MAGIC foreachPartition
# MAGIC freqItems
# MAGIC groupBy
# MAGIC groupby
# MAGIC head
# MAGIC hint
# MAGIC intersect
# MAGIC intersectAll
# MAGIC isLocal
# MAGIC isStreaming
# MAGIC is_cached
# MAGIC join
# MAGIC limit
# MAGIC localCheckpoint
# MAGIC na
# MAGIC orderBy
# MAGIC persist
# MAGIC printSchema
# MAGIC randomSplit
# MAGIC rdd
# MAGIC registerTempTable
# MAGIC repartition
# MAGIC repartitionByRange
# MAGIC replace
# MAGIC rollup
# MAGIC sample
# MAGIC sampleBy
# MAGIC schema
# MAGIC select
# MAGIC selectExpr
# MAGIC show
# MAGIC sort
# MAGIC sortWithinPartitions
# MAGIC sql_ctx
# MAGIC stat
# MAGIC storageLevel
# MAGIC subtract
# MAGIC summary
# MAGIC take
# MAGIC toDF
# MAGIC toJSON
# MAGIC toLocalIterator
# MAGIC toPandas
# MAGIC transform
# MAGIC union
# MAGIC unionAll
# MAGIC unionByName
# MAGIC unpersist
# MAGIC where
# MAGIC withColumn
# MAGIC withColumnRenamed
# MAGIC withWatermark
# MAGIC write
# MAGIC writeStream
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Use SQL direct commands, which i really like: 

# COMMAND ----------

# MAGIC %md
# MAGIC *Create a temporary table and then we can query it*

# COMMAND ----------

# MAGIC %md
# MAGIC <br>
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC # Parquet Example #2

# COMMAND ----------

# lets look at a large file
# File uploaded to /FileStore/tables/userdata1.parquet

# COMMAND ----------

# MAGIC %md
# MAGIC A good source of some parquet files:
# MAGIC * https://github.com/Teradata/kylo/tree/master/samples/sample-data/parquet

# COMMAND ----------

dbutils.fs.ls("dbfs:/FileStore/tables")    # you can see your file there

# COMMAND ----------

dataP = spark.read.parquet("dbfs:/FileStore/tables/userdata1.parquet")

# see how it infers the schema ? 



# -> Number of rows in the file: 1000
# -> Column details:
# column#		column_name		hive_datatype
# =====================================================
# 1		registration_dttm 	    timestamp
# 2		id 			            int
# 3		first_name 		        string
# 4		last_name 		        string
# 5		email 			        string
# 6		gender 			        string
# 7		ip_address 		        string
# 8		cc 			            string
# 9		country 		        string
# 10	birthdate 		        string
# 11	salary 			        double
# 12	title 			        string
# 13	comments 		        string



# COMMAND ----------

dataP.show(10)

# COMMAND ----------

# I can poll the schema directly
dataP.schema

# COMMAND ----------

# feeling lazy ? 

# upload parquet file, read it into dataframe in python, and then use 
# databrick's export 'Download csv' buttom (far right downward arrow) to
# download and view the csv form on your laptop...

# COMMAND ----------

dataP.count()  # 1,000 rows

# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC # Let's examine JSON

# COMMAND ----------

# i manually uploaded this file called json.json
# sidenote: If your cluster is running Databricks Runtime 4.0 and above, you can read JSON 
# files in single-line or multi-line mode. In single-line mode, a file can be split into 
# many parts and read in parallel.

# lets confirm i can see it in my storage: 
display(dbutils.fs.ls("dbfs:/FileStore/tables/json.json"))

# COMMAND ----------

randomDF = spark.read.json("dbfs:/FileStore/tables/json.json")

# COMMAND ----------

# this is my json.json file i uploaded:
#  {"string":"string1","int":1,"array":[1,2,3],"dict": {"key": "value1"}}
#  {"string":"string2","int":2,"array":[2,4,6],"dict": {"key": "value2"}}
#  {"string":"string3","int":3,"array":[3,6,9],"dict": {"key": "value3", "extra_key":extra_value3"}}


# but the cool part is that Spark infers the schema automatically
randomDF.printSchema

# COMMAND ----------

randomDF.show()

# COMMAND ----------

display(randomDF)

# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Another JSON example:

# COMMAND ----------

import json
import requests

# You’ll need to make an API request to the JSONPlaceholder service, so just use the requests 
# package to do the heavy lifting.
response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)


# COMMAND ----------

response.json()

# COMMAND ----------

todos == response.json()

# COMMAND ----------

type(todos)

# COMMAND ----------

todos[:4]

# COMMAND ----------

display(todos)

# COMMAND ----------

# MAGIC %md <br>

# COMMAND ----------

# MAGIC %md
# MAGIC ## another JSON example

# COMMAND ----------

dbutils.fs.put("/tmp/test.json", """
{"string":"string1","int":1,"array":[1,2,3],"dict": {"key": "value1"}}
{"string":"string2","int":2,"array":[2,4,6],"dict": {"key": "value2"}}
{"string":"string3","int":3,"array":[3,6,9],"dict": {"key": "value3", "extra_key": "extra_value3"}}
""", True)

# COMMAND ----------

testJsonData = sqlContext.read.json("/tmp/test.json")

display(testJsonData)

# COMMAND ----------

# MAGIC %sql 
# MAGIC     CREATE TEMPORARY TABLE jsonTable
# MAGIC     USING json
# MAGIC     OPTIONS (
# MAGIC       path "/tmp/test.json"
# MAGIC     )

# COMMAND ----------

# MAGIC %sql SELECT * FROM jsonTable

# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC # Databricks Delta Examination

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC >  *lets look at a deeper examination of parquet and delta, and if we can make some improvements*

# COMMAND ----------

# note in the real world, using non Databricks, you can just print out as well

flights = spark.read.format("csv") \
  .option("header", "true") \
  .option("inferSchema", "true") \
  .load("/databricks-datasets/asa/airlines/2008.csv")

# see how the schema is inferred ???

# COMMAND ----------

# write a parquet-based table using this flights data 
# i specifically partition by ORIGIN
# once i do this, it will spread files around, and breakout by folders of Origin

# flights.write.format("parquet").mode("overwrite").partitionBy("Origin").save("/tmp/flights_parquet_2")

# COMMAND ----------

# your output files
#   display(dbutils.fs.ls("dbfs:/tmp/flights_parquet"))  # you can see your file there

# COMMAND ----------

# 8 core files per origin, example shown:
#  display(dbutils.fs.ls("dbfs:/tmp/flights_parquet/Origin=DFW/"))  # you can see your file there

# COMMAND ----------

# seeing display command in action, side note:
# from pyspark.sql.functions import avg
# diamonds_df = spark.read.csv("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header="true", inferSchema="true")
# display(diamonds_df.select("color","price").groupBy("color").agg(avg("price")))

# COMMAND ----------

# lets look at one single subFile

curiousDF = sqlContext.read.parquet("dbfs:/tmp/flights_parquet/Origin=DFW/part-00004-tid-6689744057697969040-c960f890-badf-4220-9b06-f4058ede2b08-105-79.c000.snappy.parquet")

print("This individual dataset has the following number of rows: ", curiousDF.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Once step 1 completes, the "flights" table contains details of US flights for a year.
# MAGIC 
# MAGIC Next in Step 2, we run a query that get top 20 cities with highest monthly total flights on first day of week.

# COMMAND ----------

# so when you open up the tmp folder, you see a few hundred files distributed by 
# origin id of like DFW airport.  

# eight files per original

# ex: /tmp/flights_parquet/Origin=DFW/part-00000-tid-1227084317432497623-9bdbeb42-5722-4f94-9755-6801a612974e-421-79.c000.snappy.parquet

# COMMAND ----------

# MAGIC %md
# MAGIC #### step 2

# COMMAND ----------

# lets run a query:

from pyspark.sql.functions import count

# this has got to be a huge file, its consolidating everything 
flights_parquet = spark.read.format("parquet").load("/tmp/flights_parquet")

# query the huge file, breakout by day of week 1, groupby, and count totals
display(flights_parquet.filter("DayOfWeek=1").groupBy("Month","Origin").agg(count("*").alias("TotalFlights")).orderBy("TotalFlights", ascending=False).limit(20))

# this took 1.72 minutes ! 
# ran it again, and then it 2.46 minutes


# COMMAND ----------

print(type(flights_parquet))

# COMMAND ----------

flights_parquet.count()
# thats over 7 million rows dude, pretty hard core for a quick check ...

# COMMAND ----------

# very very good command for seeing the schema you have in place for the DF
#############################a
flights_parquet.printSchema()
#############################

# COMMAND ----------

flights_parquet.columns

# COMMAND ----------

# MAGIC %md
# MAGIC #### step 3

# COMMAND ----------

# MAGIC %md
# MAGIC Once step 2 completes, you can observe the latency with the standard "flights_parquet" table.
# MAGIC 
# MAGIC In step 3 and step 4, we do the same with a Databricks Delta table. This time, before running the query, we run the OPTIMIZE command with ZORDER to ensure data is optimized for faster retrieval.

# COMMAND ----------


# Step 3: Write a Databricks Delta based table using flights data
flights.write.format("delta").mode("overwrite").partitionBy("Origin").save("/tmp/flights_delta")


# COMMAND ----------


# Step 3 Continued: OPTIMIZE the Databricks Delta table

display(spark.sql("DROP TABLE  IF EXISTS flights"))

display(spark.sql("CREATE TABLE flights USING DELTA LOCATION '/tmp/flights_delta'"))
                  
display(spark.sql("OPTIMIZE flights ZORDER BY (DayofWeek)"))


# COMMAND ----------

# Step 4 : Rerun the query from Step 2 and observe the latency

flights_delta = spark.read.format("delta").load("/tmp/flights_delta")

display(flights_delta.filter("DayOfWeek=1").groupBy("Month","Origin").agg(count("*").alias("TotalFlights")).orderBy("TotalFlights", ascending=False).limit(20))

# its faster now 


# COMMAND ----------


#  HMMMMMMMM

#  it went from taking:  1.72 minutes (and then 2.46 mins)
#  to taking about    :  42.35 seconds
#  about 2.43X + faster...


# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Appendix:  Access DBFS and looking around at functionality

# COMMAND ----------

display(dbutils.fs)

# COMMAND ----------


#  write a temp file to DBFS with python i/o apis
#  then print it out 
#  all python based (base notebook is python when created)

#write a file to DBFS using python i/o apis
with open("/dbfs/tmp/test_dbfs.txt", 'w') as f:
  f.write("Apache Spark is the bomb\n")
  f.write("Tom Bresee was the bomb\n")
  f.write("Now Databricks is the bomb\n")
  f.write("Goodbye.")

# read the file
with open("/dbfs/tmp/test_dbfs.txt", "r") as f_read:
  for line in f_read:
    print (line)
    
# df.write.text("/tmp/foo.txt")


# COMMAND ----------

# When you’re using Spark APIs, you reference files with "/mnt/training/file.csv" or 
# "dbfs:/mnt/training/file.csv". If you’re using local file APIs, you must provide 
# the path under /dbfs, for example: "/dbfs/mnt/training/file.csv". You cannot use 
# a path under dbfs when using Spark APIs.

# COMMAND ----------

# MAGIC %scala
# MAGIC // Now read the file you just created from scala
# MAGIC 
# MAGIC import scala.io.Source
# MAGIC 
# MAGIC val filename = "/dbfs/tmp/test_dbfs.txt"  // what you just created 
# MAGIC 
# MAGIC for (line <- Source.fromFile(filename).getLines()) {
# MAGIC   println(line)
# MAGIC }

# COMMAND ----------

# create a directory called foobar
dbutils.fs.mkdirs("/foobar/")

# now if you go to your main menu, and then click Import and Explore Data,
# you will see this new folder you just created ! 

# COMMAND ----------

# put the verbage into the file 
dbutils.fs.put("/foobar/baz.txt", "Hello, World!")

# COMMAND ----------

# thats awesome, i blew out the free edition in the first two days... 

# COMMAND ----------

# list out all the folders you have in DBFS ! 
# this is really a 'dir' level command ! 

display(dbutils.fs.ls("dbfs:/"))

# COMMAND ----------

# lets look around into the Parquet folder you created earlier ! ! ! 

display(dbutils.fs.ls("dbfs:/tmp/testParquet"))

# COMMAND ----------

# wanna know something odd ?   
# you CANT put comments into the same cell as a filesystem magic command ! 
# what the what, it will erorr out, so it has to be a stand alone cell ! 

# COMMAND ----------

# try:
#     import jira.client
#     JIRA_IMPORTED = True

# except ImportError:
#     JIRA_IMPORTED = False
