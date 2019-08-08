// Databricks notebook source
// MAGIC %md
// MAGIC # Working with .csv files in Databricks

// COMMAND ----------

// MAGIC %md
// MAGIC > *to include examination from the perspective of scala, R, python, and SQL*

// COMMAND ----------

// MAGIC %md
// MAGIC > *written in Scala, but flips around instances...*

// COMMAND ----------

// MAGIC %md
// MAGIC <br>
// MAGIC <br>
// MAGIC <br>

// COMMAND ----------

// MAGIC %md
// MAGIC The diamonds .csv dataset is actually embedded within Databricks for your usage
// MAGIC * If you forget about the diamonds dataset (for instance it comes embedded with R as well), check out:   https://ggplot2.tidyverse.org/reference/diamonds.html

// COMMAND ----------

// MAGIC %scala 
// MAGIC 
// MAGIC val diamonds = sqlContext.read.format("csv")
// MAGIC   .option("header", "true")
// MAGIC   .option("inferSchema", "true")
// MAGIC   .load("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv")
// MAGIC 
// MAGIC display(diamonds)

// COMMAND ----------

// MAGIC %scala
// MAGIC 
// MAGIC diamonds.printSchema

// COMMAND ----------

// MAGIC %r 
// MAGIC 
// MAGIC library(SparkR)
// MAGIC diamonds <- read.df("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", source = "csv", header="true", inferSchema = "true")
// MAGIC 
// MAGIC display(diamonds)

// COMMAND ----------

// MAGIC %r
// MAGIC 
// MAGIC printSchema(diamonds)

// COMMAND ----------

// MAGIC %python
// MAGIC 
// MAGIC diamonds = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv')
// MAGIC 
// MAGIC display(diamonds)

// COMMAND ----------

// MAGIC %python
// MAGIC 
// MAGIC diamonds.printSchema()

// COMMAND ----------

// MAGIC %sql
// MAGIC -- mode "FAILFAST" will abort file parsing with a RuntimeException if any malformed lines are encountered
// MAGIC CREATE TEMPORARY TABLE temp_diamonds
// MAGIC   USING csv
// MAGIC   OPTIONS (path "/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header "true", mode "FAILFAST")

// COMMAND ----------

// MAGIC %sql SELECT * FROM temp_diamonds
