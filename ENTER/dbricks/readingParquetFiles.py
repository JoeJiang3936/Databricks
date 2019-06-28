# Databricks notebook source
# MAGIC %md 
# MAGIC # Purpose: 

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
# MAGIC ### Introduction:

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
# MAGIC <br>

# COMMAND ----------

# lets confirm we have a spark context created
# if you know me, u know i always do these first couple steps
sc

# COMMAND ----------

# list all the methods for the spark context, in case you want to look around
dir(sc)   # then you just enter sc.<the method>

# COMMAND ----------

# what is my apache version ? 
sc.version

# COMMAND ----------

# what is my specific python version ? 
sc.pythonVer

# COMMAND ----------

# what is my spark context app name ? 
sc.appName

# COMMAND ----------

# tell me my URL for seeing stages etc 
sc.uiWebUrl # etc etc type methods 

# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC # Let's look at Parquet Files: 

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
# MAGIC displayHTML("<img src ='/files/tables/parquet.gif'>")

# COMMAND ----------

# MAGIC %scala 
# MAGIC 
# MAGIC // lets use scala to manually create a tiny array and save as an Apache Parquet file ! 
# MAGIC 
# MAGIC case class MyCaseClass(key: String, group: String, value: Int, someints: Seq[Int], somemap: Map[String, Int])
# MAGIC 
# MAGIC // paralellize an array of data, then toDF() method
# MAGIC 
# MAGIC val dataframe = sc.parallelize(Array(MyCaseClass("a", "vowels", 1, Array(1), Map("a" -> 1)),
# MAGIC   MyCaseClass("b", "consonants", 2, Array(2, 2), Map("b" -> 2)),
# MAGIC   MyCaseClass("c", "consonants", 3, Array(3, 3, 3), Map("c" -> 3)),
# MAGIC   MyCaseClass("d", "consonants", 4, Array(4, 4, 4, 4), Map("d" -> 4)),
# MAGIC   MyCaseClass("e", "vowels", 5, Array(5, 5, 5, 5, 5), Map("e" -> 5)))
# MAGIC ).toDF()
# MAGIC 
# MAGIC 
# MAGIC // now write it to disk * AS parquet * 
# MAGIC // use:  dataframe method .write 
# MAGIC dataframe.write.mode("overwrite").parquet("/tmp/testParquet")  
# MAGIC 
# MAGIC 
# MAGIC // your output will include text like:
# MAGIC //  defined class MyCaseClass
# MAGIC //  dataframe: org.apache.spark.sql.DataFrame = [key: string, group: string ... 3 more fields]

# COMMAND ----------

# MAGIC %scala
# MAGIC // i want to see my raw data please 
# MAGIC display(dataframe)

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC // see how i use sqlContext to read the actual file ? 
# MAGIC 
# MAGIC val data = sqlContext.read.parquet("/tmp/testParquet")
# MAGIC // note:  use sqlContext.read.parquet to access 
# MAGIC 
# MAGIC // run this in databricks so you can see some of the cool outputs under the View Stage data
# MAGIC 
# MAGIC display(data)

# COMMAND ----------

# You have spark context running, but you also have sqlContext as well...
sqlContext  # confirm it is running...

# COMMAND ----------

# now lets use Python (not Scala), and read the parquet file you created

data2 = sqlContext.read.parquet("/tmp/testParquet")

display(data2)

# note in the real world, using non Databricks, you can just print out as well

# COMMAND ----------

data2.sql_ctx

# COMMAND ----------

# i want to know how many rows of data are in my data2 file:
data2.count()

# COMMAND ----------

print(type(data2))  # this is a DataFrame fyi 

# COMMAND ----------

# please list out my dataframe columns:
data2.columns

# COMMAND ----------

# i wish to output the column of group only:
display(data2.select('group'))

# COMMAND ----------

data2.schema

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Use SQL direct commands, which i really like: 

# COMMAND ----------

# MAGIC %md
# MAGIC *Create a temporary table and then we can query it*

# COMMAND ----------

# MAGIC %sql 
# MAGIC     CREATE TEMPORARY TABLE scalaTable
# MAGIC     USING parquet
# MAGIC     OPTIONS (
# MAGIC       path "/tmp/testParquet"
# MAGIC     )

# COMMAND ----------

# MAGIC %sql 
# MAGIC -- i love how you can use SQL directly in Databricks, its just freaking excellent
# MAGIC SELECT * FROM scalaTable

# COMMAND ----------

# MAGIC %sql 
# MAGIC -- i want the data record row where the value is '2':
# MAGIC SELECT * FROM scalaTable WHERE value = 2

