def attempt(operation, config):
    for i in range(config["attempts"]):
        if operation():
            return True
    return False
