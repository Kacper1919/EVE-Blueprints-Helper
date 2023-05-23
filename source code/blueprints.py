import json
from datetime import datetime, timedelta
import requests
from token_manager import TokenManager
from prices import Prices, AVERAGE, ADJUSTED, LOWEST
from shared import get_type_names
import math
from utils import load_json, messenger, troubleshoot_response_error_if_supposed_to, save_json

class NoSavedJsonException(Exception): pass
class FailedtoFindMarketPricesException(Exception): pass
class FailedToGetMaterialPriceException(Exception): pass
class FailedToGetProductPriceException(Exception): pass
class FailedToGetAdjustedPriceException(Exception): pass

class BlueprintComputer:
    def __init__(self, token_manager: TokenManager,
        prices: Prices,
        system_of_interest_id: int = 30000142,
        manufacturing_tax: float = 0.1,
        sales_tax: float = 0.07,
        blueprints_file_path: str = 'computed_blueprints.json',
        material_efficiency_from_structure: float = 0,
        use_average_material_prices: bool = True,
        use_average_product_prices: bool = True,
        statistical_significance: float = 0.06,
        settings: dict | None = None) -> None:
        """settings overrides some of other arguments."""
            
        self.prices: Prices = prices
        self.token_manager: TokenManager = token_manager
        self.system_of_interest_id: int = system_of_interest_id
        self.manufacturing_tax: float = manufacturing_tax
        self.sales_tax: float = sales_tax
        self.blueprints_file_path: str = blueprints_file_path
        self.material_efficiency_from_structure: float = material_efficiency_from_structure
        self.use_average_material_prices: bool = use_average_material_prices
        self.use_average_product_prices: bool = use_average_product_prices
        self.statistical_significance: float = statistical_significance

        self.system_manufacturing_cost_index: float
        self.bp_static_data: dict
        self.computed_blueprints: dict
        self.token: dict = {}

        self.populate_bp_static_data()
        self.populate_systems_crafting_cost_index()

        if settings is not None:
            self.apply_settings(settings)

        self.blueprints = load_json(self.blueprints_file_path)
        self.match_settings()
        
    def get_settings_from_members(self) -> dict:
        settings = {
            "system_of_interest_id": self.system_of_interest_id,
            "manufacturing_tax": self.manufacturing_tax,
            "sales_tax": self.sales_tax,
            "material_efficiency_from_structure": self.material_efficiency_from_structure,
            "statistical_significance": self.statistical_significance,
            "use_average_material_prices": self.use_average_material_prices,
            "use_average_product_prices": self.use_average_product_prices
        }
        return settings

    def apply_settings(self, settings: dict) -> None:
        self.system_of_interest_id = settings['system_of_interest_id']
        self.manufacturing_tax = settings['manufacturing_tax']
        self.sales_tax = settings['sales_tax']
        self.material_efficiency_from_structure = settings['material_efficiency_from_structure']
        self.statistical_significance = settings['statistical_significance']
        self.use_average_material_prices = settings['use_average_material_prices']
        self.use_average_product_prices = settings['use_average_product_prices']

        self.match_settings
        
    def match_settings(self) -> None:
        if self.blueprints is not None and 'settings' in self.blueprints.keys():
            bp_settings: dict = self.blueprints['settings']
            settings_to_match_to = self.get_settings_from_members()

            for key, setting in bp_settings.items():
                if settings_to_match_to[key] != setting:
                    self.blueprints: dict = {'settings': self.get_settings_from_members()}
                    messenger('Blueprint Computer settings did not match')
                    break
        else:
            self.blueprints: dict = {'settings': self.get_settings_from_members()}

    def get_token(self):
        if self.token == {} or float(self.token['exp']) < datetime.timestamp(datetime.now() - timedelta(seconds=15)):
            self.token = self.token_manager.get_token()
        return self.token

    def populate_bp_static_data(self) -> None:
        with open('blueprints_static_data.json', 'r') as stream:
            self.bp_static_data = json.load(stream)

    def populate_systems_crafting_cost_index(self) -> None:
        headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        }
        response = requests.get("https://esi.evetech.net/latest/industry/systems/?datasource=tranquility", headers=headers)
        troubleshoot_response_error_if_supposed_to(response)

        systems: list = response.json()

        for system in systems:
            if system['solar_system_id'] == self.system_of_interest_id:
                for activity in system['cost_indices']:
                    if activity['activity'] == 'manufacturing':
                        self.system_manufacturing_cost_index = float(activity['cost_index'])
                        break
                break

    def get_user_blueprints(self) -> list:
        token: dict = self.get_token()

        character_id = token['sub'].split(':')[2]
        headers = {
            "accept": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": f"Bearer {token['access_token']}"
        }
        response = requests.get(f"https://esi.evetech.net/latest/characters/{character_id}/blueprints", headers=headers)
        troubleshoot_response_error_if_supposed_to(response)

        return response.json()

    def get_blueprint_by_id(self, id: str) -> dict:
        return self.blueprints[id]

    def get_materials(self, blueprint_item_or_type_id: str, item_id: bool = True, own_materials: list[str] = None, invent: bool = False, get_names: bool = False) -> dict:

        if item_id:
            blueprint = self.blueprints[blueprint_item_or_type_id]
            blueprint_type_id = str(blueprint['type_id'])
            blueprint_material_efficiency = float(blueprint['material_efficiency']) / 100
            total_efficiency = blueprint_material_efficiency + self.material_efficiency_from_structure
        else:
            blueprint_type_id = blueprint_item_or_type_id
            blueprint_material_efficiency = 0
            total_efficiency = self.material_efficiency_from_structure

        if invent:
            mat_list = self.bp_static_data[blueprint_type_id]['activities']['invention']['materials']
        else:
            mat_list = self.bp_static_data[blueprint_type_id]['activities']['manufacturing']['materials']

        if get_names:
            names: dict = get_type_names(mat_list)

        full_mats: dict = {}

        for mat in mat_list:
            mat_id = str(mat['typeID'])
            quantity = mat["quantity"]
            average_price = self.prices.get_price(mat_id, AVERAGE)
            adjusted_price = self.prices.get_price(mat_id, ADJUSTED)

            if self.use_average_material_prices:
                price = self.prices.get_price(mat_id, AVERAGE)
            else:
                price = self.prices.get_price(mat_id, LOWEST)

            total_adjusted_price = adjusted_price * quantity

            if own_materials is not None and mat_id in own_materials:
                user_price = price * (1 - self.sales_tax)
            else:
                user_price = price


            if invent:
                user_quantity = quantity
            else:
                user_quantity = math.ceil(quantity * (1 - total_efficiency))

            total_price = user_quantity * user_price

            mat = {
                "type_id": mat_id,
                "quantity": quantity,
                "price": price,
                "average_price": average_price,
                "adjusted_price": adjusted_price,
                "user_price": user_price,
                "user_quantity": user_quantity,
                "total_price": total_price,
                "total_adjusted_price": total_adjusted_price
            }

            if get_names:
                mat['name'] = names[mat_id]

            full_mats[mat_id] = mat

        return full_mats

    def get_blueprint_invention_data(self,
        blueprint_item_id: str,
        own_materials: list | None = None,
        new_success_chance: float | None = None,
        optional_item_price: float | None = None,
        materials: dict | None = None) -> dict | None:

        blueprint_type_id = str(self.blueprints[blueprint_item_id]['type_id'])

        if 'invention' not in self.bp_static_data[str(blueprint_type_id)]['activities']:
            messenger(f"{self.blueprints[blueprint_item_id]['name']} Cannot be invented")
            return None

        if materials is None:
            materials = self.get_materials(blueprint_item_id, item_id=True, own_materials=own_materials, invent=True, get_names=True)

        mat_cost = 0.0

        if optional_item_price is not None:
            mat_cost += optional_item_price

        for mat in materials.values():
            mat_cost += mat['total_price']

        products = self.bp_static_data[blueprint_type_id]['activities']['invention']['products']

        if len(products) != 1:
            pass

        product = products[0]
        
        if new_success_chance is None:
            probability = product['probability']
        else:
            probability = new_success_chance

        probability_sum = 0
        i = 1
        while True:
            probability_sum += (1 - probability_sum) * probability
            if probability_sum >= 1 - self.statistical_significance:
                break
            i += 1

        average_invent_material_cost = 1 / probability * mat_cost
        invent_material_cost_error = i * average_invent_material_cost - average_invent_material_cost

        product_bp_type_id = str(product['typeID'])
        product_bp = {
            'type_id': int(product_bp_type_id)
        }

        product_bp_materials = self.get_materials(product_bp_type_id, False, own_materials, get_names=True)
        
        product_data = self.get_blueprint_profit(product_bp, materials=product_bp_materials)
        product_profit = product_data['profit']

        average_profit = product_profit - average_invent_material_cost
        profit_error = invent_material_cost_error

        bp_invent_data = {
            'invent_materials': materials,
            'invent_material_cost': mat_cost,
            'average_invent_material_cost': average_invent_material_cost,
            'invent_material_cost_error': invent_material_cost_error,
            'product_data': product_data,
            'average_profit': average_profit,
            'profit_error': profit_error
        }

        self.save()
        return bp_invent_data

    def get_blueprint_profit(self, blueprint: dict, own_materials: list = None, materials: dict = None) -> dict:
        """
        arg blueprint is required to consist at least of { 'type_id': id, material_efficiency: efficiency }
        """

        if materials is None:
            bp_item_id = str(blueprint['item_id'])
            self.blueprints[bp_item_id] = blueprint
            materials = self.get_materials(bp_item_id, item_id=True, own_materials=own_materials, invent=False, get_names=False)

        mats_cost = 0.0
        estimated_mats_value = 0.0

        for mat in materials.values():
            mats_cost += mat['total_price']
            estimated_mats_value += mat['total_adjusted_price']

        job_cost = estimated_mats_value * self.system_manufacturing_cost_index * (1 + self.manufacturing_tax)


        bp_type_id = str(blueprint['type_id'])
        product_id = str(self.bp_static_data[bp_type_id]['activities']['manufacturing']['products'][0]['typeID'])
        prouduct_quantity = int(self.bp_static_data[bp_type_id]['activities']['manufacturing']['products'][0]['quantity'])

        if self.use_average_product_prices:
            product_price = self.prices.get_price(product_id, AVERAGE)
        else:
            product_price = self.prices.get_price(product_id, LOWEST)

        profit = product_price * prouduct_quantity * (1 - self.sales_tax) - job_cost - mats_cost

        blueprint_computed_values = {
            "material_cost": mats_cost,
            "estimated_mats_value": estimated_mats_value,
            "product_price": product_price,
            "profit": profit,
            "job_cost": job_cost,
            "quantity": prouduct_quantity,
            "acquired_at": datetime.now().timestamp(),
            "materials": materials
        }
        
        return blueprint_computed_values

    def get_computed_blueprints(self) -> dict:
        """Example Output: [{
            "item_id": 1036374337174,
            "location_flag": "Hangar",
            "location_id": 1036374147165,
            "material_efficiency": 0,
            "quantity": -2,
            "runs": 5,
            "time_efficiency": 0,
            "type_id": 48108,
            "materials_cost": 7046625.78,
            "estimated_mats_value": 5761.679473448037,
            "product_price": 899.9,
            "profit": -3024918.882630676,
            "job_cost": 846.1026306758445,
            "acquired_at": 1681941700.805133,
            "name": "Baryon Exotic Plasma L Blueprint"
        }, {...}, etc.]"""

        esi_blueprints = self.get_user_blueprints()
        self.match_settings()
        names: dict = get_type_names(esi_blueprints)

        for bp_id, esi_blueprint in enumerate(esi_blueprints):
            name = names[str(esi_blueprint['type_id'])]

            messenger(f"({bp_id + 1}/{len(esi_blueprints)}): {name}", send_to_message_target=True)
            
            self.blueprints[str(esi_blueprint['item_id'])] = esi_blueprint | self.get_blueprint_profit(esi_blueprint) | {"name": name}

        self.prices.populate_price_names()

        self.save()
        self.prices.save()

        return self.blueprints
    
    def save(self) -> None:
        save_json(self.blueprints, self.blueprints_file_path)
