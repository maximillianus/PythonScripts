# MapReduce

MapReduce is a programming model that implements 2 functions which are map and
reduce. Map is a processing task that takes in an input and produce a key-value
pair outputs. Reduce is a processing task that takes in these list of key-value
pairs and reducing their individual number by aggregating them into a list of values
(key-sum pairs for example). MapReduce is the underlying clockword of Hadoop 
**processing** system. Hadoop storage system is handled using HDFS. Once input data is
divided into chunks (normally 128MB), it is stored in HDFS and ready for processing 
using MapReduce. MapReduce cycles the _mapping_ task across the clusters to 
map data into key-value pair and _reducer_ task shuffle and aggregated into a 
complete dataset as an output.

**mapreduce1.py**
this script explores capability of in-built map, filter, and reduce function in Python

**mapreduce2.py**
this script implements mapReduce using sentence-tokenizing as an example without any library
