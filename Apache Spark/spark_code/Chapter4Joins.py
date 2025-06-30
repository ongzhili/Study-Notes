# Run `pip install pyspark`

from pyspark import SparkConf, SparkContext

# Illustrates the difference between the joins.
# (Basically the exact same as SQL)

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

#  Joins Example

storeAddress = [
    ("Ritual", "1026 Valencia St"), 
    ("Philz", "748 Van Ness Ave"),
    ("Philz", "3101 24th St"), ("Starbucks", "Seattle")
]

storeRating = [
    ("Ritual", 4.9), 
    ("Philz", 4.8),
    ("Test", 0)
]

addr = sc.parallelize(storeAddress)
rating = sc.parallelize(storeRating)

# print("Left Outer Join:")
# print(addr.leftOuterJoin(rating).collect())
# print("Right Outer Join:")
# print(addr.rightOuterJoin(rating).collect())
# print("Inner Join:")
# print(addr.join(rating).collect())
# print("Full Outer Join:")
# print(addr.fullOuterJoin(rating).collect())

# f = open("./spark_code/test_file.txt")
addr.join(rating).saveAsTextFile("./Apache Spark/spark_code/test_file")