import json


def write_json(name: str, data):
    with open('./output/'+name+'.json', 'w') as file:
        json.dump(data, file)  # Write some JSON stuff
