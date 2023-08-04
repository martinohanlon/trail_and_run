match (l1:Lift{name: "Lapiaz"})-[liftend:END]->(startPos:Position)
match (endPos:Position)<-[liftstart:START]-(l2:Lift{name: "Gers"})
match path = shortestPath(
    (startPos)-[:NEXT*]->(endPos)
)
UNWIND nodes(path) as position
match (r:Route)<-[route:ON_ROUTE]-(position)
return l1, liftend, path, liftstart, l2, route, r;

// distance weighted using dijkstra
match (l1:Lift{name: "Lapiaz"})-[liftend:START]->(startPos:Position)
match (endPos:Position)<-[liftstart:START]-(l2:Lift{name: "Cascades"})

CALL
 apoc.algo.dijkstra(
 startPos,
 endPos,
 "NEXT>",
 "distance"
 )
YIELD path, weight

UNWIND nodes(path) as position
match (r:Route)<-[route:ON_ROUTE]-(position)
return l1, liftend, path, liftstart, l2, route, r, weight;