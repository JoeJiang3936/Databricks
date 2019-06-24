-- Databricks notebook source
-- MAGIC %md  
-- MAGIC > This is showing how you can create a jupyter notebook as straight SQL, and you would then use % type commands to switch around. 

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ```
-- MAGIC   Im showing the ability to create a straight SQL apache spark notebook
-- MAGIC   
-- MAGIC   Because this is a SQL notebook, the next few commands use the %python magic command
-- MAGIC   
-- MAGIC ```

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 
-- MAGIC DataFrames: 
-- MAGIC 
-- MAGIC The Apache Spark DataFrame API provides a rich set of functions (select columns, filter, join, aggregate, and so on) that allow you to solve common data analysis problems efficiently. DataFrames also allow you to intermix operations seamlessly with custom Python, R, Scala, and SQL code. 

-- COMMAND ----------

-- MAGIC 
-- MAGIC %python
-- MAGIC 
-- MAGIC #  we will be importing an example Databricks dataset
-- MAGIC  
-- MAGIC #   Use the Spark CSV datasource with options specifying:
-- MAGIC #    - First line of file is a header
-- MAGIC #    - Automatically infer the schema of the data
-- MAGIC 
-- MAGIC data = spark.read.csv("/databricks-datasets/samples/population-vs-price/data_geo.csv", header="true", inferSchema="true")
-- MAGIC 
-- MAGIC data.cache() # Cache data for faster reuse
-- MAGIC 
-- MAGIC data = data.dropna() # drop rows with missing values
-- MAGIC 
-- MAGIC Now that you have created the data DataFrame, you can quickly access the data using standard Spark commands such as take(). 

-- COMMAND ----------

-- MAGIC 
-- MAGIC %python
-- MAGIC data.take(10)

-- COMMAND ----------

-- MAGIC 
-- MAGIC %python
-- MAGIC # use display command to view this in a table format, its pretty 
-- MAGIC display(data)

-- COMMAND ----------

-- MAGIC 
-- MAGIC 
-- MAGIC %python
-- MAGIC #  *BEFORE* you can issue SQL queries, you must save your data DataFrame as a temporary table:   
-- MAGIC #     Register table so it is accessible via SQL Context
-- MAGIC data.createOrReplaceTempView("data_geo")

-- COMMAND ----------


-- this is a SQL comment
-- Specify a SQL query to list the 2015 median sales price by state:
select `State Code`, `2015 median sales price` from data_geo


-- COMMAND ----------


-- Or, query for population estimate in the state of Washington:
select City, `2014 Population estimate` from data_geo where `State Code` = 'WA';



-- COMMAND ----------


-- An additional benefit of using the Databricks display() command is that you can quickly view this 
-- data with a number of embedded visualizations. Click the down arrow next to the Chart Button to display a list of visualization types:

select `State Code`, `2015 median sales price` from data_geo



-- COMMAND ----------

-- MAGIC %python
-- MAGIC #  this is a solid link to review:   https://docs.databricks.com/getting-started/spark/dataframes.html
-- MAGIC #  shows more examples...
