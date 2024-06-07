# MapReduce Program for Full Inverted Index

## Introduction
This project involves creating a Full Inverted Index using a MapReduce program. An inverted index is a data structure used in information retrieval systems to map content to its locations in a set of documents. This project demonstrates the steps to implement a Full Inverted Index using Hadoop's MapReduce framework.

## Design
The design involves processing three files through the MapReduce pipeline, including the Mapper, Combiner, and Reducer stages, to produce the Full Inverted Index.

### File Contents
- **File 0**: "it is what it is"
- **File 1**: "what is it"
- **File 2**: "it is a banana"

### Mapper
The Mapper processes each file and emits key-value pairs where the key is a word and the value is a tuple containing the document ID and the position of the word in the document.

### Combiner
The Combiner locally aggregates the Mapper output to reduce the amount of data transferred to the Reducer.

### Reducer
The Reducer globally aggregates the Combiner output to form the Full Inverted Index, mapping each word to a list of tuples containing document IDs and positions.

## Implementation and Testing
### Step 1: Set Up the Environment
1. **Create the InvertedIndex.java file** in the Hadoop-3.4.0 directory.
2. **Compile the Java program** with Hadoop libraries.
3. **Package the compiled classes** into a JAR file:
   ```bash
   jar cf InvertedIndex.jar *.class
   ```
4. **Move the JAR file** to a new directory called `FullIndex`.

### Step 2: Prepare the HDFS
1. **Create the input directory** in HDFS:
   ```bash
   hdfs dfs -mkdir /tmp/inputfile
   ```
2. **Create the input files** with the specified contents:
   - file0: "it is what it is"
   - file1: "what is it"
   - file2: "it is a banana"
3. **Upload the files** to HDFS:
   ```bash
   hdfs dfs -put file0 file1 file2 /tmp/inputfile
   ```

### Step 3: Run the MapReduce Job
1. **Execute the Hadoop job** using the InvertedIndex.jar:
   ```bash
   hadoop jar /home/shaile32266/hadoop-3.4.0/FullIndex/InvertedIndex.jar InvertedIndex /tmp/inputfile /tmp/outputfile
   ```

### Results
The Partial Inverted Index results show the occurrence of each word across the documents.

### Step 4: Full Inverted Index with Python
1. **Create the inverted_index.py file** with the necessary code to process the documents.
2. **Run the Python script** to generate the Full Inverted Index.

### Full Index Results
- **a**: [(2, 2)]
- **banana**: [(2, 3)]
- **is**: [(0, 1), (0, 4), (1, 1), (2, 1)]
- **it**: [(0, 0), (0, 3), (1, 2), (2, 0)]
- **what**: [(0, 2), (1, 0)]

## Enhancement
Possible improvements include optimizing the MapReduce process for better performance, considering scalability for larger datasets, and adding support for more file formats and enhanced error handling.

## Conclusion
This project successfully demonstrates the implementation of a MapReduce program to create a Full Inverted Index. The process involved setting up the environment, preparing the input data, running the MapReduce job, and interpreting the results. Future work could focus on further optimizations and scalability solutions.

## References
- Hadoop documentation
- Relevant articles and tutorials on MapReduce and Inverted Indexes
- [Your specific references, if any]
