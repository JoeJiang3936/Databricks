// Databricks notebook source
// MAGIC %md ## Quick Start Using Scala
// MAGIC * Using a Databricks notebook to showcase RDD operations using Scala
// MAGIC * Reference http://spark.apache.org/docs/latest/quick-start.html

// COMMAND ----------

// Take a look at the file system
display(dbutils.fs.ls("/databricks-datasets/samples/docs/"))

// COMMAND ----------

// In our case, we see the README.md file in the samples docs
// i.e.  dbfs:/databricks-datasets/samples/docs/README.md

// COMMAND ----------

sc

// COMMAND ----------

// Setup the textFile RDD to read the README.md file
//   Note this is lazy, as a lot of this stuff ends up being per design...

val textFile = sc.textFile("/databricks-datasets/samples/docs/README.md")

// COMMAND ----------

// MAGIC %md RDDs have ***actions***, which return values, and ***transformations***, which return pointers to new RDDs.

// COMMAND ----------

// When performing an action (like a count) this is when the textFile is read and aggregate calculated
//    Click on [View] to see the stages and executors
textFile.count()

// COMMAND ----------

// MAGIC %md
// MAGIC ## Scala Count (Jobs)
// MAGIC ![Scala Count Jobs](https://sparkhub.databricks.com/wp-content/uploads/2015/12/Scala-Count-Jobs-e1450067391785.png)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Scala Count (Stages)
// MAGIC * Notice how the file is read during the *.count()* action
// MAGIC * Many Spark operations are lazy and executed upon some action
// MAGIC ![Scala Count Jobs](https://sparkhub.databricks.com/wp-content/uploads/2015/12/Scala-Count-Stages-e1450067376679.png)

// COMMAND ----------

textFile

// COMMAND ----------

textFile.count()

// COMMAND ----------

textFile.uuid

// COMMAND ----------

// Output the first line from the text file
textFile.first()

// COMMAND ----------

// MAGIC %md 
// MAGIC Now we're using a filter ***transformation*** to return a new RDD with a subset of the items in the file.

// COMMAND ----------

// Filter all of the lines wihtin the RDD and output the first five rows
val linesWithSpark = textFile.filter(line => line.contains("Spark"))

// COMMAND ----------

// MAGIC %md Notice that this completes quickly because it is a transformation but lacks any action.  
// MAGIC * But when performing the actions below (e.g. count, take) then you will see the executions.

// COMMAND ----------

// Perform a count (action) 
linesWithSpark.count()

// COMMAND ----------

// Filter all of the lines wihtin the RDD and output the first five rows
linesWithSpark.collect().take(5).foreach(println)

// COMMAND ----------

// MAGIC %md ## Random Scala Testing

// COMMAND ----------

object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
  }
}
// prints out 'HelloWorld'

// COMMAND ----------

object MainObject{  
    def main(args:Array[String]){  
        print("Hello Scala")  
    }  
}  

// COMMAND ----------

1+2

// COMMAND ----------

println("Hello, world!")

// COMMAND ----------

val msg = "Hello, world!"

// COMMAND ----------

val msg2: java.lang.String = "Hello again, world!"

// COMMAND ----------

val msg3: String = "Hello yet again, world!"

// COMMAND ----------

println(msg)

// COMMAND ----------

var greeting = "Hello, world!"

// COMMAND ----------

println("Hello, world, from a script!")

// COMMAND ----------

println("Hello, Scala!");

// COMMAND ----------

val s = "hello"; println(s)

// COMMAND ----------

import scala.collection.mutable.HashMap

// COMMAND ----------

import scala.collection.immutable.{TreeMap, TreeSet}

// COMMAND ----------

"""the present string
spans three
lines."""

// COMMAND ----------

object Test {
   def main(args: Array[String]) {
      println("Hello\tWorld\n\n" );
   }
} 

// COMMAND ----------

var myVar : String = "Foo"
