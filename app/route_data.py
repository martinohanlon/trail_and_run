from guizero import App, Box, TitleBox, Text, TextBox, PushButton, ListBox
from neo4j import GraphDatabase

class TrailsAndRuns:
    def __init__(self, uri, user, password):
        self.db = GraphDatabase.driver(uri, auth=(user, password))

    def search(self, name):

        def query(tx, name):
            result = tx.run("MATCH (r:Route {name: $name}) RETURN r", name=name)
            return [ record["r"] for record in result ]

        with self.db.session() as session:
            record = session.execute_read(query, name=name)
            return record

    def close(self):
        self.db.close()

def search_route():
    records = tr.search(search_input.value)
    if len(records) > 0:
        result_box.enabled = True
        result_box.visible = True

        result_properties.clear()
        # add the properties to the listbox
        for prop in records[0].keys():
            result_properties.insert(0, "{}: {}".format(prop, records[0][prop]))
        status_text.value = "{} results found".format(len(records))

        result_box.enabled = False
    else:
        result_box.visible = False
        status_text.value = "No results found"

def close():
    status_text.value = "Closing database connection..."
    tr.close()
    app.destroy()

app = App(title="Trails and runs")

# Setup the GUI

# search
search_box = TitleBox(app, text="Search for a trail or run", width="fill")
search_input = TextBox(search_box, text="Malice", width="fill", align="left")
Box(search_box, width=20, align="left")
search_button = PushButton(search_box, text="Search", align="left", command=search_route)

# result
result_box = TitleBox(app, text="Result", width="fill", enabled=False, visible=False)
result_label = Text(result_box, text="Label", width="fill")
result_properties = ListBox(result_box, width="fill", align="bottom")

# status
status_box = Box(app, width="fill", align="bottom")
status_text = Text(status_box, align="left")

# Connect to the database
tr = TrailsAndRuns("bolt://localhost:7687", "neo4j", "neo4jletme1n")
app.when_closed = close

app.display()