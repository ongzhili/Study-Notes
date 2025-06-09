# Apache Spark

## RDD (Resilient Distributed Dataset)

### Overview

RDDs are Spark's core abstractions for working with data.
- Immutable distributed collection of objects
    - A RDD internally is split into multiple **partitions**
        - Each partition can be computed on different clusters / nodes
    - Can contain any object
        - `JavaRDD<T>` in Java
- Works similarly to streams, where all work is chained.
    - 2 types of operations
        - Transformations
            - RDD -> RDD
        - Actions
            - RDD -> Not RDDs
    - Computed lazily, only evaluated when it is used in an action.
        - Similar contrast between `Stream` and `ArrayList` where memory is saved by not eagerly loading everything into memory.
        - Content of RDDs after computation can be stored in memory (or disk).
        - but are by default recomputed each time you run an action on the RDD

### Creating RDDs

2 Main ways of creating RDDs
- Loading an external dataset
    - More common for enterprise applications
        - Example: `sc.textFile("/path/to/file.md")`
- Paralellizing a collection in the program
    - `parallelize(list here)`
        - Java: `Arrays.asList("pandas", "i like pandas")`
        - Python: `["pandas", "I like pandas"]`
        - etc.
    - Not very applicable in enterprise applications since that requires your whole dataset to be in one machine
    - Good for learning though, since you can initialize a basic RDD and do stuff on it.

### Working with RDDs: Operations

