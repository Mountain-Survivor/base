import json
with open("model.json", "r") as file:
    data = json.load(file)

print(data)
print(type(data))
print(data["model"])
print(data["ready"])