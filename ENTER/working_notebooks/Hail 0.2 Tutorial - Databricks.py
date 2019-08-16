# Databricks notebook source
# MAGIC %md
# MAGIC ## Databricks - Genomics

# COMMAND ----------

# MAGIC %md
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC This may help to see the big picture:
# MAGIC *  https://en.wikipedia.org/wiki/1000_Genomes_Project

# COMMAND ----------

# MAGIC %md
# MAGIC <div class="alert alert-block alert-warning">
# MAGIC <b>Note:</b> There are a **lot** of dependencies to make this notebook work.  In the Appendix I list all of them...
# MAGIC </div>

# COMMAND ----------

# MAGIC %md 
# MAGIC This notebook is designed to provide a broad overview of Hail's functionality, with emphasis on the functionality to manipulate and query a genetic dataset. 
# MAGIC 
# MAGIC We walk through a genome-wide SNP association test, and demonstrate the need to control for confounding caused by population stratification.  Parts of this are taken from Hail's online tutorial series: 
# MAGIC 
# MAGIC 
# MAGIC *  https://hail.is/docs/0.2/tutorials/07-matrixtable.html

# COMMAND ----------

# MAGIC %md
# MAGIC READ:  Remember, you do NOT need to initiate a SparkSession (context) like you do in normal vanilla Apache Spark.  It is pre-built for you when you open up a Spark notebook in Databricks.  So don't re-create or double create spark sessions, it will fail...

# COMMAND ----------

import hail as hl
import hail.expr.aggregators as agg
hl.init(sc, idempotent=True)

# COMMAND ----------

# Looks very similar to Apache Spark when it initiates...

# COMMAND ----------

# side note:   it took me 42 days to make this work right.
# my advice:   sometimes its ok to ask for help.  
# advice2:     if your not first, you're last. 
# advice3:     if you are new to Apache Spark, don't start with a crazy complex genomics sequencing project as your first dive into it

# COMMAND ----------

from pprint import pprint
from bokeh.io import output_notebook, show
from bokeh.layouts import gridplot
from bokeh.models import Span
output_notebook()

# COMMAND ----------

from bokeh.embed import components, file_html
from bokeh.resources import CDN

def displayBokeh(p):
  html = file_html(p, CDN, "Chart")
  # display this html
  displayHTML(html)

# COMMAND ----------

# --- core files we will use for this --- 
vcf_path = '/databricks-datasets/hail/data-001/1kg_sample.vcf.bgz'
annotation_path = '/databricks-datasets/hail/data-001/1kg_annotations.txt'

# COMMAND ----------

# --- databricks actually comes with some genomics raw data for you to mess with ---
display(dbutils.fs.ls("/databricks-datasets/hail/data-001"))

# COMMAND ----------

# MAGIC %md ### Loading data from disk
# MAGIC 
# MAGIC Hail has its own internal data representation, called a MatrixTable. This is both an on-disk file format and a [Python object](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable). Here, we read a MatrixTable from DBFS.

# COMMAND ----------

mt = hl.import_vcf(vcf_path)

# COMMAND ----------

# MAGIC %md ### Data 
# MAGIC 
# MAGIC It's important to have easy ways to slice, dice, query, and summarize a dataset. Some of these methods are demonstrated below.

# COMMAND ----------

# MAGIC %md The [rows](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable.rows) method can be used to get a table with all the row fields in our MatrixTable. 
# MAGIC 
# MAGIC We can use `rows` along with [select](https://hail.is/docs/devel/hail.Table.html#hail.Table.select) to pull out 5 variants. The `select` method takes either a string refering to a field name in the table, or a Hail [Expression](https://hail.is/docs/devel/expr/expression.html#hail.expr.expression.Expression). Here, we leave the arguments blank to keep only the row key fields, `locus` and `alleles`.
# MAGIC 
# MAGIC Use the `show` method to display the variants.

# COMMAND ----------

mt.rows().select().show(5)

# COMMAND ----------



# COMMAND ----------

# MAGIC %md Here is how to peek at the first few sample IDs:

