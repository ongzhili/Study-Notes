# Run `pip install pyspark`

from pyspark import SparkConf, SparkContext


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

print(addr.leftOuterJoin(rating).collect())
print(addr.rightOuterJoin(rating).collect())
print(addr.join(rating).collect())