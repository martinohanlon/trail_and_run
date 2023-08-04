from guizero import App, Box, TitleBox, Text, Combo
from neo4j import GraphDatabase

class TrailsAndRuns:
    def __init__(self, uri, user, password):
        self.db = GraphDatabase.driver(uri, auth=(user, password))

    def get_trails(self):
        def query(tx):
            result = tx.run("""
                            MATCH (t:Trail) 
                            WHERE t.name IS NOT NULL 
                            RETURN t 
                            ORDER BY t.name
                            """)
            return [ record["t"] for record in result ]

        with self.db.session() as session:
            record = session.execute_read(query)
            return record
        
    def get_lifts(self):
        def query(tx):
            result = tx.run("""
                            MATCH (l:Lift) 
                            WHERE l.name 
                            IS NOT NULL RETURN l 
                            ORDER BY l.name
                            """)
            return [ record["l"] for record in result ]

        with self.db.session() as session:
            record = session.execute_read(query)
            return record
        
    def get_route_options(self, route_name, trail_or_lift, start_or_end):
        def query(tx):
            result = tx.run(f"""
                            MATCH (r:{trail_or_lift} {{name: "{route_name}"}})-[:{start_or_end}]->(pos:Position)
                            MATCH (routes)<-[onr:ON_ROUTE]-(pos)
                            OPTIONAL MATCH (routes)-[start:START]->(pos)
                            OPTIONAL MATCH (routes)-[end:END]->(pos)
                            RETURN routes, onr, start, end
                            """)
            
            available_routes = []

            for record in result:
                # ignore anything which is an :END
                if record["end"] is None:
                    data = {
                        "trail_or_lift": "Trail" if "Trail" in record["routes"].labels else "Lift",
                        "id": record["routes"]["id"],
                        "name": record["routes"].get("name", None),
                        "difficulty": record["routes"].get("difficulty", None),
                        "type": record["routes"].get("type", None),
                    }
                    
                    available_routes.append(data)

            return available_routes

        with self.db.session() as session:
            record = session.execute_read(query)
            return record

    def search(self, name):

        def query(tx, name):
            result = tx.run("MATCH (r:Route {name: $name}) RETURN r", name=name)
            return [ record["r"] for record in result ]

        with self.db.session() as session:
            record = session.execute_read(query, name=name)
            return record

    def close(self):
        self.db.close()

def update_routes():
    selected_route = select_route.value
    
    if trail_or_lift.value == "Trail":
        routes = tr.get_trails()
    else:
        routes = tr.get_lifts()
    select_route.clear()

    for route in routes:
        select_route.append(route["name"])

    select_route.value = selected_route

    update_route_options()

def update_route_options():
    options = tr.get_route_options(select_route.value, trail_or_lift.value, route_position.value)
    options_text.value = ""
    for option in options:
        if option["trail_or_lift"] == "Trail":
            options_text.value += f"Take trail '{option['name']}' - a {option['difficulty']} {option['type']}\n"
        else:
            options_text.value += f"Take lift '{option['name']}'  - a '{option['type']}'\n"

def close():
    tr.close()
    app.destroy()

app = App(title="Route options", height=200, width=500)

# Setup the GUI
where_box = TitleBox(app, text="Where are you?", width="fill", align="top")
Text(where_box, text="I am at the", align="left")
route_position = Combo(where_box, options=["START", "END"], selected="START", command=update_route_options, align="left")
Text(where_box, text="of the", align="left")
select_route = Combo(where_box, command=update_route_options, align="left")
trail_or_lift = Combo(where_box, options=["Trail", "Lift"], selected="Trail", command=update_routes, align="left")

Box(app, width="fill", height=20)

options_box = TitleBox(app, text="You can ...", width="fill", align="top")
options_text = Text(options_box, width="fill", align="top")

# Connect to the database
tr = TrailsAndRuns("bolt://localhost:7687", "neo4j", "neo4jletme1n")
app.when_closed = close


update_routes()

app.display()