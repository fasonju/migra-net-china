import json
import os

def get_json(json_path: os.PathLike):
    with open(json_path, 'r') as f:
        output = json.load(f)
    return output



