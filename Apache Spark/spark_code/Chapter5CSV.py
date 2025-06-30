from pyspark import SparkConf, SparkContext
import csv
from io import StringIO

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

# Basic csv parsing
lines = sc.textFile("./Apache Spark/spark_code/file.csv")
rdd = lines.map(lambda line: line.split(","))

header = rdd.first()
data_rdd = rdd.filter(lambda row: row != header)
print(data_rdd.collect())

# Using csv lib in py

def parse_csv(line):
    return next(csv.reader(StringIO(line)))

rdd = lines.map(parse_csv)
print(rdd.collect())


def loadLine(line):
    # line[0] = filename, line[1] = file content
    input = StringIO(line[1])
    reader = csv.DictReader(input, fieldnames=["one", "two", "three"])
    return reader
data = sc.wholeTextFiles("./Apache Spark/spark_code/file.csv").flatMap(loadLine)

print(data.collect())

def writeRecords(records):
    """Write out CSV lines"""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["one", "two", "three"])
    for record in records:
        writer.writerow(record)
    return [output.getvalue()]

data.mapPartitions(writeRecords).saveAsTextFile("./Apache Spark/spark_code/csv/output")