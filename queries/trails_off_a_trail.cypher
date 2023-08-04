// find all the trails which are connected to a specific trail  

MATCH (t:Trail {name: "Lutin"})<-[:ON_ROUTE]-(p:Position)-[:ON_ROUTE]->(trails:Trail) 
RETURN t, trails, p