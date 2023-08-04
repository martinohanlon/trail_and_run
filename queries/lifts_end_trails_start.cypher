MATCH (l:Lift)-[:END]->(p:Position)<-[:START]-(t:Trail)
RETURN l,t,p