# COMMAND ----------

# MAGIC %md
# MAGIC <br>
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC # Parquet Example #2

# COMMAND ----------

# lets look at a much larger file
# File uploaded to /FileStore/tables/userdata1.parquet

# COMMAND ----------

# MAGIC %md
# MAGIC A good source of some parquet files:
# MAGIC * https://github.com/Teradata/kylo/tree/master/samples/sample-data/parquet

# COMMAND ----------

display(dbutils.fs.ls("dbfs:/FileStore/tables"))  # you can see your file there

# COMMAND ----------

dataP = sqlContext.read.parquet("dbfs:/FileStore/tables/userdata1.parquet")

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

display(dataP)

# COMMAND ----------

# I can poll the schema directly
dataP.schema

# COMMAND ----------

# feeling lazy ? 

# upload parquet file, read it into dataframe in python, and then use 
# databrick's export 'Download csv' buttom (far right downward arrow) to
# download and view the csv form on your laptop...

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
display(dbutils.fs.ls("dbfs:/FileStore/tables"))

# COMMAND ----------

# this already exists
spark

# COMMAND ----------

# this already exists
sqlContext

# COMMAND ----------

# list methods, but without those annoying _ underlines 

for i in dir(sqlContext):
  if not i.startswith("_"): print(i)

# COMMAND ----------

randomDF = sqlContext.read.json("dbfs:/FileStore/tables/json.json")

# COMMAND ----------

# this is my json.json file i uploaded:
#  {"string":"string1","int":1,"array":[1,2,3],"dict": {"key": "value1"}}
#  {"string":"string2","int":2,"array":[2,4,6],"dict": {"key": "value2"}}
#  {"string":"string3","int":3,"array":[3,6,9],"dict": {"key": "value3", "extra_key":extra_value3"}}


# but the cool part is that Spark infers the schema automatically
randomDF.printSchema


# COMMAND ----------

display(randomDF)

# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC #### Another JSON example:

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

# MAGIC %md
# MAGIC #### another JSON example

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

flights.write.format("parquet").mode("overwrite").partitionBy("Origin").save("/tmp/flights_parquet")

# COMMAND ----------

# your output files
display(dbutils.fs.ls("dbfs:/tmp/flights_parquet"))  # you can see your file there

# COMMAND ----------

# 8 core files per origin, example shown:
display(dbutils.fs.ls("dbfs:/tmp/flights_parquet/Origin=DFW/"))  # you can see your file there

# COMMAND ----------

# seeing display command in action, side note:
# from pyspark.sql.functions import avg
# diamonds_df = spark.read.csv("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header="true", inferSchema="true")
# display(diamonds_df.select("color","price").groupBy("color").agg(avg("price")))

# COMMAND ----------

# lets look at one single subFile

curiousDF = sqlContext.read.parquet("dbfs:/tmp/flights_parquet/Origin=DFW/part-00000-tid-1227084317432497623-9bdbeb42-5722-4f94-9755-6801a612974e-421-79.c000.snappy.parquet")

print("This individual dataset has the following number of rows: ", curiousDF.count())

# COMMAND ----------

#

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
# thats over 7 million rows...

# COMMAND ----------

# very very good command for seeing the schema you have in place for the DF
#############################a
flights_parquet.printSchema()
#############################

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

# MAGIC %md
# MAGIC <br>

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

# read the verbage you just created
dbutils.fs.head("/foobar/baz.txt")

# COMMAND ----------

# remove the file you just created
dbutils.fs.rm("/foobar/baz.txt")

# COMMAND ----------

# list out all the folders you have in DBFS ! 
# this is really a 'dir' level command ! 

display(dbutils.fs.ls("dbfs:/"))
# see how you can see the folder 'foobar' you created earlier ? 

# COMMAND ----------

# lets look around
display(dbutils.fs.ls("dbfs:/tmp"))

# COMMAND ----------

# lets look around into the Parquet folder you created earlier ! ! ! 

display(dbutils.fs.ls("dbfs:/tmp/testParquet"))

# COMMAND ----------

# wanna know something odd ?   
# you CANT put comments into the same cell as a filesystem magic command ! 
# what the what, it will erorr out, so it has to be a stand alone cell ! 

# COMMAND ----------

# MAGIC %fs rm -r foobar

# COMMAND ----------

# MAGIC %fs ls

# COMMAND ----------


try:
    import jira.client
    JIRA_IMPORTED = True

except ImportError:
    JIRA_IMPORTED = False
