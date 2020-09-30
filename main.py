import json
import xmltodict
import random

with open("simpleRez.xml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

node_data = data_dict["SaveRezept"]["mRezept"]["Node"]

with open("node_data.json", "w") as json_file:
    json.dump(node_data, json_file, indent=4)


def get_my_data(nodes_full_info):
    if type(nodes_full_info) is not list:
        nodes_full_info = [nodes_full_info]
    nodes = []
    for i in nodes_full_info:
        node = {
            "type": i["@xsi:type"],
            "name": i["@Name"],
            "id": i["@Id"],
            "runtime": random.randint(1, 4),
            "is_done": False
        }
        if i["@xsi:type"] == "RAndOut":
            node["nodes"] = get_my_data(i["OutSection"]["Node"])
        nodes.append(node)
    return nodes


my_data = get_my_data(node_data)

with open("simpleRez.json", "w") as json_file:
    json.dump(my_data, json_file, indent=4)
