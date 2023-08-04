import json
import csv

# trails
# id, name, type, difficulty, nodes

# lifts
# id, name, type, capacity, occupancy, oneway, nodes
 
# routes
# id, sequence, node

# positions
# id, lat, lon

INPUT_FILE_NAME = 'data/flaine_test_data2.json'
OUTPUT_FILE_NAME = 'data/test_{}_data.csv'

i = open(INPUT_FILE_NAME,'r')
input_data = json.load(i)
i.close()

# print(input_data)
route_file = open(OUTPUT_FILE_NAME.format('route'), 'w', newline='')
route_fieldnames = ['id', 'sequence', 'node']
route_writer = csv.DictWriter(route_file, fieldnames=route_fieldnames)
route_writer.writeheader()

piste_file = open(OUTPUT_FILE_NAME.format('trail'), 'w', newline='')
piste_fieldnames = ['id', 'name', 'type', 'difficulty', 'nodes']
piste_writer = csv.DictWriter(piste_file, fieldnames=piste_fieldnames)
piste_writer.writeheader()

lift_file = open(OUTPUT_FILE_NAME.format('lift'), 'w', newline='')
lift_fieldnames = ['id', 'name', 'type', 'capacity', 'oneway', 'nodes']
lift_writer = csv.DictWriter(lift_file, fieldnames=lift_fieldnames)
lift_writer.writeheader()

node_file = open(OUTPUT_FILE_NAME.format('position'), 'w', newline='')
node_fieldnames = ['node', 'lat', 'lon']
node_writer = csv.DictWriter(node_file, fieldnames=node_fieldnames)
node_writer.writeheader()

for element in input_data['elements']:
    # get the routes
    if element['type'] == 'way':
        if "tags" in element.keys():
            if "piste:type" in element['tags'].keys() or "aerialway" in element['tags'].keys():
                # route
                seq = 0
                for route_node in element.get('nodes', []):
                    route_data = {
                        'id': element['id'], 
                        'sequence': seq, 
                        'node': route_node
                    }
                    seq += 1
                    route_writer.writerow(route_data)
            
            # piste
            if "piste:type" in element['tags'].keys():            
                piste_data = {
                    'id': element['id'], 
                    'name': element["tags"].get('name', ''), 
                    'type': element["tags"].get('piste:type', ''), 
                    'difficulty': element["tags"].get('piste:difficulty', ''), 
                    'nodes': "|".join(str(node) for node in element.get('nodes', []))
                }
                piste_writer.writerow(piste_data)

            # lift
            elif "aerialway" in element['tags'].keys():
                lift_data = {
                    'id': element['id'], 
                    'name': element["tags"].get('name', ''), 
                    'type': element["tags"].get('aerialway', ''), 
                    'capacity': element["tags"].get('aerialway:capacity', ''), 
                    'oneway': element["tags"].get('oneway', ''), 
                    'nodes': "|".join(str(node) for node in element.get('nodes', []))
                }                    
                lift_writer.writerow(lift_data)

    # get the nodes
    if element['type'] == 'node':
        node_data = {
            'node': element['id'],
            'lat': element['lat'],
            'lon': element['lon']
        }
        node_writer.writerow(node_data)


route_file.close()
piste_file.close()
lift_file.close()
node_file.close()
