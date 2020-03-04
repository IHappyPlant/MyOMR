# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml_creator/xml_creator.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(843, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.mainTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.mainTab)
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 505))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(0, 0, 381, 511))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "                                                            ")
        self.label.setText("")
        self.label.setObjectName("label")
        self.scrollArea.setWidget(self.label)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.images_list = QtWidgets.QListWidget(self.mainTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.images_list.sizePolicy().hasHeightForWidth())
        self.images_list.setSizePolicy(sizePolicy)
        self.images_list.setObjectName("images_list")
        self.horizontalLayout.addWidget(self.images_list)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.add_to_model_button = QtWidgets.QPushButton(self.mainTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.add_to_model_button.sizePolicy().hasHeightForWidth())
        self.add_to_model_button.setSizePolicy(sizePolicy)
        self.add_to_model_button.setObjectName("add_to_model_button")
        self.gridLayout_2.addWidget(self.add_to_model_button, 2, 0, 1, 1)
        self.type_label = QtWidgets.QLabel(self.mainTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.type_label.sizePolicy().hasHeightForWidth())
        self.type_label.setSizePolicy(sizePolicy)
        self.type_label.setObjectName("type_label")
        self.gridLayout_2.addWidget(self.type_label, 0, 0, 1, 1)
        self.types_box = QtWidgets.QComboBox(self.mainTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.types_box.sizePolicy().hasHeightForWidth())
        self.types_box.setSizePolicy(sizePolicy)
        self.types_box.setObjectName("types_box")
        self.types_box.addItem("")
        self.types_box.addItem("")
        self.types_box.addItem("")
        self.gridLayout_2.addWidget(self.types_box, 1, 0, 1, 1)
        self.folder_select_button = QtWidgets.QPushButton(self.mainTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.folder_select_button.sizePolicy().hasHeightForWidth())
        self.folder_select_button.setSizePolicy(sizePolicy)
        self.folder_select_button.setObjectName("folder_select_button")
        self.gridLayout_2.addWidget(self.folder_select_button, 3, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.point_coords_output = QtWidgets.QTextEdit(self.mainTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.point_coords_output.sizePolicy().hasHeightForWidth())
        self.point_coords_output.setSizePolicy(sizePolicy)
        self.point_coords_output.setMinimumSize(QtCore.QSize(0, 50))
        self.point_coords_output.setMaximumSize(QtCore.QSize(16777215, 50))
        self.point_coords_output.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.point_coords_output.setObjectName("point_coords_output")
        self.verticalLayout_2.addWidget(self.point_coords_output)
        self.tabWidget.addTab(self.mainTab, "")
        self.schema_tab = QtWidgets.QWidget()
        self.schema_tab.setObjectName("schema_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.schema_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.schema_output = QtWidgets.QTextEdit(self.schema_tab)
        self.schema_output.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.schema_output.setObjectName("schema_output")
        self.horizontalLayout_2.addWidget(self.schema_output)
        self.objects_list_view = QtWidgets.QTreeView(self.schema_tab)
        self.objects_list_view.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.objects_list_view.setObjectName("objects_list_view")
        self.horizontalLayout_2.addWidget(self.objects_list_view)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.save_schema_button = QtWidgets.QPushButton(self.schema_tab)
        self.save_schema_button.setObjectName("save_schema_button")
        self.horizontalLayout_3.addWidget(self.save_schema_button)
        self.delete_object_button = QtWidgets.QPushButton(self.schema_tab)
        self.delete_object_button.setObjectName("delete_object_button")
        self.horizontalLayout_3.addWidget(self.delete_object_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.schema_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "XML Creator"))
        self.add_to_model_button.setText(
            _translate("MainWindow", "Add to model"))
        self.type_label.setText(_translate("MainWindow", "Object type:"))
        self.types_box.setItemText(0, _translate("MainWindow",
                                                 "unfilled checkbox"))
        self.types_box.setItemText(1,
                                   _translate("MainWindow", "filled checkbox"))
        self.types_box.setItemText(2, _translate("MainWindow", "checkmark"))
        self.folder_select_button.setText(
            _translate("MainWindow", "Select folder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab),
                                  _translate("MainWindow", "Main"))
        self.save_schema_button.setText(_translate("MainWindow", "Save Schema"))
        self.delete_object_button.setText(
            _translate("MainWindow", "Delete object"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.schema_tab),
                                  _translate("MainWindow", "Display Schema"))
