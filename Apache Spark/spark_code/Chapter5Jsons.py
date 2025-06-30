import json
from pyspark import SparkConf, SparkContext

# Illustrates the difference between the joins.
# (Basically the exact same as SQL)

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)
input = sc.textFile("./Apache Spark/spark_code/file.json")
data = input.map(lambda x: json.loads(x))

print(data.collect())