As mentioned in [Overview](#overview), there are 2 types of operations on RDDs.

#### Transformations

Transformed RDDs are:
- Computed lazily
- Operates on 1 or more RDDs
    - `filter` takes in 1 RDDs
    - `union` takes in 2 RDDs
        - Pseudo-set operations are supported (like `intersection`, `union`, `subtract`, `cartesian`)
- Mostly element-wise (work on 1 element at a time)
    - Not all though.
- Use `flatMap` if you want to do a 1 to many mapping. (Returns `RDD<Type>` instead of `RDD<List<Type>>`)
- Examples:
    - Java: `exampleRDD.filter((String x) => x.contains("Java"))`
    - py: `exampleRDD.filter(lambda x: "Python" in x)`

The existing RDD is not mutated (**remember that RDDs are immutable**). A transformation simply returnsa pointer to an entirely new RDD.

Spark also keeps track of the transformations via a _lineage graph_
- Compute each RDD on demand
- Helps recover lost data

#### Actions

Return a final value  to the program / write data to external storage

- **Forces evaluation of transformations required for the RDD**, since they need to produce output.
- Examples:
    - `foreach`
        - Applies funtion to each element of the RDD. Returns nothing
    - `count`
        - Returns number of elments in RDD
    - `take(int)`
        - Takes first n elements
    - `collect`
        - Returns all elements from the RDD
        - That also means all the RDD content is expected to fit inside memory
        - Commonly used in unit tests to easily compare RDD values to expected values.
    - `reduce`
    - `fold` (Remember `accumulate` in CS1101s?)
        - `fold` is just `reduce` with a seed (a.k.a start with 0 for + or 1 for *)
    - `aggregate`
        - `aggregate` is different from `reduce` or `fold` as the input and output for the accumulation function does not have to be the same type.
            - e.g you want both the sum and count of a RDD. You can just use a pair `(sum, count)` in `aggregate` and supply:
                1. A function that adds an element to an accumulator (e.g py `lambda acc, value: (acc[0] + value, acc[1] + 1)`)
                2. A lambda that adds 2 accumulators together (e.g py `lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1]`)
- Note that every time an action is called, the entire RDD is recomputed by default.
    - [persistency](#persistence) can be toggled to prevent such behavior.

#### Converting between RDD types

Some functions are only available on RDDs of certain types
- e.g `mean()` and `variance()` on numeric RDDs / `join()` for Key/value pair RDDs.

How it behaves differs between prog langs
- `Scala`: Implicitly handled
    - Must `import org.apache.spark.SparkContext._`
- `Java`: Explicitly converted
    - e.g conversion to `DoubleRDD`: Instead of `Function<T, Double>` with `map()`, you supply `DoubleFunction<T>` using `mapToDouble()` 
- `Python`: Operation simply fails at runtime if incompatible

### Persistence
RDDs in spark are lazily evaluated.
- There are cases where you want to use the same RDD multiple times
    - Default behavior: Spark recomputes the RDD and all its dependencies each time you call an action
        - Very expensive!
    - In this case, we can ask Spark to persist the data via:
        - `rdd.persist(STORAGE_LEVEL)`
            - Note that `persist()` does not force evaluation.
        - The nodes that compute the RDD store their partitions.
            - That means, if the node that has data persisted on it fails, Spark will recompute the lost partitions when necessary.
        - Storage Levels:
            - `MEMORY_ONLY`
            - `MEMORY_ONLY_SER`
            - `MEMORY_AND_DISK`
            - `MEMORY_AND_DISK_SER`
            - `DISK_ONLY`
        - If the user attempts to cache too much data in memory, spark will evict old partitions using LRU cache policy.
            - If purely memory, partitions are recomputed when they are accessed.
            - If memory-disk, old partitions are written to disk.

## Special RDDs

### Key/Value pair RDDs (Pair RDDs)

Common in aggregation functions.

Often initial ETL (**E**xtract, **T**ransform, **L**oad) is done to convert the data into a Key/Value format.

Useful in many programs
- Example uses:
    - Act on each key in parallel
    - Regrouping data across network

#### Creating Pair RDDs

From a regular RDD:
- py and Scala: `map()` function into a (key, value) tuple.
- Java: No tuples. PairRDD is of type `JavaPairRDD<(key), (value)>`
    - Spark uses `scala.Tuple2`
        - Instantiated using `new Tuple2(e1, e2)`
        - Key: accessed using`._1()`
        - Value: accessed using`._2()`
    - Call `mapToPair(func)`, where func is of the class `PairFunction<(pdd type), (key type), (value type)>`

From an in-memory collection:
- py and Scala: `SparkContext.parallelize()` on a list of tuples
- Java: `SparkContext.parallelizePairs()` on a list of `Tuple2`s.

#### Transformations on Pair RDDs

- All standard RDD transformations
- Special functions (Examples include, but are not exclusive to):
    - `reduceByKey()`
        - Combines values with the same key
    - `groupByKey()`
        - Groups values with the same key
    - `mapValues()`
        - Apply function to value in key-value pair. Key is unchanged.
- In fact, transformations on Pair RDDs exist as well
    - `subtractByKey()`
        - Removes an element if its key is present in the other RDD
    - `join()`
        - Inner join
    - `cogroup()`
        - Group data sharing the same key

In fact, we can separate them into a different families of functions
- Aggregations
    - Some form of combining in place
        -`groupByKey()`
        -`reduceByKey()`

##### Common Usecases

###### Grouping Data
Aggregating values that share the same key together.
- We get a RDD of type `[K, Iterable[V]]`.

If data is unpaird or we want to use a different condition, we can use `groupBy` which takes in a function that can be applied to the RDD element to determine the key.
- We get a RDD of type `[K, Iterable[V]]` as well, but the key would be the result of `function(element)`

If you do intend on `reduce()` or `fold()`-ing the values afterwards, the per-key aggregation functions would be more efficient, as `groupBy(Key)` creates an extra list per key to hold its values, and simply using the aggregation function will avoid this inefficiency.

**Joins**

Basically the same idea as joins in SQL.
- Inner Join
    - RDD contains key/value pair of key matches
        - In the format `(key, (value1, value2))`
    - If multiple of the same key exists in 1 RDD, the resulting RDD will have every posible pair of values with that key.
- Outer Join
    - Left: All source RDD keys present
        - If present in source but not argument: value = None
    - Right: All argument RDD keys present
        - If present in argument but not source: vaue = None
    - Full: All keys present, value is none if no key exists in either RDD.
    - Implementation of Optional in that prog lang is used (Some and None)

**Sorting**

Custom sort order can be provided via a custom comparison function
- Java: `Comparator<>`
- Scala: `Ordering[type]`
- Python: A lambda function

Ascendng / Descending order can be toggled via an argument as well.

#### Actions on Pair RDDs

- All traditional actions
- `countByKey()` - Returns `(key, count)`
- `collectAsMap()` - Returns `(key, value)` map
- `lookup(key)` - Returns a list of values associated with provided key

## Data Partitioning

Consider the case where you have a large, relatively unchanging dataset, with small datasets coming in and running joins on them.

`join()` by default does not know anything about how the keys are partitioned in the dataset.
- Hence, both datasets are shuffled
    - Shuffling: Distributing data across cluster workers to process it in parallel.
    - Spark does this to ensure all the records with the same key are on the same node.
- If you do a partition, then `persist()` (especially if large disparity in data set size), you can avoid the shuffling of the big, unchanged RDD, as Spark only needs to shuffle the smaller RDDs and send them to the matching nodes that containing its corresponding hash.
    - Failure to `persist()` will result in the RDD re-partitioning the data every time. (aka shuffling again)
    - Which defeats the purpose of using `partitionBy()`

In Java / Scala, you can call `rdd.partitioner` to get its partitioner. Returns an `Optional`.
- If no partitioning: `None`
- Else: `Some(partitioner)`

You can also provide a custom `Partitioner` which looks like this:

```java
class SamplePartitioner<Integer> extends Partitioner {
    @Override
    public int numPartitions {
        ...
        // Returns number of partitions used
    }

    @Override
    public int getPartition(Object key) {
        ...
        // Returns which partition an object will be partitioned to
    }

    @Override
    public boolean equals(Object obj) {
        ...
        // Checks if 1 partitioner is equal to the other
    }

    @Override
    public int hashCode() {
        ... 
    }
}

```

Operations that benefit from partitioning
- Most group / join functions
    - e.g `join()`s, `reduceByKey()`, `lookup()`
- On operations involving a single RDD:
    - All values corresponding to some specific key will be computed on a single node
    - Final value is returned to master
- On operations involving 2 RDDs, partitioning will result in at least one of the RDDs to not be shuffled.

Operations that affect partitioning
- Spark does not check if your functions change the key.
- Hence, most operations will return a RDD without partitioner.

## Level of parallelism

Each RDD has a fixed number of partitions that determine the degree of parallelism.
- Spark will infer a sensible default value
- Can be fine-tuned for performance
    - a.k.a Improvable via performance testing potentially?

Partitionings themselves can also be changed
- `repartition()` shuffles teh data to create a new set of partitions.
    - This is a fairly expensive operation.
- `coalesce()` is more optimized, but only works if you are decreasng the number of RDD partitions. (a.k.a each partition is larger)


## Loading and Saving Data

Sandbox examples are loaded / saved on a native language collection (like `List`) or regular text files.

### File Formats

Some commonly supported file formats:
- `.txt`
    - Assume 1 entry per line
- `.json`
    - Most libs require 1 record per line
- `.csv`
- SequenceFiles
- Protocol buffers

### Text Files

#### Loading

The simplest file to read.
- 1 line = 1 element in RDD.
- `sc.textfile("path/to/file")`
- Possible to pass a directory too
    - All files in the directory will be loaded into the RDD
    - `wholeTextFiles()` can be used if files are small enough
        - Obtain Pair RDD. Key = filename, Value = entire file content
        - **DO NOT TRY THIS FOR LARGE FILES**

#### Saving

Outputting to text files is also simple
- `saveAsTextFile("file-name")`
- Creates a directory containing 1 file per computing node.

### JSON

Most popular way is to load `.json` as text file and using a JSON parser to map the values.
- Likewise, using a JSON serialization library to do the opposite direction.

#### Loading
- Works nicely if: **1 json record per row**.
    - Doesnt work with multiline json files.
- Else: load whole file, then parse each line.

- Recommended libraries:
    - py: standard lib
    - Scala / Java: Jackson

#### Saving

`data.map(<json_to_string_func>).saveAsTextFile(outputFile)`

### Comma-Separated Values / Tab-Separated values (CSV & TSV)

Often 1 record 1 line. Fields separated by a comma (or tab).

Common practice for first fow to contain field names.

#### Loading

Same strategy as JSON: We can load as text, then process it. No standardization of format though. Use a library that works with your format.

See: Example in `spark_code`

#### Saving

We can simply use something like a `DictWriter` in python's `csv` lib to map a record into the "field1, field2, field3" or "field1  field2  field3" csv/tsv respectively.

Then, we just run `saveAsTextFile()` to save to file.

### SequenceFiles

Previous 2 requies that we know the schema beforehand.

**Flat File** - Simple file containing tabular data (e.g 1 row is 1 record)

SequenceFiles are binary, but conceptually can be represented like this:
```
| Header (metadata) |
|--------------------|
| Key 1 (binary)   | Value 1 (binary) |
|--------------------|-----------------|
| Key 2 (binary)   | Value 2 (binary) |
|--------------------|-----------------|
| ...               | ...              |
```

#### Reading a SequenceFile
- `sc.sequenceFile(filename, type, corresponding Writable class)`

**Writable Classes**

Many of the common types have a Writable

| Type      | Writable                     |
|-----------|------------------------------|
| Integer   | IntWritable / VIntWritable   |
| Long      | LongWritable / VLongWritable |
| Float     | FloatWritable                |
| Double    | DoubleWritable               |
| Boolean   | BooleanWritable              |
| byte[]    | BytesWritable                |
| String    | Text                         |
| T[]       | ArrayWritable<TW>            |
| List<T>   | ArrayWritable<TW>            |
| Map<A, B> | MapWritable<AW, BW>          |

1. VInt / VLong writables are used when you have a large number of small numbers. (V means variable). Saves space compared to non-variable, where the same amount of bits is used to store a small number and a really large number
2. TW/AW/BW are the corresponding writable types of T,A,B.

If your type does not have a writable, you can implement it via the following:

**Creating a custom Writable class**
- Override from `org.apache.hadoop.io.Writable
```java
class xxxx extends Writable {
    @Override
    public void readFields(DataInput in) throws IOException {
        ...
    }

    @Override
    public void write(DataOutput out) throws IOException {
        ...
    }
}
```

