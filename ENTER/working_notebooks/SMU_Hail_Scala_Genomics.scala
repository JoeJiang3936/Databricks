// Databricks notebook source
// MAGIC %md
// MAGIC #  Working Notebook - Hail on Databricks via Scala code

// COMMAND ----------


//
//  Working on the very latest version of Databricks Runtime
//  Scala-based code
//  import hail = true to open start with correct Hail version
//


// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC `
// MAGIC ``

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC *  Find out the temporary name for the Hail 0.2 jar that is assigned to your jar file by Databricks:

// COMMAND ----------


// List out all of the jars in this Filestore ! 
// Hail 0.2 should be one of them ! ! ! 

dbutils.fs.ls("/FileStore/jars/")

//  res0: Seq[com.databricks.backend.daemon.dbutils.FileInfo] = WrappedArray(FileInfo(dbfs:/FileStore/jars/5698d3bc_4eae_4017_adc7_a960409bcd16-hail_all_spark-71440.jar,
//  5698d3bc_4eae_4017_adc7_a960409bcd16-hail_all_spark-71440.jar, 29914913))


// COMMAND ----------


val hailJar = dbutils.fs.ls("/FileStore/jars/")
  .map(_.name)
  .filter(_.contains("hail_all_spark"))
  .headOption
  .getOrElse(sys.error("Failed to find hail jar, make sure that steps above are run"))

println(s"Found the jar: $hailJar")

//   Found the jar: 5698d3bc_4eae_4017_adc7_a960409bcd16-hail_all_spark-71440.jar
//   hailJar: String = 5698d3bc_4eae_4017_adc7_a960409bcd16-hail_all_spark-71440.jar


// COMMAND ----------

// MAGIC %md
// MAGIC Copy this temporary jar file (`$hailJar`) to all executors:

// COMMAND ----------


dbutils.fs.put("/databricks/init/install_hail.sh", s"""
#!/bin/bash
mkdir -p /mnt/driver-daemon/jars
mkdir -p /mnt/jars/driver-daemon
cp /dbfs/FileStore/jars/$hailJar /mnt/driver-daemon/jars/ 
cp /dbfs/FileStore/jars/$hailJar /mnt/jars/driver-daemon/
""", true)


// COMMAND ----------

// MAGIC %md Restart the cluster and you are ready to go.

// COMMAND ----------

// MAGIC %md # Processing

// COMMAND ----------

// MAGIC %md
// MAGIC ## Import Hail and create Hail Context

// COMMAND ----------


spark

// output:  res2: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@264eeaa3


// COMMAND ----------

// just confirming they are running

sc

//   working output:  res4: org.apache.spark.SparkContext = org.apache.spark.SparkContext@41cd4f57


// COMMAND ----------

import org.apache.spark.ui.ConsoleProgressBar

// COMMAND ----------


import is.hail._

// working output: import is.hail._


// COMMAND ----------


val hc = HailContext(sc)

// working output:
// 2019-08-10 20:45:13 Hail: INFO: SparkUI: http://10.67.227.154:48136
// 2019-08-10 20:45:13 Hail: INFO: Running Hail version 0.1-5306854
// import is.hail._
// hc: is.hail.HailContext = is.hail.HailContext@5988bf17



// COMMAND ----------


hc

// output:  res1: is.hail.HailContext = is.hail.HailContext@5988bf17


// COMMAND ----------

// MAGIC %md ## Specify the path to files 
// MAGIC These files are already uploaded and available in Databricks. If you decide to use your own files, please upload them to Databricks and move to the dbfs file system.

// COMMAND ----------


val vcf_path =  "/databricks-datasets/hail/data-001/1kg_sample.vcf.bgz"
val annotation_path = "/databricks-datasets/hail/data-001/1kg_annotations.txt"

//  working output:  
//    vcf_path: String = /databricks-datasets/hail/data-001/1kg_sample.vcf.bgz
//    annotation_path: String = /databricks-datasets/hail/data-001/1kg_annotations.txt


// COMMAND ----------


println(hc)

// working output:  is.hail.HailContext@5988bf17


// COMMAND ----------

// MAGIC %md ## Import the VCF file

// COMMAND ----------

// MAGIC %md
// MAGIC ### Quick Sidebar:

// COMMAND ----------


dbutils.fs.ls("/FileStore/jars/")

//  var vds = hc.importVCF(vcf_path)



// COMMAND ----------

// MAGIC %fs ls

// COMMAND ----------

// MAGIC 
// MAGIC %fs ls dbfs:/databricks-datasets

// COMMAND ----------

// MAGIC 
// MAGIC %fs ls dbfs:/databricks-datasets/genomics

// COMMAND ----------

