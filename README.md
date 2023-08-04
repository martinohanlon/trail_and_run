# Trail and Run

Trail and Run is a project I created to support my learning of Neo4j, Cypher and Python integration. 

It takes Ski resort data from OpenStreetMap, loads it into a Neo4j database and asks useful questions such as "What is the shortest route between lifts?"

You can read about my experience in the blog post - ####

## Structure

- /app/route_data.py - a Python program that pulls back data about a route
- /app/where_can_I_go - a Python program which gives options about routes you can take based on where you are
- /data - test data files, overpass turbo queries and the Python program to generate the CSV files used to load the Neo4j database
- /data_structure - the initial data structure which can be opened using https://arrows.app/
- /load/load_data.cypher - the Cypher query to generate and load the Neo4j database 
- /queries - useful Cypher queries for interrogating the data