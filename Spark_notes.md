# Apache Spark

## RDD (Resilient Distributed Dataset)

### Overview

RDDs are Spark's core abstractions for working with data.
- They are simply an immutable distributed collection of objects
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
- Mostly element-wise (work on 1 element at a time)
    - Not all though.
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
    - `count`
    - `take(int)`
    - `collect`
- Note that every time an action is called, the entire RDD is recomputed by default.
    - persistency can be toggled to prevent such behavior.
