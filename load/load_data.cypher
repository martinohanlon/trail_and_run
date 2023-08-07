DROP CONSTRAINT position_id IF EXISTS;
DROP CONSTRAINT route_id IF EXISTS;

MATCH (r:Route) DETACH DELETE r;
MATCH (p:Position) DETACH DELETE p;
MATCH (t:Trail) DETACH DELETE t;
MATCH (l:Lift) DETACH DELETE l;

CREATE CONSTRAINT route_id
FOR (r:Route) REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT position_id
FOR (p:Position) REQUIRE p.id IS UNIQUE;

// routes and nodes
LOAD CSV WITH HEADERS
//    FROM 'https://drive.google.com/uc?export=download&id=1HXHph5-Rv35TP3YrNYyVjYXfx6k5Gubf'
FROM 'file:///test_route_data.csv'
AS row

MERGE (r:Route {id: toInteger(row.id)})
MERGE (p:Position {id: toInteger(row.node)})
MERGE (p)-[pr:ON_ROUTE]->(r)
SET pr.sequence = toInteger(row.sequence);

// add node coordinates
LOAD CSV WITH HEADERS
// FROM 'https://drive.google.com/uc?export=download&id=1Xw7WfDYFGYMPAvqw9x92KVDLyyIK17zM'
FROM 'file:///test_position_data.csv'
AS row
MATCH (p:Position {id: toInteger(row.node)})
SET p.location = point({latitude: toFloat(row.lat), longitude: toFloat(row.lon)});

// trails
LOAD CSV WITH HEADERS
// FROM 'https://drive.google.com/uc?export=download&id=1t5Ha5JSIH-v9H5lHpoUpKodTOdC7MISf'
FROM 'file:///test_trail_data.csv'
AS row
MATCH (r:Route {id: toInteger(row.id)})
SET r:Trail,
r.name = row.name,
r.type = row.type,
r.difficulty = row.difficulty;

// lifts
LOAD CSV WITH HEADERS
// FROM 'https://drive.google.com/uc?export=download&id=169Zy3w9k3GFwfq8MJsvRf5YPqfAA33Y0'
FROM 'file:///test_lift_data.csv'
AS row
MATCH (r:Route {id: toInteger(row.id)})
SET r:Lift,
r.name = row.name,
r.type = row.type,
r.capacity = toInteger(row.capacity),
r.occupancy = toInteger(row.occupancy),
r.oneway = row.oneway;

// set start and end positions on routes
MATCH (r)<-[rp:ON_ROUTE]-(p)
WITH r, rp, p
ORDER BY rp.sequence
WITH r, collect(p) AS positions
WITH r, head(positions) AS firstposition, last(positions) AS lastposition
MERGE (r)-[start:START]->(firstposition)
MERGE (r)-[end:END]->(lastposition);

// set the next node on each node
MATCH (r:Route)<-[rp:ON_ROUTE]-(p:Position)
WITH r, rp, p
ORDER BY rp.sequence
WITH r, collect(p) AS positions
UNWIND range(0, size(positions)-2) as idx
WITH positions[idx] as this, positions[idx+1] as next
MERGE (this)-[nr:NEXT]->(next)
SET nr.distance = point.distance(this.location, next.location);

// set the difficulty score on next relationships
MATCH (this)-[n:NEXT]->(next)-[:ON_ROUTE]->(t:Trail)
WITH t, n,
CASE t.difficulty
    when 'novice' then 1
    when 'easy' then 2
    when 'intermediate' then 3
    when 'advanced' then 4
    else 0
END AS diff_score
SET n.diff_score = diff_score;
