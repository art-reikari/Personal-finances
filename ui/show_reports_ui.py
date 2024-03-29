# Form implementation generated from reading ui file 'show_reports_ui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(796, 593)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 791, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_frm = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_frm.setContentsMargins(0, 0, 0, 0)
        self.main_frm.setSpacing(0)
        self.main_frm.setObjectName("main_frm")
        self.title = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(0, 48))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(32)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.title.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        self.main_frm.addWidget(self.title)
        self.settings_frm = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_frm.sizePolicy().hasHeightForWidth())
        self.settings_frm.setSizePolicy(sizePolicy)
        self.settings_frm.setMinimumSize(QtCore.QSize(0, 57))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(12)
        self.settings_frm.setFont(font)
        self.settings_frm.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.settings_frm.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.settings_frm.setObjectName("settings_frm")
        self.gridLayout = QtWidgets.QGridLayout(self.settings_frm)
        self.gridLayout.setContentsMargins(25, -1, 25, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.report_type_cmbbox = QtWidgets.QComboBox(parent=self.settings_frm)
        font = QtGui.QFont()
        font.setFamily("Candara Light")
        font.setPointSize(14)
        self.report_type_cmbbox.setFont(font)
        self.report_type_cmbbox.setObjectName("report_type_cmbbox")
        self.report_type_cmbbox.addItem("")
        self.report_type_cmbbox.setItemText(0, "")
        self.report_type_cmbbox.addItem("")
        self.report_type_cmbbox.addItem("")
        self.report_type_cmbbox.addItem("")
        self.gridLayout.addWidget(self.report_type_cmbbox, 0, 0, 1, 1)
        self.first_month_cmbbox = QtWidgets.QComboBox(parent=self.settings_frm)
        font = QtGui.QFont()
        font.setFamily("Candara Light")
        font.setPointSize(14)
        self.first_month_cmbbox.setFont(font)
        self.first_month_cmbbox.setObjectName("first_month_cmbbox")
        self.gridLayout.addWidget(self.first_month_cmbbox, 1, 0, 1, 1)
        self.last_mont_cmbbox = QtWidgets.QComboBox(parent=self.settings_frm)
        font = QtGui.QFont()
        font.setFamily("Candara Light")
        font.setPointSize(14)
        self.last_mont_cmbbox.setFont(font)
        self.last_mont_cmbbox.setObjectName("last_mont_cmbbox")
        self.gridLayout.addWidget(self.last_mont_cmbbox, 1, 1, 1, 1)
        self.load_report_btn = QtWidgets.QPushButton(parent=self.settings_frm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_report_btn.sizePolicy().hasHeightForWidth())
        self.load_report_btn.setSizePolicy(sizePolicy)
        self.load_report_btn.setMinimumSize(QtCore.QSize(112, 0))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(14)
        self.load_report_btn.setFont(font)
        self.load_report_btn.setObjectName("load_report_btn")
        self.gridLayout.addWidget(self.load_report_btn, 0, 5, 2, 1)
        self.grouping_cmbbox = QtWidgets.QComboBox(parent=self.settings_frm)
        font = QtGui.QFont()
        font.setFamily("Candara Light")
        font.setPointSize(14)
        self.grouping_cmbbox.setFont(font)
        self.grouping_cmbbox.setObjectName("grouping_cmbbox")
        self.gridLayout.addWidget(self.grouping_cmbbox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(104, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 2, 1)
        self.main_frm.addWidget(self.settings_frm)
        self.report_table = QtWidgets.QTableWidget(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setBold(True)
        self.report_table.setFont(font)
        self.report_table.setDragDropOverwriteMode(True)
        self.report_table.setShowGrid(True)
        self.report_table.setObjectName("report_table")
        self.report_table.setColumnCount(0)
        self.report_table.setRowCount(0)
        self.main_frm.addWidget(self.report_table)
        self.return_frm = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.return_frm.sizePolicy().hasHeightForWidth())
        self.return_frm.setSizePolicy(sizePolicy)
        self.return_frm.setMinimumSize(QtCore.QSize(0, 49))
        self.return_frm.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.return_frm.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.return_frm.setObjectName("return_frm")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.return_frm)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.return_btn = QtWidgets.QPushButton(parent=self.return_frm)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(12)
        self.return_btn.setFont(font)
        self.return_btn.setObjectName("return_btn")
        self.horizontalLayout_2.addWidget(self.return_btn)
        self.main_frm.addWidget(self.return_frm)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Show reports"))
        self.title.setText(_translate("Form", "Reports"))
        self.report_type_cmbbox.setPlaceholderText(_translate("Form", "Choose report"))
        self.report_type_cmbbox.setItemText(1, _translate("Form", "Earnings"))
        self.report_type_cmbbox.setItemText(2, _translate("Form", "Expenses"))
        self.report_type_cmbbox.setItemText(3, _translate("Form", "Savings"))
        self.first_month_cmbbox.setPlaceholderText(_translate("Form", "First month"))
        self.last_mont_cmbbox.setPlaceholderText(_translate("Form", "Last month"))
        self.load_report_btn.setText(_translate("Form", "Load report"))
        self.grouping_cmbbox.setPlaceholderText(_translate("Form", "Choose grouping"))
        self.report_table.setSortingEnabled(False)
        self.return_btn.setText(_translate("Form", "Return"))