# COMMAND ----------

mt.s.show(5)

# COMMAND ----------

# MAGIC %md To look at the first few genotype calls, we can use [entries](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable.entries) along with `select` and `take`. The `take` method collects the first n rows into a list. Alternatively, we can use the `show` method, which prints the first n rows to the console in a table format. 
# MAGIC 
# MAGIC Try changing `take` to `show` in the cell below.

# COMMAND ----------

mt.entry.take(5)

# COMMAND ----------

# MAGIC %md ## Adding column fields
# MAGIC 
# MAGIC A Hail MatrixTable can have any number of row fields and column fields for storing data associated with each row and column. Annotations are usually a critical part of any genetic study. Column fields are where you'll store information about sample phenotypes, ancestry, sex, and covariates. Row fields can be used to store information like gene membership and functional impact for use in QC or analysis. 
# MAGIC 
# MAGIC In this tutorial, we demonstrate how to take a text file and use it to annotate the columns in a MatrixTable. 

# COMMAND ----------

# MAGIC %md The file provided contains the sample ID, the population and "super-population" designations, the sample sex, and two simulated phenotypes (one binary, one discrete).

# COMMAND ----------

# MAGIC %md This file can be imported into Hail with [import_table](https://hail.is/docs/devel/methods/impex.html#hail.methods.import_table). This method produces a [Table](https://hail.is/docs/devel/hail.Table.html#hail.Table) object. Think of this as a Pandas or R dataframe that isn't limited by the memory on your machine -- behind the scenes, it's distributed with Spark.

# COMMAND ----------

table = (hl.import_table(annotation_path, impute=True)
         .key_by('Sample'))

# COMMAND ----------

# MAGIC %md A good way to peek at the structure of a `Table` is to look at its `schema`. 

# COMMAND ----------

table.describe()

# COMMAND ----------

# MAGIC %md To peek at the first few values, use the `show` method:

# COMMAND ----------

table.show(width=100)

# COMMAND ----------

# MAGIC %md Now we'll use this table to add sample annotations to our dataset, storing the annotations in column fields in our MatrixTable. First, we'll print the existing column schema:

# COMMAND ----------

print(mt.col.dtype)

# COMMAND ----------

# MAGIC %md We use the [annotate_cols](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable.annotate_cols) method to join the table with the MatrixTable containing our dataset.

# COMMAND ----------

mt = mt.annotate_cols(**table[mt.s])

# COMMAND ----------

print(mt.col.dtype)

# COMMAND ----------

print(mt.col.dtype.pretty())

# COMMAND ----------

# MAGIC %md ## Query functions and the Hail Expression Language
# MAGIC 
# MAGIC Hail has a number of useful query functions that can be used for gathering statistics on our dataset. These query functions take Hail Expressions as arguments.
# MAGIC 
# MAGIC We will start by looking at some statistics of the information in our table. The [aggregate](https://hail.is/docs/devel/hail.Table.html#hail.Table.aggregate) method can be used to aggregate over rows of the table.

# COMMAND ----------

# MAGIC %md `counter` is an aggregation function that counts the number of occurrences of each unique element. We can use this to pull out the population distribution by passing in a Hail Expression for the field that we want to count by.

# COMMAND ----------

pprint(table.aggregate(agg.counter(table.SuperPopulation)))

# COMMAND ----------

# MAGIC %md `stats` is an aggregation function that produces some useful statistics about numeric collections. We can use this to see the distribution of the CaffeineConsumption phenotype.

# COMMAND ----------

pprint(table.aggregate(agg.stats(table.CaffeineConsumption)))

# COMMAND ----------

# MAGIC %md However, these metrics aren't perfectly representative of the samples in our dataset. Here's why:

# COMMAND ----------

table.count()

# COMMAND ----------

mt.count_cols()

# COMMAND ----------

# MAGIC %md Since there are fewer samples in our dataset than in the full thousand genomes cohort, we need to look at annotations on the dataset. We can use [aggregate_cols](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable.aggregate_cols) to get the metrics for only the samples in our dataset.

