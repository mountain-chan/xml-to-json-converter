import json
import threading
import time

with open("my_data.json") as my_data:
    recipe = json.load(my_data)


def search_by_id(nodes, _id):
    node = next((item for item in nodes if item["id"] == _id), None)
    if node:
        return node
    for r in nodes:
        if r["type"] == "RAndOut":
            return search_by_id(r["nodes"], _id)


def ran_node(nodes, r_in_id):
    n = len(nodes)
    for i, node in enumerate(nodes):
        if node["type"] == "RBox":
            if nodes[i - 1]["type"] == "RAndIn":
                while not nodes[i - 1]["is_done"]:
                    pass

            print("---------")
            print(node["name"])
            print(f"runtime: {node['runtime']}")
            time.sleep(node["runtime"])
            node["is_done"] = True

        if node["type"] == "RAndOut":
            if nodes[i - 1]["type"] == "RAndIn":
                while not nodes[i - 1]["is_done"]:
                    pass
            tn = threading.Thread(target=ran_node, args=(node["nodes"], node["id"]))
            tn.start()

        if i == n - 1:
            r_out_id = str(int(r_in_id) + 1)
            r_and_in = search_by_id(recipe, r_out_id)
            if r_and_in:
                r_and_in["is_done"] = True


t1 = threading.Thread(target=ran_node, args=(recipe, "0"))

t1.start()
t1.join()
