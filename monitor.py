import json
import model_utils as model_utils

try:
    with open("models.json", "r") as file:
        models = json.load(file)

    for model in models:
        status = model_utils.check_model(model)
        print (model["name"], status)

except FileNotFoundError:
    print("models.json not found")

except json.JSONDecodeError:
    print("Invalid JSON")

"""
for model in models:
    if model["ready"]:
        print(model["name"], "READY")
    else:
        print(model["name"], "NOT READY")
"""

print("Feature monitor enabled")