# COMMAND ----------

mt.aggregate_cols(agg.counter(mt.SuperPopulation))

# COMMAND ----------

pprint(mt.aggregate_cols(agg.stats(mt.CaffeineConsumption)))

# COMMAND ----------

# MAGIC %md The functionality demonstrated in the last few cells isn't anything especially new: it's certainly not difficult to ask these questions with Pandas or R dataframes, or even Unix tools like `awk`. But Hail can use the same interfaces and query language to analyze collections that are much larger, like the set of variants. 
# MAGIC 
# MAGIC Here we calculate the counts of each of the 12 possible unique SNPs (4 choices for the reference base * 3 choices for the alternate base). 
# MAGIC 
# MAGIC To do this, we need to get the alternate allele of each variant and then count the occurences of each unique ref/alt pair. This can be done with Hail's `counter` method.

# COMMAND ----------

snp_counts = mt.aggregate_rows(agg.counter(hl.Struct(ref=mt.alleles[0], alt=mt.alleles[1])))
pprint(snp_counts)

# COMMAND ----------

# MAGIC %md We can list the counts in descending order using Python's Counter class.

# COMMAND ----------

from collections import Counter
counts = Counter(snp_counts)
counts.most_common()

# COMMAND ----------

# MAGIC %md It's nice to see that we can actually uncover something biological from this small dataset: we see that these frequencies come in pairs. C/T and G/A are actually the same mutation, just viewed from from opposite strands. Likewise, T/A and A/T are the same mutation on opposite strands. There's a 30x difference between the frequency of C/T and A/T SNPs. Why?

# COMMAND ----------

# MAGIC %md The same Python, R, and Unix tools could do this work as well, but we're starting to hit a wall - the latest [gnomAD release](http://gnomad.broadinstitute.org/) publishes about 250 million variants, and that won't fit in memory on a single computer.
# MAGIC 
# MAGIC What about genotypes? Hail can query the collection of all genotypes in the dataset, and this is getting large even for our tiny dataset. Our 284 samples and 10,000 variants produce 10 million unique genotypes. The gnomAD dataset has about **5 trillion** unique genotypes.

# COMMAND ----------

# MAGIC %md Hail plotting functions allow Hail fields as arguments, so we can pass in the DP field directly here. If the range and bins arguments are not set, this function will compute the range based on minimum and maximum values of the field and use the default 50 bins.

# COMMAND ----------

p = hl.plot.histogram(mt.DP, range=(0,30), bins=30, title='DP Histogram', legend='DP')
displayBokeh(p)

# COMMAND ----------

# MAGIC %md ## Quality Control
# MAGIC 
# MAGIC QC is where analysts spend most of their time with sequencing datasets. QC is an iterative process, and is different for every project: there is no "push-button" solution for QC. Each time the Broad collects a new group of samples, it finds new batch effects. However, by practicing open science and discussing the QC process and decisions with others, we can establish a set of best practices as a community.

# COMMAND ----------

# MAGIC %md QC is entirely based on the ability to understand the properties of a dataset. Hail attempts to make this easier by providing the [sample_qc](https://hail.is/docs/devel/methods/genetics.html#hail.methods.sample_qc) method, which produces a set of useful metrics and stores them in a column field.

# COMMAND ----------

mt.col.describe()

# COMMAND ----------

mt = hl.sample_qc(mt)

# COMMAND ----------

mt.col.describe()

# COMMAND ----------

# MAGIC %md Plotting the QC metrics is a good place to start.

# COMMAND ----------

p = hl.plot.histogram(mt.sample_qc.call_rate, range=(.88,1), legend='Call Rate')
displayBokeh(p)

# COMMAND ----------

p = hl.plot.histogram(mt.sample_qc.gq_stats.mean, range=(10,70), legend='Mean Sample GQ')
displayBokeh(p)

# COMMAND ----------

# MAGIC %md Often, these metrics are correlated.

# COMMAND ----------