// MAGIC 
// MAGIC %fs ls dbfs:/databricks-datasets/genomics/1000G/	

// COMMAND ----------


fs ls dbfs:/databricks-datasets/genomics/1kg-vcfs/


// COMMAND ----------

// MAGIC 
// MAGIC %fs ls dbfs:/databricks-datasets/hail/data-001/
// MAGIC 
// MAGIC // working output:  
// MAGIC //   dbfs:/databricks-datasets/hail/data-001/1kg_annotations.txt	    1kg_annotations.txt	      22784
// MAGIC //   dbfs:/databricks-datasets/hail/data-001/1kg_sample.vcf.bgz	        1kg_sample.vcf.bgz	      39767725
// MAGIC //   dbfs:/databricks-datasets/hail/data-001/purcell5k.interval_list	purcell5k.interval_list	  192078

// COMMAND ----------



// COMMAND ----------

//%fs
// dbutils.fs.ls("dbfs:/databricks-datasets/")

dbutils.fs.ls("dbfs:/databricks-datasets/")


// COMMAND ----------



//  var vds = hc.importVCF(vcf_path)



// COMMAND ----------


var vds = hc.importVCF(vcf_path)  // if input.bgz doesn't work, try to load uncompressed data.


// COMMAND ----------





// COMMAND ----------

// MAGIC %md ## Split multi-allelic variants
// MAGIC 
// MAGIC This method splits multi-allelic variants into biallelic variants. For example, the variant `1:1000:A:T,C` would become two variants: `1:1000:A:T` and `1:1000:A:C`.

// COMMAND ----------

vds = vds.splitMulti()

// COMMAND ----------

// MAGIC %md ## Annotate samples
// MAGIC This step will load information on each sample from the sample annotations file.
// MAGIC 
// MAGIC First, we import the annotation table. `impute=true` will infer column types automatically.

// COMMAND ----------

val table = hc.importTable(annotation_path, impute=true).keyBy("Sample")

// COMMAND ----------

// MAGIC %md ### Print the annotation table

// COMMAND ----------

display(table.toDF(hc.sqlContext))

// COMMAND ----------

// MAGIC %md ### Apply the annotation schema to the VDS

// COMMAND ----------

vds = vds.annotateSamplesTable(table, root="sa")

// COMMAND ----------

// MAGIC %md ### Print schemas

// COMMAND ----------

// MAGIC %md Sample schema:

// COMMAND ----------

print(vds.saSignature)

// COMMAND ----------

// MAGIC %md %md You can also print it in a more human-readable format: 

// COMMAND ----------

print(vds.saSignature.schema.prettyJson)

// COMMAND ----------

// MAGIC %md Variant schema:

// COMMAND ----------

print(vds.vaSignature.schema.prettyJson)

// COMMAND ----------

// MAGIC %md
// MAGIC Global schema

// COMMAND ----------

// vds.global_schema() in Hail's python API
print(vds.globalSignature)

// COMMAND ----------

// MAGIC %md *We have not applied any global schema, so it is empty.*

// COMMAND ----------

// MAGIC %md ### Count the number of samples

// COMMAND ----------

// MAGIC %md Total number of samples:

// COMMAND ----------

vds.nSamples

// COMMAND ----------

// MAGIC %md Number of samples per population:

// COMMAND ----------

display(table.toDF(hc.sqlContext).groupBy("Population").count())

// COMMAND ----------

// MAGIC %md ## Explore the data

// COMMAND ----------

// MAGIC %md Print summary statistics:

// COMMAND ----------

print(vds.summarize())

// COMMAND ----------

// MAGIC %md
// MAGIC The above output shows:
// MAGIC 
// MAGIC * 710 - samples
// MAGIC * 10961 - variants 
// MAGIC * 0.988 - successfully called genotypes.
// MAGIC * 23 - chromosomes
// MAGIC * 0 - multiallelic variants
// MAGIC * 10961 - SNPs
// MAGIC * 0 - MNP alternate alleles
// MAGIC * 0 - insertions
// MAGIC * 0 - deletions
// MAGIC * 0 - complex alternate alleles
// MAGIC * 0 - Number of star (upstream deletion)
// MAGIC * 2 - Highest number of alleles at any variant.
// MAGIC 
// MAGIC All these annotation variables can be called separately with a few extra steps described below:

// COMMAND ----------

// MAGIC %md Save the summarize output as a separate object:

// COMMAND ----------

val sumVDS = vds.summarize()

// COMMAND ----------

// MAGIC %md Now, place a dot after the summarize object and press TAB. You will be displayed all available variable. Select the variable of interest:

// COMMAND ----------

