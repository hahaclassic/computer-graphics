import yaml
from yaml.loader import SafeLoader

def read_manual() -> str:
    with open('config.yml', 'r') as f:
        config_data = yaml.load(f, Loader=SafeLoader)

    file = open(config_data['manual_path'], "r")
    manual = file.read()
    file.close()
    return manual

def read_task() -> str:
    with open('config.yml', 'r') as f:
        config_data = yaml.load(f, Loader=SafeLoader)

    file = open(config_data['task_path'], "r")
    task = file.read()
    file.close()
    return task

