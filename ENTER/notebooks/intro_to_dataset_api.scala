// Databricks notebook source
// MAGIC %md
// MAGIC # Dataset API
// MAGIC 
// MAGIC In this notebook, we demonstrate the new Dataset API in Spark 2.0, using a very simple JSON file.
// MAGIC 
// MAGIC To read the companion blog post, click here: https://databricks.com/blog/2016/05/11/spark-2-0-technical-preview-easier-faster-and-smarter.html

// COMMAND ----------

// You can access files in DBFS using the Databricks CLI, DBFS API, Databricks Utilities, Spark APIs, and local file APIs.

// COMMAND ----------

// List files in DBFS
// dbfs ls

// COMMAND ----------

// PLEASE TELL ME THE LOCATION OF ALL OF YOUR FILES ! ! ! ! !   // 

%fs ls /databricks-datasets

// COMMAND ----------

// MAGIC %fs ls /databricks-datasets/Rdatasets/data-001/datasets.csv

// COMMAND ----------

# List files in DBFS
%fs ls 

// COMMAND ----------

// MAGIC %fs ls dbfs/home

// COMMAND ----------



// COMMAND ----------

import scala.io.Source

val filename = "/dbfs/home/webinar/person.json"
for (line <- Source.fromFile(filename).getLines()) {
  println(line)
}

// COMMAND ----------

// Take a look at the content of the file
dbutils.fs.head("/home/webinar/person.json")

// COMMAND ----------

// MAGIC %md
// MAGIC ### Creating DataFrames and Datasets
// MAGIC 
// MAGIC Starting Spark 2.0, a DataFrame is simply a type alias for Dataset of Row. There are many ways to create DataFrames and Datasets.
// MAGIC 
// MAGIC The first way, used primarily in testing and demos, uses the range function available on SparkSession.

// COMMAND ----------

// range(100) creates a Dataset with 100 elements, from 0 to 99.
val range100 = spark.range(100)
range100.collect()

// COMMAND ----------

// MAGIC %md
// MAGIC The second way, which is probably the most common way, is to create a DataFrame/Dataset by referencing some files on external storage systems.

// COMMAND ----------

// Read the data in as a DataFrame
val jsonData = spark.read.json("/home/webinar/person.json")

// COMMAND ----------

display(jsonData)

// COMMAND ----------

// DataFrame is just an alias for Dataset[Row]
import org.apache.spark.sql.Dataset
val jsonDataset: Dataset[Row] = jsonData

// COMMAND ----------

// MAGIC %md
// MAGIC Databricks' display works on both DataFrames and Datasets.

// COMMAND ----------

display(jsonDataset)

// COMMAND ----------

// MAGIC %md
// MAGIC DataFrame (or Dataset of Row) is great, but sometimes I want compile-time type safety and we would to be able to work with my own domain-specific objects. Here we demonstrate how to turn an untyped Dataset into a typed Dataset.

// COMMAND ----------

// First, define my domain specific class
case class Person(email: String, iq: Long, name: String)

// Turn a generic DataFrame into a Dataset of Person
val ds = spark.read.json("/home/webinar/person.json").as[Person]

// COMMAND ----------

// MAGIC %md
// MAGIC ### Metadata operations
// MAGIC 
// MAGIC There are a few metadata operations that are very handy for Datasets.

// COMMAND ----------

// Get the list of columns
ds.columns

// COMMAND ----------

// Get the schema of the underlying data structure.
ds.schema

// COMMAND ----------

// Explain the logical and physical query plan to compute the Dataset.
ds.explain(true)

// COMMAND ----------

// MAGIC %md
// MAGIC ### Typed Dataset API
// MAGIC 
// MAGIC Dataset includes a typed functional API similar to RDDs and Scala's own collection library. This API is available in Scala/Java, but not Python/R.

// COMMAND ----------

// Run a map
ds.map(_.name).collect()

// COMMAND ----------

// Run a filter
ds.filter(_.iq > 140).collect()

// COMMAND ----------

// Can also run agregations to compute total IQ and average IQ grouped by some key
// In this case we are just grouping by a constant 0, i.e. all records get grouped together
import org.apache.spark.sql.expressions.scala.typed
ds.groupByKey(_ => 0).agg(typed.sum(_.iq), typed.avg(_.iq)).collect()

// COMMAND ----------

// MAGIC %md
// MAGIC ### Untyped Dataset API (a.k.a. DataFrame API)
// MAGIC 
// MAGIC Dataset also includes untyped functions that return results in the form of DataFrames (i.e. Dataset[Row]). This API is available in all programming languages (Java/Scala/Python/R).

// COMMAND ----------

// The select function is similar to the map function, but is not typed (i.e. it returns a DataFrame)
ds.select("name").collect()

// COMMAND ----------

// Run some aggregations: note that we are using groupBy, which is different from the type safe groupByKey
import org.apache.spark.sql.functions.{sum, avg}
ds.groupBy().agg(sum("iq"), avg("iq")).collect()

// COMMAND ----------

// MAGIC %md
// MAGIC ### Interoperate with RDDs
// MAGIC 
// MAGIC A Dataset can be easily turned into an RDD.

// COMMAND ----------

ds.rdd

// COMMAND ----------

// MAGIC %md
// MAGIC Again, to read the companion blog post, click here: https://databricks.com/blog/2016/05/11/spark-2-0-technical-preview-easier-faster-and-smarter.html