p = hl.plot.scatter(mt.sample_qc.dp_stats.mean, mt.sample_qc.call_rate, xlabel='Mean DP', ylabel='Call Rate')
displayBokeh(p)

# COMMAND ----------

# MAGIC %md Removing outliers from the dataset will generally improve association results. We can draw lines on the above plot to indicate outlier cuts.

# COMMAND ----------

p.renderers.extend(
    [Span(location=0.97, dimension='width', line_color='black', line_width=1),
     Span(location=4, dimension='height', line_color='black', line_width=1)])
displayBokeh(p)

# COMMAND ----------

# MAGIC %md We'll want to remove all samples that fall in the bottom left quadrant. 
# MAGIC 
# MAGIC It's easy to filter when we've got the cutoff values decided:

# COMMAND ----------

mt = mt.filter_cols((mt.sample_qc.dp_stats.mean >= 4) & (mt.sample_qc.call_rate >= 0.97))
print('After filter, %d/284 samples remain.' % mt.count_cols())

# COMMAND ----------

# MAGIC %md Next is genotype QC. To start, we'll print the post-sample-QC call rate. It's actually gone _up_ since the initial summary - dropping low-quality samples disproportionally removed missing genotypes.
# MAGIC 
# MAGIC Import the `hail.expr.functions` module.

# COMMAND ----------

call_rate = mt.aggregate_entries(agg.fraction(hl.is_defined(mt.GT)))
print('pre QC call rate is %.3f' % call_rate)

# COMMAND ----------

# MAGIC %md It's a good idea to filter out genotypes where the reads aren't where they should be: if we find a genotype called homozygous reference with >10% alternate reads, a genotype called homozygous alternate with >10% reference reads, or a genotype called heterozygote without a ref / alt balance near 1:1, it is likely to be an error.

# COMMAND ----------

ab = mt.AD[1] / hl.sum(mt.AD)

filter_condition_ab = ((mt.GT.is_hom_ref() & (ab <= 0.1)) |
                        (mt.GT.is_het() & (ab >= 0.25) & (ab <= 0.75)) |
                        (mt.GT.is_hom_var() & (ab >= 0.9)))

mt = mt.filter_entries(filter_condition_ab)

# COMMAND ----------

post_qc_call_rate = mt.aggregate_entries(agg.fraction(hl.is_defined(mt.GT)))
print('post QC call rate is %.3f' % post_qc_call_rate)

# COMMAND ----------

# MAGIC %md Variant QC is a bit more of the same: we can use the [variant_qc](https://hail.is/docs/devel/methods/genetics.html?highlight=variant%20qc#hail.methods.variant_qc) method to produce a variety of useful statistics, plot them, and filter.

# COMMAND ----------

mt.row.describe()

# COMMAND ----------

# MAGIC %md The [cache](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable.cache) is used to optimize some of the downstream operations.

# COMMAND ----------

mt = hl.variant_qc(mt).cache()

# COMMAND ----------

mt.row.describe()

# COMMAND ----------

qc_table = mt.rows()
qc_table = qc_table.select(gq_mean = qc_table.variant_qc.gq_stats.mean,
                           call_rate = qc_table.variant_qc.call_rate,
                           p_value_hwe = qc_table.variant_qc.p_value_hwe,
                           AAF = qc_table.variant_qc.AF[1],)

p1 = hl.plot.histogram(qc_table.gq_mean, range=(10,80), legend='Variant Mean GQ')

p2 = hl.plot.histogram(qc_table.AAF, range=(0,1), legend='Alternate Allele Frequency')

p3 = hl.plot.histogram(qc_table.call_rate, range=(.5,1), legend='Variant Call Rate')

p4 = hl.plot.histogram(qc_table.p_value_hwe, range=(0,1), legend='Hardy-Weinberg Equilibrium p-value')

g = gridplot([[p1, p2], [p3, p4]])
displayBokeh(g)

# COMMAND ----------

# MAGIC %md These statistics actually look pretty good: we don't need to filter this dataset. Most datasets require thoughtful quality control, though. The [filter_rows](https://hail.is/docs/devel/hail.MatrixTable.html#hail.MatrixTable.filter_rows) method can help!

