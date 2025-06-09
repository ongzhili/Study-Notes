from pyspark import SparkConf, SparkContext
import csv
from io import StringIO

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

# Basic csv parsing
lines = sc.textFile("./spark_code/file.csv")
rdd = lines.map(lambda line: line.split(","))

header = rdd.first()
data_rdd = rdd.filter(lambda row: row != header)
print(data_rdd.collect())

# Using csv lib in py

def parse_csv(line):
    return next(csv.reader(StringIO(line)))

rdd = lines.map(parse_csv)
print(rdd.collect())