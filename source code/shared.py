import requests
from utils import troubleshoot_response_error_if_supposed_to
import json

def get_type_names(types: list[dict]) -> dict:
    """Required types arg: [{ type_id/typeID: id }}"""
    proper_names: dict = {}
    ids = []

    for type in types:

        if 'type_id' in type:
            type_id = str(type['type_id'])
        elif 'typeID' in type.keys():
            type_id = str(type['typeID'])

        # if self.prices is not None and type_id in self.prices.chosen_prices.keys():
        #     if 'name' in self.prices.chosen_prices[type_id]:
        #         proper_names[type_id] = self.prices.chosen_prices[type_id]['name']
        #         continue

        if not int(type_id) in ids:
            ids.append(int(type_id))

    if len(ids) == 0:
        return None
    
    data = json.dumps(ids)

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
    }
    response = requests.post("https://esi.evetech.net/latest/universe/names", data=data, headers=headers)
    troubleshoot_response_error_if_supposed_to(response)

    names: list[dict] = response.json()

    for name in names:
        proper_names[str(name["id"])] = name['name']
    
    return proper_names