# COMMAND ----------

# MAGIC %md ## Let's do a GWAS!
# MAGIC 
# MAGIC First, we need to restrict to variants that are : 
# MAGIC 
# MAGIC  - common (we'll use a cutoff of 1%)
# MAGIC  - uncorrelated (not in linkage disequilibrium)

# COMMAND ----------

common_mt = mt.filter_rows(mt.variant_qc.AF[1] > 0.01)

# COMMAND ----------

print('Samples: %d  Variants: %d' % (common_mt.count_cols(), common_mt.count_rows()))

# COMMAND ----------

# MAGIC %md These filters removed about 15% of sites (we started with a bit over 10,000). This is _NOT_ representative of most sequencing datasets! We have already downsampled the full thousand genomes dataset to include more common variants than we'd expect by chance.
# MAGIC 
# MAGIC In Hail, the association tests accept column fields for the sample phenotype and covariates. Since we've already got our phenotype of interest (caffeine consumption) in the dataset, we are good to go:

# COMMAND ----------

gwas = hl.linear_regression_rows(y=common_mt.CaffeineConsumption, x=common_mt.GT.n_alt_alleles(), covariates=[1.0])
gwas.row.describe()

# COMMAND ----------

# MAGIC %md Looking at the bottom of the above printout, you can see the linear regression adds new row fields for the beta, standard error, t-statistic, and p-value.
# MAGIC 
# MAGIC Hail makes it easy to make a [Q-Q (quantile-quantile) plot](https://en.wikipedia.org/wiki/Q–Q_plot).

# COMMAND ----------

p = hl.plot.qq(gwas.p_value)
displayBokeh(p)

# COMMAND ----------

# MAGIC %md ## Confounded!
# MAGIC 
# MAGIC The observed p-values drift away from the expectation immediately. Either every SNP in our dataset is causally linked to caffeine consumption (unlikely), or there's a confounder.
# MAGIC 
# MAGIC We didn't tell you, but sample ancestry was actually used to simulate this phenotype. This leads to a [stratified](https://en.wikipedia.org/wiki/Population_stratification) distribution of the phenotype. The solution is to include ancestry as a covariate in our regression. 
# MAGIC 
# MAGIC The [linear_regression](https://hail.is/docs/devel/methods/stats.html#hail.methods.linear_regression) method can also take column fields to use as covariates. We already annotated our samples with reported ancestry, but it is good to be skeptical of these labels due to human error. Genomes don't have that problem! Instead of using reported ancestry, we will use genetic ancestry by including computed principal components in our model.
# MAGIC 
# MAGIC The [pca](https://hail.is/docs/devel/methods/stats.html#hail.methods.pca) method produces eigenvalues as a list and sample PCs as a Table, and can also produce variant loadings when asked. The [hwe_normalized_pca](https://hail.is/docs/devel/methods/genetics.html#hail.methods.hwe_normalized_pca) method does the same, using HWE-normalized genotypes for the PCA.

# COMMAND ----------

pca_eigenvalues, pca_scores, _ = hl.hwe_normalized_pca(common_mt.GT)

# COMMAND ----------

pprint(pca_eigenvalues)

# COMMAND ----------

pca_scores.show(5, width=100)

# COMMAND ----------

# MAGIC %md Now that we've got principal components per sample, we may as well plot them! Human history exerts a strong effect in genetic datasets. Even with a 50MB sequencing dataset, we can recover the major human populations.

# COMMAND ----------

p = hl.plot.scatter(pca_scores.scores[0], pca_scores.scores[1],
                    label=common_mt.cols()[pca_scores.s].SuperPopulation,
                    title='PCA', xlabel='PC1', ylabel='PC2')
displayBokeh(p)

# COMMAND ----------

# MAGIC %md Now we can rerun our linear regression, controlling for sample sex and the first few principal components. We'll do this with input variable the number of alternate alleles as before, and again with input variable the genotype dosage derived from the PL field.

