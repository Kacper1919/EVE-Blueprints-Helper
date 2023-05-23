from app_config import client_id, host, port

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QWidget
import sys
from ui import Ui_MainWindow
from settings import Ui_Form

import utils
from utils import load_json, pretty_print_big_number, save_json

import prices

from token_requests import TokenRequester
from token_manager import TokenManager
from blueprints import BlueprintComputer
from prices import Prices

import cProfile

#To Do: Handle 502 Server Error: Bad Gateway
#TO Do: Some UI handling of long actions

SCOPES = ['esi-characters.read_blueprints.v1',
          'esi-assets.read_assets.v1']

DEFAUL_SETTINGS: dict = {
    "system_of_interest_id": 30000142,
    "region_of_interest_id": 10000002,
    "structure_of_interest_location_id": 60003760,
    "manufacturing_tax": 0.1,
    "sales_tax": 0.1,
    "material_efficiency_from_structure": 0.0,
    "statistical_significance": 0.05,
    "use_average_material_prices": False,
    "use_average_product_prices": False
}

token_manager: TokenManager
blueprint_computer: BlueprintComputer
prices: Prices
token = dict
blueprints = dict
acquired_settings: dict

running = False
selected_blueprint_id: str = None

class CustomCheckbox(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.BottomToTop, parent=self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.wdg = QCheckBox()
        self.layout.addWidget(self.wdg)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.getTokenBtn.clicked.connect(self.get_token_on_push)
        self.ui.refresh_btn.clicked.connect(self.refresh_on_push)
        self.ui.settings_btn.clicked.connect(self.show_settings)

        self.ui.table.setColumnWidth(1, 300)
        self.ui.table.setColumnWidth(2, 70)
        self.ui.table.setColumnWidth(3, 70)
        self.ui.table.setColumnHidden(0, True)
        self.ui.table.cellClicked.connect(self.blueprint_selected_populate_tables)

        self.ui.table_2.setColumnWidth(1, 100)
        self.ui.table_2.setColumnWidth(2, 70)
        self.ui.table_2.setColumnWidth(3, 70)
        self.ui.table_2.setColumnWidth(4, 70)
        self.ui.table_2.setColumnHidden(0, True)

        self.ui.pushButton.clicked.connect(self.calculate_customized_blueprint)


        self.ui.table_3.setColumnWidth(1, 300)
        self.ui.table_3.setColumnWidth(2, 70)
        self.ui.table_3.setColumnWidth(3, 70)
        self.ui.table_3.setColumnWidth(4, 70)
        self.ui.table_3.setColumnHidden(0, True)
        self.ui.pushButton_2.clicked.connect(self.calculate_invent_data_1)

        self.ui.statusbar.showMessage('started')


        self.ui.table_4.setColumnWidth(1, 100)
        self.ui.table_4.setColumnWidth(2, 70)
        self.ui.table_4.setColumnWidth(3, 70)
        self.ui.table_4.setColumnWidth(4, 70)
        self.ui.table_4.setColumnHidden(0, True)

        self.ui.tabWidget.tabBarClicked.connect(self.populate_tab)

    def populate_tab(self):
        if self.ui.tab.isVisible():
            self.populate_manufacture_data()
        else:
            self.populate_invent_data()

    def show_settings(self) -> None:
        global setting_win
        setting_win.set_values(acquired_settings)
        setting_win.show()
        
    def calculate_invent_data_1(self):
        own_materials: list = []

        for i in range(0, self.ui.table_3.rowCount()):
            checkbox: CustomCheckbox = self.ui.table_3.cellWidget(i, 4)
            if checkbox is not None and checkbox.wdg.isChecked():
                own_materials.append(self.ui.table_3.item(i, 0).text())

        for i in range(0, self.ui.table_4.rowCount()):
            checkbox: CustomCheckbox = self.ui.table_4.cellWidget(i, 4)
            if checkbox is not None and checkbox.wdg.isChecked():
                own_materials.append(self.ui.table_4.item(i, 0).text())

        if self.ui.optional_reserch_material.isChecked():
            try:
                new_success_chance = float(self.ui.new_success_chance.toPlainText())
                optional_item_price = float(self.ui.optional_research_material_price.toPlainText())
            except ValueError:
                return
        else:
            new_success_chance = None
            optional_item_price = None

        self.populate_invent_data(own_materials, new_success_chance, optional_item_price, True)
        print('Calculated invent data')

    def calculate_customized_blueprint(self):
        if selected_blueprint_id == -1:
            return

        own_materials = []

        for i in range(0, self.ui.table_2.rowCount()):
            checkbox: CustomCheckbox = self.ui.table_2.cellWidget(i, 4)
            if checkbox is not None and checkbox.wdg.isChecked():
                own_materials.append(self.ui.table_2.item(i, 0).text())
        
        bp = blueprint_computer.get_blueprint_profit(blueprint_computer.get_blueprint_by_id(selected_blueprint_id), own_materials)
        self.ui.material_price.setText(pretty_print_big_number(bp['material_cost']))
        self.ui.sell.setText(pretty_print_big_number(bp['product_price']*bp['quantity']))
        self.ui.profit.setText(pretty_print_big_number(bp['profit']))

    def blueprint_selected_populate_tables(self, row, column: int = 0):
        row = self.ui.table.selectedItems()[0].row()
        global selected_blueprint_id
        selected_blueprint_id = self.ui.table.item(row, 0).text()

        self.populate_tab()

    def populate_invent_data(self, own_materials: list | None = None, new_success_chance: float | None = None, optional_item_price: float | None = None, already_exists: bool = False):
        if selected_blueprint_id is None:
            self.ui.table_3.setRowCount(0)
            self.ui.table_4.setRowCount(0)
        else:
            blueprint_invent_data = blueprint_computer.get_blueprint_invention_data(selected_blueprint_id, own_materials, new_success_chance, optional_item_price)

            if blueprint_invent_data is None:
                return

            invent_materials: dict = blueprint_invent_data['invent_materials']
            self.ui.table_3.setRowCount(len(invent_materials))
            for i, mat in enumerate(invent_materials.values()):
                self.ui.table_3.setItem(i, 0, QTableWidgetItem(str(mat['type_id'])))
                self.ui.table_3.setItem(i, 1, QTableWidgetItem(str(mat['name'])))
                self.ui.table_3.setItem(i, 2, QTableWidgetItem(str(mat['user_quantity'])))
                self.ui.table_3.setItem(i, 3, QTableWidgetItem(pretty_print_big_number(mat['total_price'])))

                if not already_exists:
                    self.ui.table_3.setCellWidget(i, 4, CustomCheckbox())

            product_materials = blueprint_invent_data['product_data']['materials']
            self.ui.table_4.setRowCount(len(product_materials))
            for i, mat in enumerate(product_materials.values()):
                self.ui.table_4.setItem(i, 0, QTableWidgetItem(str(mat['type_id'])))
                self.ui.table_4.setItem(i, 1, QTableWidgetItem(str(mat['name'])))
                self.ui.table_4.setItem(i, 2, QTableWidgetItem(str(mat['user_quantity'])))
                self.ui.table_4.setItem(i, 3, QTableWidgetItem(pretty_print_big_number(mat['total_price'])))

                if not already_exists:
                    self.ui.table_4.setCellWidget(i, 4, CustomCheckbox())

            self.ui.material_price_2.setText(pretty_print_big_number(blueprint_invent_data['average_invent_material_cost']))
            self.ui.profit_3.setText(pretty_print_big_number(blueprint_invent_data['average_profit']))
            self.ui.profit_error.setText(pretty_print_big_number(blueprint_invent_data['profit_error']))

    def populate_manufacture_data(self):
        mats = blueprint_computer.get_materials(selected_blueprint_id, get_names=True)
        self.ui.table_2.setRowCount(len(mats))
        for i, mat in enumerate(mats.values()):
            self.ui.table_2.setItem(i, 0, QTableWidgetItem(str(mat['type_id'])))
            self.ui.table_2.setItem(i, 1, QTableWidgetItem(str(mat['name'])))
            self.ui.table_2.setItem(i, 2, QTableWidgetItem(str(mat['user_quantity'])))
            self.ui.table_2.setItem(i, 3, QTableWidgetItem(pretty_print_big_number(mat['total_price'])))

            self.ui.table_2.setCellWidget(i, 4, CustomCheckbox())

    def get_token_on_push(self):
        global token
        token = token_manager.get_token()
        self.ui.characterName.setText(token['name'])

    def refresh_on_push(self):
        global blueprint_computer
        global running
        if not running:
            running = True

            self.compute_blueprints()

    def compute_blueprints(self):
        global blueprints
        blueprints = blueprint_computer.get_computed_blueprints()
        blueprints.pop('settings')
        blueprints = [v for v in sorted(blueprints.values(), key=lambda item: item['profit'], reverse=True)]
        global token
        token = blueprint_computer.token
        self.ui.characterName.setText(token['name'])

        self.ui.table.setRowCount(len(blueprints))

        for i, bp in enumerate(blueprints):
            self.ui.table.setItem(i, 0, QTableWidgetItem(str(bp['item_id'])))
            self.ui.table.setItem(i, 1, QTableWidgetItem(bp['name']))
            self.ui.table.setItem(i, 2, QTableWidgetItem(pretty_print_big_number(bp['profit'])))
            self.ui.table.setItem(i, 3, QTableWidgetItem(pretty_print_big_number(bp['job_cost'])))
        else:
            if self.ui.table.rowCount() > i + 1:
                for e in range(i + 1, self.ui.table.rowCount() - 2):
                    print(f'removed row at {e}')
                    self.ui.table.removeRow(e)

        global running
        running = False

class SettingsWindow(QWidget):
    def __init__(self) -> None:
        super(SettingsWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.reset_btn.clicked.connect(self.reset)
        self.ui.apply_btn.clicked.connect(self.apply)

    def reset(self):
        self.set_values(DEFAUL_SETTINGS)

    def set_values(self, settings: dict):
        self.ui.system_of_interest_id.setText(str(settings['system_of_interest_id']))
        self.ui.region_of_interest_id.setText(str(settings['region_of_interest_id']))
        self.ui.structure_of_interest_location_id.setText(str(settings['structure_of_interest_location_id']))
        self.ui.manufacturing_tax.setText(str(settings['manufacturing_tax']))
        self.ui.sales_tax.setText(str(settings['sales_tax']))
        self.ui.material_efficiency_from_structure.setText(str(settings['material_efficiency_from_structure']))
        self.ui.statistical_significance.setText(str(settings['statistical_significance']))
        self.ui.price_deprecation_time.setText(str(settings['price_deprecation_time_in_seconds']))
        self.ui.use_average_material_prices.setChecked(settings['use_average_material_prices'])
        self.ui.use_average_product_prices.setChecked(settings['use_average_product_prices'])

    def apply(self) -> None:
        acquired_settings
        try:
            acquired_settings['system_of_interest_id'] = int(self.ui.system_of_interest_id.toPlainText())
            acquired_settings['region_of_interest_id'] = int(self.ui.region_of_interest_id.toPlainText())
            acquired_settings['structure_of_interest_location_id'] = int(self.ui.structure_of_interest_location_id.toPlainText())
            acquired_settings['manufacturing_tax'] = float(self.ui.manufacturing_tax.toPlainText())
            acquired_settings['sales_tax'] = float(self.ui.sales_tax.toPlainText())
            acquired_settings['material_efficiency_from_structure'] = float(self.ui.material_efficiency_from_structure.toPlainText())
            acquired_settings['statistical_significance'] = float(self.ui.statistical_significance.toPlainText())
            acquired_settings['price_deprecation_time_in_seconds'] = int(self.ui.price_deprecation_time.toPlainText())
        except ValueError:
            print('Wrong values.')
            return

        acquired_settings['use_average_material_prices'] = self.ui.use_average_material_prices.isChecked()
        acquired_settings['use_average_product_prices'] = self.ui.use_average_product_prices.isChecked()

        global settings
        settings = acquired_settings
        apply_settings()
        self.close()

setting_win: SettingsWindow

def apply_settings():
    prices.apply_settings(settings)
    blueprint_computer.apply_settings(settings)
    save_json(settings, 'settings.json')

def app():
    app = QApplication(sys.argv)
    global setting_win
    setting_win = SettingsWindow()
    win = Window()

    global token_requester, blueprint_computer, token_manager, prices, acquired_settings
    
    token_requester = TokenRequester(
        client_id = client_id,
        host = host,
        port = port,
        callback_uri = "http://127.0.0.1:5050/callback",
        login_url = "https://login.eveonline.com/v2/oauth/authorize",
        get_token_url = "https://login.eveonline.com/v2/oauth/token",
        sso_metadata_url = "https://login.eveonline.com/.well-known/oauth-authorization-server",
        jwk_audience = "EVE Online",
        token_host_url = "login.eveonline.com"
    )

    token_manager = TokenManager(token_requester, SCOPES, store_tokens = True)

    acquired_settings = load_json('settings.json')
    if acquired_settings is None:
        acquired_settings = DEFAUL_SETTINGS
    #win.show_settings(settings)

    prices = Prices(settings=acquired_settings)

    blueprint_computer = BlueprintComputer(token_manager, prices, settings=acquired_settings)

    utils.message_target = win.ui.statusbar.showMessage

    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    profile = cProfile.Profile()
    app()