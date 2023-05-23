import os
import json
import requests
from collections.abc import Callable

class ServerTimeoutException(Exception): pass

CANNOT_LOAD_FILE: object
message_target: Callable[[str], None] | None = None

def load_json(file_path) -> None | dict:
        if not os.path.isfile(file_path):
            return None
        elif os.stat(file_path).st_size < 10:
            return None
        
        with open(file_path, 'r') as stream:
            data = json.load(stream)

        if len(data) < 3:
            return None
        
        return data

def messenger(_message: str, _print: bool = True, send_to_message_target: bool = False) -> None:
    if _print:
        print(_message)

    if message_target is not None and send_to_message_target:
        message_target(str(_message))

def troubleshoot_response_error_if_supposed_to(response: requests.Response) -> None:
    if response.status_code != 200:
        if response.headers.get('Content-Type').startswith('application/json'):
            messenger(response.json())
        messenger(response.request)
        messenger(response.request.body)
        messenger(response.request.url)
        messenger(response.request.headers)
        if response.status_code == 504:
            raise ServerTimeoutException
        response.raise_for_status()

def save_json(data: dict, path: str):
    with open(path, 'w') as stream:
        json.dump(data, stream, indent=4)

def pretty_print_big_number(n: float) -> str:
    if abs(n) > 10**9:
        s = f"{n/10**9:.3f}B"
    elif abs(n) > 10*6:
        s = f"{n/10**6:.3f}M"
    elif abs(n) > 10**3:
        s = f"{n/10**3:.3f}K"
    else:
        s = str(n)

    return s