from pyspark import SparkConf, SparkContext

# Illustrates partitioning examples

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

userData = [
    (1, {
        "topics": ["a", "b", "c"]
    }),
    (2, {
        "topics": ["b", "c"]
    }),
    (3, {
        "topics": ["a", "c"]
    }),
]

events = [
    (1, "a"),
    (1, "b"),
    (1, "c"),
    (1, "d"),
    (2, "a"),
    (2, "b"),
    (3, "b"),
]

userd = sc.parallelize(userData)
evnts = sc.parallelize(events)

# Inefficient code
joined = userd.join(evnts)
offTopicVisits = joined.filter(lambda data: data[1][1] not in data[1][0]['topics'])
print(offTopicVisits.collect())

# Partitioned: Only events is shuffled
userd2 = sc.parallelize(userData).partitionBy(3).persist()
joined2 = userd2.join(evnts)
offTopicVisits = joined2.filter(lambda data: data[1][1] not in data[1][0]['topics'])
print(offTopicVisits.collect())