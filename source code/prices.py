import requests
from utils import troubleshoot_response_error_if_supposed_to, messenger, save_json, load_json
from datetime import datetime
from shared import get_type_names

AVERAGE = object()
ADJUSTED = object()
LOWEST = object()

class Prices:
    def __init__(self,
        region_of_interest_id: int = 10000002,
        structure_of_interest_location_id: int = 60003760,
        price_deprecation_time_in_seconds: int = 86400,
        prices_file_path: str = 'prices.json',
        settings: dict | None = None) -> None:
        """settings override some of the other arguments."""
        
        self.region_of_interest_id: int = region_of_interest_id
        self.structure_of_interest_location_id: int = structure_of_interest_location_id
        self.price_deprecation_time_in_seconds: int = price_deprecation_time_in_seconds
        self.prices_file_path: str = prices_file_path

        self.chosen_prices: dict = {}
        self.general_prices: dict = {}

        self.populate_general_prices()

        if settings is not None:
            self.apply_settings(settings)

        self.chosen_prices = load_json(prices_file_path)
        self.match_settings()

    def get_settings_from_members(self) -> dict:
        settings = {
            "region_of_interest_id": self.region_of_interest_id,
            "structure_of_interest_location_id": self.structure_of_interest_location_id,
            "price_deprecation_time_in_seconds": self.price_deprecation_time_in_seconds,
        }
        return settings

    def match_settings(self) -> None:
        if self.chosen_prices is not None and'settings' in self.chosen_prices.keys():
            p_settings: dict = self.chosen_prices['settings']
            settings_to_match_to = self.get_settings_from_members()

            for key, setting in p_settings.items():
                if settings_to_match_to[key] != setting:
                    self.chosen_prices: dict = {"settings": self.get_settings_from_members()}
                    messenger('Prices settings did not match')
                    break
        else:
            self.chosen_prices: dict = {"settings": self.get_settings_from_members()}

    def apply_settings(self, settings: dict) -> None:
        self.region_of_interest_id = settings['region_of_interest_id']
        self.structure_of_interest_location_id = settings['structure_of_interest_location_id']
        self.price_deprecation_time_in_seconds = settings['price_deprecation_time_in_seconds']

        self.match_settings()

    def populate_general_prices(self) -> None:
        headers = {
            "accept": "application/json",
            "Cache-Control": "no-cache",
        }
        response = requests.get("https://esi.evetech.net/latest/markets/prices/?datasource=tranquility", headers=headers)
        troubleshoot_response_error_if_supposed_to(response)

        types: list[dict] = response.json()

        for type in types:
            adjusted_price = type['adjusted_price']

            if 'average_price' in type.keys():
                average_price = type['average_price']
            else:
                average_price = adjusted_price

            self.general_prices[str(type['type_id'])] = { "adjusted": adjusted_price, "average": average_price}

    def get_type_cheapest_order(self, type_id: int) -> dict:
        headers = {
            "accept": "application/json",
            "Cache-Control": "no-cache",
        }
        response = requests.get(f"https://esi.evetech.net/latest/markets/{self.region_of_interest_id}/orders/?datasource=tranquility&order_type=sell&page=1&type_id={type_id}", headers=headers)
        troubleshoot_response_error_if_supposed_to(response)

        orders = response.json()
        pages = response.headers['x-pages']

        if int(pages) > 1:
            for i in range(2, int(pages)+1):
                response = requests.get(f"https://esi.evetech.net/latest/markets/{self.region_of_interest_id}/orders/?datasource=tranquility&order_type=sell&page={i}&type_id={type_id}", headers=headers)
                troubleshoot_response_error_if_supposed_to(response)
                orders = orders | response.json()

        cheapest_corret_order = {"price": 66666666666666666666 }

        for order in orders:
            if int(order["price"] < cheapest_corret_order["price"]):
                if order['location_id'] == self.structure_of_interest_location_id:
                    cheapest_corret_order = order

        if cheapest_corret_order == {"price": 66666666666666666666 }:
            messenger(f"Couldn't find order for: {type_id}", send_to_message_target=True)

        messenger(f'got_chepest_order for {type_id}')

        return cheapest_corret_order
    
    def get_lowest_price(self, type_id: str) -> float:
        """If not already saved or deprecated than enumerates through sell orders to determine lowest price. Saves it to self.prices"""
        
        if 'lowest' not in self.chosen_prices[type_id].keys() or self.chosen_prices[type_id]['acquired_at'] + self.price_deprecation_time_in_seconds < datetime.now().timestamp():
            lowest_price = float(self.get_type_cheapest_order(type_id)['price'])

            self.chosen_prices[type_id]['lowest'] = lowest_price
            self.chosen_prices[type_id]['acquired_at'] = datetime.timestamp(datetime.now())

            return lowest_price
        else:
            return self.chosen_prices[type_id]['lowest']
        
    def populate_price_names(self):
        """Adds price name to every price in self.prices"""
        item_ids = []

        for price_item_id, type in self.chosen_prices.items():
            if type is dict and 'name' not in type.keys():
                item_ids.append({'type_id': price_item_id})

        if len(item_ids) == 0:
            return

        names: dict = get_type_names(item_ids)

        for key, name in names.items():
            self.chosen_prices[key]['name'] = name

    def get_price(self, type_id: str, type_of_price: object, ) -> float:
        if type_id in self.chosen_prices:
            price_set: dict = self.chosen_prices[type_id]

            if type_of_price == AVERAGE:
                return price_set['average']
            elif type_of_price == ADJUSTED:
                return price_set['adjusted']
            elif type_of_price == LOWEST:
                return self.get_lowest_price(type_id)
        else:
            general_price: dict = self.general_prices[type_id]

            adjusted = general_price['adjusted']
            average = general_price['average']

            self.chosen_prices[type_id] = {
                'average': average,
                'adjusted': adjusted
            }

            if type_of_price == AVERAGE:
                return average
            elif type_of_price == ADJUSTED:
                return adjusted
            elif type_of_price == LOWEST:
                return self.get_lowest_price(type_id)
            
    def save(self):
        save_json(self.chosen_prices, self.prices_file_path)