// sumVDS.       // remove the two back slashes "//" in front of the command, place the cursor after the dot and press TAB to see avaliable options.

// COMMAND ----------

// MAGIC %md ## Filter genotypes
// MAGIC 
// MAGIC Let's filter genotypes based on genotype quality (GQ) and read coverage (DP).
// MAGIC 
// MAGIC Here `g` is genotype, `v` is variant, `s` is sample, and annotations are accessible via `va`, `sa`, and `global`. 

// COMMAND ----------

// MAGIC %md Genotype quality is measured with a Phred quality score. You can read more about it in the next cell.

// COMMAND ----------

// This allows easy embedding of publicly available information into any other notebook
// when viewing in git-book just ignore this block - you may have to manually chase the URL in frameIt("URL").
// Example usage:
// displayHTML(frameIt("https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation#Topics_in_LDA",250))
def frameIt( u:String, h:Int ) : String = {
      """<iframe 
 src=""""+ u+""""
 width="95%" height="""" + h + """"
 sandbox>
  <p>
    <a href="http://spark.apache.org/docs/latest/index.html">
      Fallback link for browsers that, unlikely, don't support frames
    </a>
  </p>
</iframe>"""
   }
displayHTML(frameIt("https://en.wikipedia.org/wiki/Phred_quality_score",500))

// COMMAND ----------

// MAGIC %md ### Plot the genotype quality scores

// COMMAND ----------

// MAGIC %md Make a dataframe for genotypes:

// COMMAND ----------

val gtDF = vds.genotypeKT().flatten.toDF(hc.sqlContext)
display(gtDF)

// COMMAND ----------

// MAGIC %md Now extract the scores for genotype depth (`g.dp`) and genotype quality (`g.gq`) from the last column (`g`) with SQL.
// MAGIC 
// MAGIC There are many genotypes and using all of them make plotting computationally difficult. So, we will subset the score by randomly selecting 1% and limiting the number of rows to 3000. This should be enough to obtain general distributions and define cut-offs.

// COMMAND ----------

gtDF.createOrReplaceTempView("genotypes") 
val gtDFdpqc = spark.sql("SELECT g.dp as DEPTH, g.gq as GenQuality from genotypes WHERE g.dp IS NOT NULL AND g.gq IS NOT NULL and RAND() <= .01 LIMIT 3000")
display(gtDFdpqc)

// COMMAND ----------

// MAGIC %md Using Databricks built-in display option, make plots for the extracted scores:

// COMMAND ----------

display(gtDFdpqc)

// COMMAND ----------

// MAGIC %md From the plots, we can define that genotypes with genotype quality less than 10 and coverage less than 2 can be removed:

// COMMAND ----------

var vdsGfilter = vds.filterGenotypes("g.dp >= 2 && g.gq >= 10")

// COMMAND ----------

// MAGIC %md Check the average call rate in the filtered data:

// COMMAND ----------

print(vdsGfilter.summarize().callRate)

// COMMAND ----------

// MAGIC %md Remember, in the cmd 46, the call rate was 0.988. Now, the call rate is 0.84 because many genotypes were filtered out. 

// COMMAND ----------

// MAGIC %md ### Filter samples
// MAGIC If your dataset is large, you can also afford to remove samples with low call rate.

// COMMAND ----------

// MAGIC %md Calculate the samples quality scores:

// COMMAND ----------

vdsGfilter = vdsGfilter.sampleQC()

// COMMAND ----------

// MAGIC %md Extract the samples scores:

// COMMAND ----------

val saDF = vdsGfilter.samplesKT().flatten.toDF(hc.sqlContext)
display(saDF)

// COMMAND ----------

// MAGIC  %md 
// MAGIC Make a plot for `sa.qc.callRate`:

// COMMAND ----------

display(saDF)

// COMMAND ----------

// MAGIC %md Apply the filter:

// COMMAND ----------

var vdsGSfilter = vdsGfilter.filterSamplesExpr("sa.qc.callRate >= 0.60")

// COMMAND ----------

// MAGIC %md Check the results of filtering:

// COMMAND ----------

print(vdsGSfilter.summarize().samples)

// COMMAND ----------

// MAGIC %md There were 710 samples before, now there are 667 samples.

// COMMAND ----------

val saDFfilter = vdsGSfilter.samplesKT().flatten.toDF(hc.sqlContext)
display(saDFfilter)

// COMMAND ----------

// MAGIC %md ### Filter variants
// MAGIC We recommend to use the [GATK Best Practices](https://gatkforums.broadinstitute.org/gatk/discussion/2806/howto-apply-hard-filters-to-a-call-set) for assistance to define cut-off for variant scores.

// COMMAND ----------

