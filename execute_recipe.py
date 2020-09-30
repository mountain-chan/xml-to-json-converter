import json
import threading
import time

with open("simpleRez.json") as my_data:
    recipe = json.load(my_data)


def search_by_id(nodes, _id):
    node = next((item for item in nodes if item["id"] == _id), None)
    if node:
        return node
    for r in nodes:
        if r["type"] == "RAndOut":
            return search_by_id(r["nodes"], _id)


end = False


def ran_node(nodes, r_in_id):
    n = len(nodes)
    for i, node in enumerate(nodes):
        j = i - 1

        if end:
            break

        if node["type"] != "RAndIn":
            while j >= 0 and nodes[j]["type"] == "RAndIn":
                while not nodes[j]["is_done"]:
                    if end:
                        break
                    pass
                j -= 1

        if node["type"] == "RBox":
            print("---------")
            print(node["name"])
            print(f"runtime: {node['runtime']}")

            # execute function if not done
            if not node["is_done"]:
                time.sleep(node["runtime"])
                node["is_done"] = True

                # update status recipe
                with open("simpleRun.json", "w") as json_file:
                    json.dump(recipe, json_file, indent=4)

        elif node["type"] == "RAndOut":
            tn = threading.Thread(target=ran_node, args=(node["nodes"], node["id"]))
            tn.start()

        if i == n - 1:
            r_out_id = str(int(r_in_id) + 1)
            r_and_in = search_by_id(recipe, r_out_id)
            if r_and_in:
                r_and_in["is_done"] = True

                # update status recipe
                with open("simpleRun.json", "w") as json_file:
                    json.dump(recipe, json_file, indent=4)


t1 = threading.Thread(target=ran_node, args=(recipe, "0"))

t1.start()
t1.join()