# COMMAND ----------

cmt = common_mt.annotate_cols(pca = pca_scores[common_mt.s])

linear_regression_results = hl.linear_regression_rows(
    y=cmt.CaffeineConsumption, x=cmt.GT.n_alt_alleles(),
    covariates=[1.0, cmt.isFemale, cmt.pca.scores[0], cmt.pca.scores[1], cmt.pca.scores[2]])

# COMMAND ----------

p = hl.plot.qq(linear_regression_results.p_value)
displayBokeh(p)

# COMMAND ----------

# MAGIC %md We can also use the genotype dosage (the probability-weighted expected number of alternate alleles) instead of the hard call in our regression

# COMMAND ----------

def plDosage(pl):
    linear_scaled = pl.map(lambda x: 10 ** (-x / 10))
    pl_sum = hl.sum(linear_scaled)
    normed = linear_scaled / pl_sum
    return 1 * normed[1] + 2 * normed[2]

# COMMAND ----------

linear_regression_results = hl.linear_regression_rows(
    y=cmt.CaffeineConsumption, x=plDosage(cmt.PL),
    covariates=[1.0, cmt.isFemale, cmt.pca.scores[0], cmt.pca.scores[1], cmt.pca.scores[2]])

# COMMAND ----------

p = hl.plot.qq(linear_regression_results.p_value)
displayBokeh(p)

# COMMAND ----------

# MAGIC %md That's more like it! We may not be publishing ten new coffee-drinking loci in _Nature_, but we shouldn't expect to find anything but the strongest signals from a dataset of 284 individuals anyway. 

# COMMAND ----------

# MAGIC %md ## Rare variant analysis
# MAGIC 
# MAGIC Here we'll demonstrate how one can use the expression language to group and count by any arbitrary properties in row and column fields. Hail also implements the sequence kernel association test (SKAT).

# COMMAND ----------

entries = mt.entries()
results = (entries.group_by(pop = entries.SuperPopulation, chromosome = entries.locus.contig)
      .aggregate(n_het = agg.count_where(entries.GT.is_het())))

# COMMAND ----------

results.show()

# COMMAND ----------

# MAGIC %md What if we want to group by minor allele frequency bin and hair color, and calculate the mean GQ?

# COMMAND ----------

entries = entries.annotate(maf_bin = hl.cond(entries.info.AF[0]<0.01, "< 1%", 
                             hl.cond(entries.info.AF[0]<0.05, "1%-5%", ">5%")))

results2 = (entries.group_by(af_bin = entries.maf_bin, purple_hair = entries.PurpleHair)
      .aggregate(mean_gq = agg.stats(entries.GQ).mean, 
                 mean_dp = agg.stats(entries.DP).mean))

# COMMAND ----------

results2.show()

# COMMAND ----------

# MAGIC %md We've shown that it's easy to aggregate by a couple of arbitrary statistics. This specific examples may not provide especially useful pieces of information, but this same pattern can be used to detect effects of rare variation:
# MAGIC 
# MAGIC  - Count the number of heterozygous genotypes per gene by functional category (synonymous, missense, or loss-of-function) to estimate per-gene functional constraint
# MAGIC  - Count the number of singleton loss-of-function mutations per gene in cases and controls to detect genes involved in disease

# COMMAND ----------

# MAGIC %md
# MAGIC <br>
# MAGIC <br>

# COMMAND ----------

# MAGIC %md
# MAGIC # Tutorial on MatrixTable

# COMMAND ----------

# MAGIC %md
# MAGIC A `MatrixTable` has four kinds of fields:
# MAGIC *  global fields
# MAGIC *  row fields
# MAGIC *  column fields
# MAGIC *  entry fields

# COMMAND ----------

from bokeh.io import output_notebook, show
output_notebook()

# COMMAND ----------

# MAGIC %fs
# MAGIC ls

# COMMAND ----------

