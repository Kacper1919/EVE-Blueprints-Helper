import os
import json

store_tokens = True

def read_secrets() -> dict:
    filename = os.path.join('app_config.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        raise RuntimeError("Cannot find requiredd app config file")
    
app_config = read_secrets()

client_id = app_config['client_id']
port = app_config['port']
host = app_config['host']
base_uri = f"http://{host}:{port}"