// MAGIC %md First, we will annotate the variants because we removed some genotypes and samples, and this changed the scores. We will also use `cache()` for better performance.

// COMMAND ----------

vdsGSfilter = vdsGSfilter.variantQC().cache()

// COMMAND ----------

// MAGIC %md Then we will extract the annotation score to a data frame and show its content.

// COMMAND ----------

val vaDF = vdsGSfilter.variantsKT().flatten.toDF(hc.sqlContext)
display(vaDF)

// COMMAND ----------

// MAGIC %md Visualize any variant annotation score with Databricks plot options:

// COMMAND ----------

display(vaDF)

// COMMAND ----------

var vdsGSVfilter = vdsGSfilter.filterVariantsExpr("va.info.MQ >= 55.0 && va.info.QD >= 5.0")

// COMMAND ----------

// MAGIC %md Check how many sites have been removed:

// COMMAND ----------

print(vdsGSVfilter.summarize().variants)

// COMMAND ----------

// MAGIC %md There were 10961 variants beofre filtering. Now, there 10660 variant sites.

// COMMAND ----------

// MAGIC %md You can also make plots for the scores from the filtered dataset to make sure that all the filter worked as intended.

// COMMAND ----------

val vaDFfilter = vdsGSVfilter.variantsKT().flatten.toDF(hc.sqlContext)

// COMMAND ----------

display(vaDFfilter)

// COMMAND ----------

// MAGIC %md ## Write the filtered VDS to a file for future analyses

// COMMAND ----------

val out_path = "/1kg_filtered.vds"
vdsGSVfilter.write(out_path, overwrite=true)

// COMMAND ----------

// MAGIC %md After that you can simply load this already filtered file for the future analyses.

// COMMAND ----------

val vdsFiltered = hc.readVDS(out_path) 

// COMMAND ----------

// MAGIC %md ## PCA
// MAGIC 
// MAGIC To show you a simple analysis you can do with such genetic data, we will check if there is any genetic structure in this data. We will use a principal component analysis (PCA) for that.

// COMMAND ----------

val VDSpca = vdsFiltered.pca("sa.pca", k=2)

// COMMAND ----------

val pcaDF = VDSpca.samplesKT().flatten.toDF(hc.sqlContext)

// COMMAND ----------

// MAGIC %md Replace dots in column names because they are not recognized correctly by SQL

// COMMAND ----------

val pcaDFrenamed = pcaDF.toDF(pcaDF.columns.map(_.replace(".", "_")): _*)
display(pcaDFrenamed)

// COMMAND ----------

// MAGIC %md Extract the PCA scores to a dataframe.

// COMMAND ----------

pcaDFrenamed.createOrReplaceTempView("PCA") 
val pc12DF = spark.sql("SELECT sa_SuperPopulation as pop, sa_pca_PC1 as PC1, sa_pca_PC2 as PC2 from PCA")
display(pc12DF)

// COMMAND ----------

// MAGIC %md Make a scatterplot with `PC1` and `PC2`, and add `Pop` as a grouping key.

// COMMAND ----------

display(pc12DF)

// COMMAND ----------

// MAGIC %md You can see from this PCA that human genetic data is not homogeneous. There is a clear genetic differentiation between populations.

// COMMAND ----------

// MAGIC %md # Visualization
// MAGIC This pipeline can also be modified to make plots with R instead of Databricks' `display()`. R allows making more complex and more flexible plots.
// MAGIC 
// MAGIC Below is an example of an R plot for the PCA. The same approach can be applied to all plots above.

// COMMAND ----------

// MAGIC %md Create an R dataframe from a Spark object:

// COMMAND ----------

// MAGIC %r
// MAGIC rPCAdf <- as.data.frame(sql("SELECT sa_SuperPopulation as Population, sa_pca_PC1 as PC1, sa_pca_PC2 as PC2 from PCA"))
// MAGIC head(rPCAdf)

// COMMAND ----------

// MAGIC %md Using your favourite R library (*ggplot2* in this case), make a plot:

// COMMAND ----------

// MAGIC %r
// MAGIC library(ggplot2)
// MAGIC 
// MAGIC ggplot(rPCAdf, aes(x = PC1, y = PC2, color = Population)) + geom_point()

// COMMAND ----------

// MAGIC %md ## Summary
// MAGIC 
// MAGIC Data filtering:
// MAGIC 
// MAGIC  - Filter genotypes
// MAGIC  - Filter samples
// MAGIC  - Filter variants
// MAGIC  
// MAGIC 
// MAGIC *Variants can be filtered before samples filtering if samples are of greater priority in a study.*
// MAGIC 
// MAGIC Such genetic data can be analyzed in various ways. A PCA is just one simple example.