# MAGIC %md
# MAGIC Ok, if you want to get really really tricky here, you could go to the Hail Github location, where they actually have independent files that are scripts in python to pull down enormous amounts of genomics data.  Think a million wgets pulling down data, if you do it right...

# COMMAND ----------

# MAGIC %md
# MAGIC * https://github.com/hail-is/hail/tree/master/datasets/load

# COMMAND ----------

print("""
Example:  We could infiltrate this...

ht_samples = hl.read_table('gs://hail-datasets-hail-data/1000_Genomes_phase3_samples.ht')
ht_relationships = hl.read_table('gs://hail-datasets-hail-data/1000_Genomes_phase3_sample_relationships.ht')

mt = hl.import_vcf(
    'gs://hail-datasets-raw-data/1000_Genomes/1000_Genomes_phase3_chr{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22}_GRCh37.vcf.bgz',
    reference_genome='GRCh37')

mt = mt.annotate_cols(**ht_samples[mt.s])
mt = mt.annotate_cols(**ht_relationships[mt.s])

mt_split = hl.split_multi(mt)
mt_split = mt_split.select_entries(GT=hl.downcode(mt_split.GT, mt_split.a_index))
mt_split = mt_split.annotate_rows(info=hl.struct(
    CIEND=mt_split.info.CIEND[mt_split.a_index - 1],
    CIPOS=mt_split.info.CIPOS[mt_split.a_index - 1],
    CS=mt_split.info.CS,
    END=mt_split.info.END,
    IMPRECISE=mt_split.info.IMPRECISE,
    MC=mt_split.info.MC,
    MEINFO=mt_split.info.MEINFO,
    MEND=mt_split.info.MEND,
    MLEN=mt_split.info.MLEN,
    MSTART=mt_split.info.MSTART,
    SVLEN=mt_split.info.SVLEN,
    SVTYPE=mt_split.info.SVTYPE,
    TSD=mt_split.info.TSD,
    AC=mt_split.info.AC[mt_split.a_index - 1],
    AF=mt_split.info.AF[mt_split.a_index - 1],
    NS=mt_split.info.NS,
    AN=mt_split.info.AN,
    EAS_AF=mt_split.info.EAS_AF[mt_split.a_index - 1],
    EUR_AF=mt_split.info.EUR_AF[mt_split.a_index - 1],
    AFR_AF=mt_split.info.AFR_AF[mt_split.a_index - 1],
    AMR_AF=mt_split.info.AMR_AF[mt_split.a_index - 1],
    SAS_AF=mt_split.info.SAS_AF[mt_split.a_index - 1],
    DP=mt_split.info.DP,
    AA=mt_split.info.AA,
    VT=(hl.case()
       .when((mt_split.alleles[0].length() == 1) & (mt_split.alleles[1].length() == 1), 'SNP')
       .when(mt_split.alleles[0].matches('<CN*>') | mt_split.alleles[1].matches('<CN*>'), 'SV')
       .default('INDEL')),
    EX_TARGET=mt_split.info.EX_TARGET,
    MULTI_ALLELIC=mt_split.info.MULTI_ALLELIC))

n_rows, n_cols = mt_split.count()
n_partitions = mt_split.n_partitions()

mt_split = hl.sample_qc(mt_split)
mt_split = hl.variant_qc(mt_split)

mt_split = mt_split.annotate_globals(
    metadata=hl.struct(
        name='1000_Genomes_phase3_autosomes',
        reference_genome='GRCh37',
        n_rows=n_rows,
        n_cols=n_cols,
        n_partitions=n_partitions))

mt_split.write('gs://hail-datasets-hail-data/1000_Genomes_phase3_autosomes.GRCh37.mt', overwrite=True)

mt = hl.read_matrix_table('gs://hail-datasets-hail-data/1000_Genomes_phase3_autosomes.GRCh37.mt')
mt.describe()
print(mt.count())
""")

# COMMAND ----------

# import logging
# import os
# import cloudstorage as gcs
# import webapp2
# from google.appengine.api import app_identity

# COMMAND ----------

# This notebook file is getting big, I'm going to split it into the next notebook... stay tuned...
