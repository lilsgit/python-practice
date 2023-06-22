# Framework 3: pyspark
from functools import reduce

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import count, max, sum, when, col

spark = SparkSession.builder \
    .appName('datasetExercise') \
    .master("local[*]") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

# Read the data from the csv file
df1 = spark.read.csv('dataset1.csv', header=True, inferSchema=True)
df2 = spark.read.csv('dataset2.csv', header=True, inferSchema=True)

# Cache the DataFrames for reuse
df1.cache()
df2.cache()

# Merge the two dataframes
df3_first_merge = df1.join(df2.hint("broadcast"), on='counter_party', how='inner')


# Function to calculate the metrics
def agg_group_by_cols(group_by_cols: [str], the_other_cols: [str]):
    count_expressions = [count(col_name).alias(col_name) for col_name in the_other_cols]
    sum_if = lambda pyspark_expr, col: sum(when(pyspark_expr, col).otherwise(0))

    return df3_first_merge \
        .groupBy(group_by_cols) \
        .agg(*count_expressions,
             max('rating').alias("max_rating"),
             sum_if(col("status") == "ARAP", col('value')).alias("sum_value_ARAP"),
             sum_if(col("status") == "ACCR", col('value')).alias("sum_value_ACCR"),
             ) \
        .select('legal_entity', 'counter_party', 'tier', 'max_rating', 'sum_value_ARAP', 'sum_value_ACCR')


# Generate all the group by pairs needed
def generate_all_pairs(*args):
    all_mappings = []
    for i in range(len(args)):
        group_by_name = [args[i]]
        the_rest_names = [args[j] for j in range(len(args)) if j != i]
        all_mappings.append((group_by_name, the_rest_names))
    return all_mappings


group_by_cols = ('legal_entity', 'counter_party', 'tier')
all_pairs = generate_all_pairs(*group_by_cols)

df5 = reduce(DataFrame.unionAll,
             [agg_group_by_cols(group_by_cols, the_other_cols) for group_by_cols, the_other_cols in all_pairs])
df5.show()
# +------------+-------------+----+----------+--------------+--------------+
# |legal_entity|counter_party|tier|max_rating|sum_value_ARAP|sum_value_ACCR|
# +------------+-------------+----+----------+--------------+--------------+
# |          L1|            6|   6|         6|            85|           100|
# |          L3|            6|   6|         6|           145|           205|
# |          L2|            6|   6|         6|          1020|           207|
# |           3|           C6|   3|         6|           145|            60|
# |           5|           C3|   5|         6|             5|           197|
# |           2|           C4|   2|         6|            40|           100|
# |           3|           C5|   3|         6|          1000|           115|
# |           3|           C1|   3|         3|            40|             0|
# |           2|           C2|   2|         3|            20|            40|
# |           3|            3|   1|         3|            40|             0|
# |           3|            3|   6|         6|           145|            60|
# |           5|            5|   3|         6|             5|           197|
# |           3|            3|   5|         6|          1000|           115|
# |           2|            2|   4|         6|            40|           100|
# |           2|            2|   2|         3|            20|            40|
# |          L1|           C4|   2|         6|            40|           100|
# |          L3|           C6|   3|         6|           145|            60|
# |          L2|           C2|   2|         3|            20|            40|
# |          L2|           C5|   3|         6|          1000|           115|
# |          L3|           C3|   3|         4|             0|           145|
# +------------+-------------+----+----------+--------------+--------------+
# only showing top 20 rows


# extra thoughts:
# grouping object:
# filter first - assign filter to different partition
# basic idea: using different nodes in spark
