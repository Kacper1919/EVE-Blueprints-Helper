# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(608, 482)
        Form.setStyleSheet("*{\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    background: rgba(0, 0, 0, 0);\n"
"    padding: 0;\n"
"    border: none;\n"
"    color: #fff;\n"
"}\n"
"#Form{\n"
"    background-image: url(img/background.jpg);\n"
"}\n"
"#header{\n"
"    background-color: rgba(9, 9, 9, 200);\n"
"}\n"
"QPushButton{\n"
"    border: 2px solid rgb(160, 160, 160);\n"
"    border-radius: 4px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgba(153, 153, 153, 170);\n"
"}\n"
"QTextEdit{\n"
"    border: 2px solid rgba(50,50,50,255);\n"
"}")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_11 = QtWidgets.QWidget(parent=self.widget)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_10.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(parent=self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(0, 30))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.structure_of_interest_location_id = QtWidgets.QTextEdit(parent=self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.structure_of_interest_location_id.sizePolicy().hasHeightForWidth())
        self.structure_of_interest_location_id.setSizePolicy(sizePolicy)
        self.structure_of_interest_location_id.setMinimumSize(QtCore.QSize(0, 30))
        self.structure_of_interest_location_id.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.structure_of_interest_location_id.setFont(font)
        self.structure_of_interest_location_id.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.structure_of_interest_location_id.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.structure_of_interest_location_id.setObjectName("structure_of_interest_location_id")
        self.horizontalLayout_10.addWidget(self.structure_of_interest_location_id)
        self.verticalLayout.addWidget(self.widget_11)
        self.widget_10 = QtWidgets.QWidget(parent=self.widget)
        self.widget_10.setObjectName("widget_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_10)
        self.horizontalLayout.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_12 = QtWidgets.QLabel(parent=self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(0, 30))
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.material_efficiency_from_structure = QtWidgets.QTextEdit(parent=self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.material_efficiency_from_structure.sizePolicy().hasHeightForWidth())
        self.material_efficiency_from_structure.setSizePolicy(sizePolicy)
        self.material_efficiency_from_structure.setMinimumSize(QtCore.QSize(0, 30))
        self.material_efficiency_from_structure.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.material_efficiency_from_structure.setFont(font)
        self.material_efficiency_from_structure.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.material_efficiency_from_structure.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.material_efficiency_from_structure.setObjectName("material_efficiency_from_structure")
        self.horizontalLayout.addWidget(self.material_efficiency_from_structure)
        self.verticalLayout.addWidget(self.widget_10)
        self.widget_8 = QtWidgets.QWidget(parent=self.widget)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_6.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(parent=self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.region_of_interest_id = QtWidgets.QTextEdit(parent=self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.region_of_interest_id.sizePolicy().hasHeightForWidth())
        self.region_of_interest_id.setSizePolicy(sizePolicy)
        self.region_of_interest_id.setMinimumSize(QtCore.QSize(0, 30))
        self.region_of_interest_id.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.region_of_interest_id.setFont(font)
        self.region_of_interest_id.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.region_of_interest_id.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.region_of_interest_id.setObjectName("region_of_interest_id")
        self.horizontalLayout_6.addWidget(self.region_of_interest_id)
        self.verticalLayout.addWidget(self.widget_8)
        self.widget_7 = QtWidgets.QWidget(parent=self.widget)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_5.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(parent=self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 30))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setToolTip("30000142")
        self.label_4.setToolTipDuration(1)
        self.label_4.setStatusTip("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.system_of_interest_id = QtWidgets.QTextEdit(parent=self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.system_of_interest_id.sizePolicy().hasHeightForWidth())
        self.system_of_interest_id.setSizePolicy(sizePolicy)
        self.system_of_interest_id.setMinimumSize(QtCore.QSize(0, 30))
        self.system_of_interest_id.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.system_of_interest_id.setFont(font)
        self.system_of_interest_id.setWhatsThis("")
        self.system_of_interest_id.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.system_of_interest_id.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.system_of_interest_id.setAutoFormatting(QtWidgets.QTextEdit.AutoFormattingFlag.AutoNone)
        self.system_of_interest_id.setAcceptRichText(False)
        self.system_of_interest_id.setPlaceholderText("")
        self.system_of_interest_id.setObjectName("system_of_interest_id")
        self.horizontalLayout_5.addWidget(self.system_of_interest_id)
        self.verticalLayout.addWidget(self.widget_7)
        self.widget_6 = QtWidgets.QWidget(parent=self.widget)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_16 = QtWidgets.QLabel(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QtCore.QSize(0, 30))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setToolTip("30000142")
        self.label_16.setToolTipDuration(1)
        self.label_16.setStatusTip("")
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_4.addWidget(self.label_16)
        self.statistical_significance = QtWidgets.QTextEdit(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statistical_significance.sizePolicy().hasHeightForWidth())
        self.statistical_significance.setSizePolicy(sizePolicy)
        self.statistical_significance.setMinimumSize(QtCore.QSize(0, 30))
        self.statistical_significance.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.statistical_significance.setFont(font)
        self.statistical_significance.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.statistical_significance.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.statistical_significance.setObjectName("statistical_significance")
        self.horizontalLayout_4.addWidget(self.statistical_significance)
        self.verticalLayout.addWidget(self.widget_6)
        self.widget_5 = QtWidgets.QWidget(parent=self.widget)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(parent=self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.manufacturing_tax = QtWidgets.QTextEdit(parent=self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manufacturing_tax.sizePolicy().hasHeightForWidth())
        self.manufacturing_tax.setSizePolicy(sizePolicy)
        self.manufacturing_tax.setMinimumSize(QtCore.QSize(0, 30))
        self.manufacturing_tax.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.manufacturing_tax.setFont(font)
        self.manufacturing_tax.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.manufacturing_tax.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.manufacturing_tax.setObjectName("manufacturing_tax")
        self.horizontalLayout_3.addWidget(self.manufacturing_tax)
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_3 = QtWidgets.QWidget(parent=self.widget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(parent=self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 30))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.sales_tax = QtWidgets.QTextEdit(parent=self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sales_tax.sizePolicy().hasHeightForWidth())
        self.sales_tax.setSizePolicy(sizePolicy)
        self.sales_tax.setMinimumSize(QtCore.QSize(0, 30))
        self.sales_tax.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sales_tax.setFont(font)
        self.sales_tax.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sales_tax.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sales_tax.setObjectName("sales_tax")
        self.horizontalLayout_2.addWidget(self.sales_tax)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_9 = QtWidgets.QWidget(parent=self.widget)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_7.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(parent=self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(0, 30))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.price_deprecation_time = QtWidgets.QTextEdit(parent=self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.price_deprecation_time.sizePolicy().hasHeightForWidth())
        self.price_deprecation_time.setSizePolicy(sizePolicy)
        self.price_deprecation_time.setMinimumSize(QtCore.QSize(0, 30))
        self.price_deprecation_time.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.price_deprecation_time.setFont(font)
        self.price_deprecation_time.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.price_deprecation_time.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.price_deprecation_time.setObjectName("price_deprecation_time")
        self.horizontalLayout_7.addWidget(self.price_deprecation_time)
        self.verticalLayout.addWidget(self.widget_9)
        self.use_average_product_prices = QtWidgets.QCheckBox(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.use_average_product_prices.setFont(font)
        self.use_average_product_prices.setObjectName("use_average_product_prices")
        self.verticalLayout.addWidget(self.use_average_product_prices)
        self.use_average_material_prices = QtWidgets.QCheckBox(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.use_average_material_prices.setFont(font)
        self.use_average_material_prices.setObjectName("use_average_material_prices")
        self.verticalLayout.addWidget(self.use_average_material_prices)
        self.widget_2 = QtWidgets.QWidget(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 60))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_8.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.apply_btn = QtWidgets.QPushButton(parent=self.widget_2)
        self.apply_btn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.apply_btn.setFont(font)
        self.apply_btn.setObjectName("apply_btn")
        self.horizontalLayout_8.addWidget(self.apply_btn)
        self.reset_btn = QtWidgets.QPushButton(parent=self.widget_2)
        self.reset_btn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.reset_btn.setFont(font)
        self.reset_btn.setObjectName("reset_btn")
        self.horizontalLayout_8.addWidget(self.reset_btn)
        self.verticalLayout.addWidget(self.widget_2)
        self.verticalLayout_3.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Settings"))
        self.label_10.setText(_translate("Form", "structure location id"))
        self.structure_of_interest_location_id.setStatusTip(_translate("Form", "Jita 4-4 TH: 60003760"))
        self.label_12.setText(_translate("Form", "material efficiency bonus from structure"))
        self.label_5.setText(_translate("Form", "region id"))
        self.region_of_interest_id.setStatusTip(_translate("Form", "The Forge: 10000002"))
        self.label_4.setText(_translate("Form", "system id"))
        self.system_of_interest_id.setStatusTip(_translate("Form", "Jita: 30000142"))
        self.label_16.setText(_translate("Form", "statistical significance"))
        self.statistical_significance.setStatusTip(_translate("Form", "The Forge: 10000002"))
        self.label_7.setText(_translate("Form", "manufacturing tax"))
        self.label_8.setText(_translate("Form", "sales tax"))
        self.label_6.setText(_translate("Form", "price deprecation time [seconds]"))
        self.price_deprecation_time.setStatusTip(_translate("Form", "Jita 4-4 TH: 60003760"))
        self.use_average_product_prices.setText(_translate("Form", "use average product prices"))
        self.use_average_material_prices.setText(_translate("Form", "use average material prices"))
        self.apply_btn.setText(_translate("Form", "apply"))
        self.reset_btn.setText(_translate("Form", "reset"))
