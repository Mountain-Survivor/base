def check_model(model):
    if model["ready"]:
        return "READY"
    else:
        return "NOT READY"