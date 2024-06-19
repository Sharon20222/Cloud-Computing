
# Project: Calculating Pi Using MapReduce and PySpark

## Overview
This project aims to calculate the value of Pi using two approaches: MapReduce and PySpark. The steps include setting up a VM instance on Google Cloud Platform (GCP), generating random dots, implementing MapReduce to calculate Pi, and enhancing the results using PySpark.

## Table of Contents
1. [Introduction](#introduction)
2. [Design](#design)
3. [Implementation](#implementation)
   - [MapReduce](#mapreduce)
   - [PySpark](#pyspark)
4. [Testing](#testing)
5. [Enhancements](#enhancements)
6. [Conclusion](#conclusion)
7. [References](#references)

## Introduction
The objective of this project is to calculate the value of Pi using MapReduce and PySpark. The project involves the following main steps:
1. Setting up the environment on GCP.
2. Implementing MapReduce to calculate Pi.
3. Enhancing the result using PySpark.

## Design
### Step 1: MapReduce Approach
1. Generate random dot pairs using a Java program.
2. Implement MapReduce to calculate Pi based on the generated dots.
3. Calculate Pi using the MapReduce result.

### Step 2: PySpark Enhancement
1. Implement Pi Calculation using PySpark on GCP.
2. Compare the results from MapReduce and PySpark.

## Implementation

### MapReduce
#### 1. Start VM instance on GCP
- Initialize the VM instance.

#### 2. Connect via SSH
- Access the instance using SSH.

#### 3. Add a directory for code
- Create a directory to store all the codes.

#### 4. Generate random dots
- Java Program: `GenerateDots.java`
- Command line arguments: radius, number of pairs.

#### 5. Implement MapReduce Code
- Java Program: `CalculatePiMR.java`

#### 6. Java Program for Pi Calculation
- Calculate Pi using MapReduce result.

#### 7. Format the filesystem
- Prepare the environment.

#### 8. Start NameNode and DataNode
- Command: `sbin/start-dfs.sh`
- Resolve permission issues by reconnecting SSH.

#### 9. Generate SSH Keys
```bash
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
$ chmod 0600 ~/.ssh/authorized_keys
$ ssh localhost
```

#### 10. Reformat and Start Daemons
- Finalize the setup by formatting and starting NameNode and DataNode.

#### 11. Test Connection
- Verify the connection with localhost.

#### 12. Compile and run `GenerateDots.java`
```bash
$ javac GenerateDots.java
$ java GenerateDots 5 1000 > ./Input/dots.txt
```

#### 13. Copy file to Hadoop and check
```bash
$ hadoop fs -put ./Input/dots.txt /Input/dots.txt
$ hadoop fs -ls /Input
```

#### 14. Compile Java and Create JAR
```bash
$ javac -classpath $(hadoop classpath) -d . CalculatePiMR.java
$ jar -cvf CalculatePiMR.jar -C . .
```

#### 15. Run Application
```bash
$ hadoop jar CalculatePiMR.jar org.myorg.CalculatePiMR /Input /Output
```

#### 16. Check Output File
```bash
$ hadoop fs -cat /Output/part-r-00000
```

#### 17. Show Output
- Display the calculated value of Pi.

#### 18. Calculate Pi using MapReduce Output
- Use the output to compile and run the Java program to get the Pi value.

### PySpark
#### 1. Open GCP and Select Cloud Storage
- Initial setup.

#### 2. Select Dataproc
- Access Dataproc service from the console.

#### 3. Create Cluster
- Configure and create the cluster with single node type.

#### 4. Activate Cloud Shell Editor
- Prepare the environment and add the Spark Pi Calculator program.

#### 5. Submit Job
```bash
$ gcloud dataproc jobs submit pyspark --cluster=<cluster-name> --region=<region> spark_pi.py
```

#### 6. View Output
- Check the results.

#### 7. Check Pi Calculated
- Verify the calculated Pi value in the output folder.
- **Result**: Pi value calculated by PySpark: `3.13732`

## Testing
- Verify setup and execution at each stage.
- Present the Pi value calculated using MapReduce.
- **Result**: Pi value calculated: `3.104`

## Enhancements
### Enhancing the Result with PySpark
1. Open GCP and Select Cloud Storage.
2. Select Dataproc from the console menu.
3. Create a cluster with a single node.
4. Activate the Cloud Shell editor and add the Spark Pi Calculator program.
5. Submit the PySpark job and view the output.
6. Verify the Pi value calculated by PySpark.
- **Result**: Pi value calculated by PySpark: `3.13732`

## Conclusion
- **Comparison of Methods**:
  - MapReduce Pi value: `3.104`
  - PySpark Pi value: `3.13732`
- **Learning Outcome**:
  - PySpark provides a closer approximation to the actual value of Pi compared to MapReduce.
  - PySpark is more efficient and easier to implement than traditional MapReduce.

## References
- GCP Documentation
- Hadoop and MapReduce Tutorials
- PySpark Documentation


