import sys
import backend
import PyQt6
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QComboBox
from ui import main_window_ui
from ui import add_earnings_or_expenses_ui
from ui import show_reports_ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.new_window = None
        self.db = 'finances_db.db'

        self.year = backend.get_current_year()
        self.month = backend.get_current_month_numeric()
        self.ui.month_year_lbl.setText(
            f'{backend.get_current_month_str()}, {self.year}')
        self.savings = None

        backend.create_expense_categories_table(self.db)
        backend.create_expense_subcategories_table(self.db)
        backend.create_product_service_table(self.db)
        backend.create_expenses_table(self.db)
        backend.create_earning_categories_table(self.db)
        backend.create_earning_types_table(self.db)
        backend.create_earnings_table(self.db)
        backend.create_savings_table(self.db)

        if backend.check_if_savings_empty(self.db):
            self.ui.main_frm.hide()
            self.ui.input_current_savings_frm.show()
        else:
            self.ui.main_frm.show()
            self.ui.input_current_savings_frm.hide()
            if backend.check_if_current_month_savings_empty(self.db, self.month, self.year):
                backend.add_savings(self.db, self.month, self.year, backend.get_last_month_savings(self.db, self.month,
                                                                                                   self.year))
            self.update_savings_info()

        self.ui.add_earnings_expenses_btn.clicked.connect(
            lambda: new_window_btn_clicked(self, AddExpensesEarningsWindow))
        self.ui.show_reports_btn.clicked.connect(lambda: new_window_btn_clicked(self, ShowReportsWindow))
        # self.ui.settings_btn.clicked.connect(self.settings_btn_clicked)
        self.ui.input_current_savings_btn.clicked.connect(self.input_current_savings_btn_clicked)

    def btn_clicked(self):
        window = ShowReportsWindow(self)
        window.show()
        self.close()

    def update_savings_info(self):
        self.savings = str(backend.get_current_month_savings(self.db, self.month, self.year))
        self.ui.savings_lbl.setText('Savings: ' + self.savings)

    def input_current_savings_btn_clicked(self):
        backend.add_savings(self.db, self.month, self.year, self.ui.current_savings_inpt.text())
        self.ui.input_current_savings_frm.hide()
        self.ui.main_frm.show()
        self.update_savings_info()


class AddExpensesEarningsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = add_earnings_or_expenses_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.new_category_inpt.hide()
        self.ui.new_subcategory_inpt.hide()
        for element in self.ui.info_frm.children():
            if isinstance(element, PyQt6.QtWidgets.QGridLayout):
                continue
            element.hide()

        self.ui.choose_type_cmbbox.currentTextChanged.connect(self.type_changed)
        self.ui.category_cmbbox.currentTextChanged.connect(self.category_changed)
        self.ui.subcategory_cmbbox.currentTextChanged.connect(self.subcategory_changed)
        self.ui.product_service_cmbbox.currentTextChanged.connect(self.product_service_changed)
        self.ui.add_btn.clicked.connect(self.add_btn_clicked)

        self.ui.return_btn.clicked.connect(lambda: return_btn_clicked(self, parent))

    def type_changed(self):
        if self.ui.choose_type_cmbbox.currentText() == 'Earnings':
            self.ui.category_lbl.show()
            self.ui.category_cmbbox.show()
            self.ui.total_lbl.show()
            self.ui.total_inpt.show()
            self.ui.subcategory_lbl.show()
            self.ui.subcategory_lbl.setText('Type')
            self.ui.subcategory_cmbbox.show()
            self.ui.subcategory_cmbbox.setEnabled(True)
            self.ui.product_service_lbl.hide()
            self.ui.product_service_cmbbox.hide()
            self.ui.product_service_cmbbox.setDisabled(True)
            self.ui.qty_lbl.hide()
            self.ui.qty_inpt.hide()
            self.ui.qty_inpt.setDisabled(True)
            self.ui.add_btn_frm.show()
            self.ui.category_cmbbox.clear()
            self.ui.subcategory_cmbbox.clear()
            self.ui.product_service_cmbbox.clear()
            update_cmbbox(self.ui.category_cmbbox, 'category', backend.get_all_earning_categories, finances.db)
        elif self.ui.choose_type_cmbbox.currentText() == 'Expenses':
            self.ui.category_lbl.show()
            self.ui.category_cmbbox.show()
            self.ui.total_lbl.show()
            self.ui.total_inpt.show()
            self.ui.subcategory_lbl.show()
            self.ui.subcategory_lbl.setText('Subcategory')
            self.ui.subcategory_cmbbox.show()
            self.ui.subcategory_cmbbox.setEnabled(True)
            self.ui.product_service_lbl.show()
            self.ui.product_service_cmbbox.show()
            self.ui.product_service_cmbbox.setEnabled(True)
            self.ui.qty_lbl.show()
            self.ui.qty_inpt.show()
            self.ui.qty_inpt.setEnabled(True)
            update_cmbbox(self.ui.category_cmbbox, 'category', backend.get_all_expense_categories, finances.db)
            self.ui.add_btn_frm.show()
        else:
            for element in self.ui.info_frm.children():
                if isinstance(element, PyQt6.QtWidgets.QGridLayout):
                    continue
                element.hide()

    def category_changed(self):
        if self.ui.choose_type_cmbbox.currentText() == 'Earnings':
            if self.ui.category_cmbbox.currentText() == 'Add new category':
                self.ui.new_category_inpt.show()
                update_cmbbox(self.ui.subcategory_cmbbox, 'type', backend.get_all_earning_types_in_category,
                              finances.db)
            else:
                self.ui.new_category_inpt.hide()
                update_cmbbox(self.ui.subcategory_cmbbox, 'type', backend.get_all_earning_types_in_category,
                              finances.db, self.ui.category_cmbbox.currentText())
        else:
            if self.ui.category_cmbbox.currentText() == 'Add new category':
                self.ui.new_category_inpt.show()
                update_cmbbox(self.ui.subcategory_cmbbox, 'subcategory',
                              backend.get_all_expense_subcategories_in_category, finances.db)
            else:
                self.ui.new_category_inpt.hide()
                update_cmbbox(self.ui.subcategory_cmbbox, 'subcategory',
                              backend.get_all_expense_subcategories_in_category,
                              finances.db, self.ui.category_cmbbox.currentText())
                if not backend.get_all_expense_subcategories_in_category(self.ui.category_cmbbox.currentText(),
                                                                         finances.db):
                    update_cmbbox(self.ui.product_service_cmbbox, 'type',
                                  backend.get_all_products_services_in_subcategory, finances.db,
                                  self.ui.category_cmbbox.currentText())

    def subcategory_changed(self):
        if self.ui.choose_type_cmbbox.currentText() == 'Earnings':
            if self.ui.subcategory_cmbbox.currentText() == 'Add new type':
                self.ui.new_subcategory_inpt.show()
            else:
                self.ui.new_subcategory_inpt.hide()
        else:
            if self.ui.subcategory_cmbbox.currentText() == 'Add new subcategory':
                self.ui.new_subcategory_inpt.show()
                update_cmbbox(self.ui.product_service_cmbbox, 'product or service',
                              backend.get_all_products_services_in_subcategory, finances.db, None)
            else:
                self.ui.new_subcategory_inpt.hide()
                update_cmbbox(self.ui.product_service_cmbbox, 'product or service',
                              backend.get_all_products_services_in_subcategory,
                              finances.db, self.ui.subcategory_cmbbox.currentText())

    def product_service_changed(self):
        if self.ui.product_service_cmbbox.currentText() == 'Add new product or service':
            self.ui.new_product_service_inpt.show()
        else:
            self.ui.new_product_service_inpt.hide()

    def add_btn_clicked(self):
        if self.ui.choose_type_cmbbox.currentText() == 'Earnings':
            if self.ui.new_category_inpt.isVisible():
                earning_category = self.ui.new_category_inpt.text()
                backend.add_earning_category(earning_category, finances.db)
            else:
                earning_category = self.ui.category_cmbbox.currentText()
            if self.ui.new_subcategory_inpt.isVisible():
                earning_type = self.ui.new_subcategory_inpt.text()
                backend.add_earning_type(earning_type, earning_category, finances.db)
            else:
                earning_type = self.ui.subcategory_cmbbox.currentText()
            amount = float(self.ui.total_inpt.text())
            if self.ui.category_cmbbox.currentText() == 'Add new category':
                update_cmbbox(self.ui.category_cmbbox, 'category', backend.get_all_earning_categories, finances.db)
            backend.add_earnings(earning_type, finances.month, finances.year, amount, finances.db)
        else:
            # print('We are inside first if!')
            if self.ui.new_category_inpt.isVisible():
                category = self.ui.new_category_inpt.text()
                backend.add_expense_category(category, finances.db)
            else:
                category = self.ui.category_cmbbox.currentText()
            if self.ui.new_subcategory_inpt.isVisible():
                # print('We change our subcategory!')
                subcategory = self.ui.new_subcategory_inpt.text()
                backend.add_expense_subcategory(subcategory, category, finances.db)
            else:
                subcategory = self.ui.subcategory_cmbbox.currentText()
            if self.ui.new_product_service_inpt.isVisible():
                # print('We change our product_service!')
                product_service = self.ui.new_product_service_inpt.text()
                backend.add_product_service(product_service, subcategory, finances.db)
            else:
                product_service = self.ui.product_service_cmbbox.currentText()
            qty = float(self.ui.qty_inpt.text())
            total = float(self.ui.total_inpt.text())
            backend.add_expenses(product_service, finances.month, finances.year,
                                 qty, total, finances.db)
            if self.ui.category_cmbbox.currentText() == 'Add new category':
                update_cmbbox(self.ui.category_cmbbox, 'category', backend.get_all_expense_categories, finances.db)
        for element in self.ui.info_frm.children():
            if isinstance(element, QLineEdit):
                element.clear()
            elif isinstance(element, QComboBox):
                element.setCurrentIndex(0)
            else:
                pass
        finances.update_savings_info()


class ShowReportsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = show_reports_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.grouping_cmbbox.setDisabled(True)
        self.ui.load_report_btn.setDisabled(True)
        self.ui.first_month_cmbbox.setDisabled(True)
        self.ui.last_mont_cmbbox.setDisabled(True)
        self.ui.report_table.hide()

        self.ui.report_type_cmbbox.currentTextChanged.connect(self.report_type_changed)
        self.ui.grouping_cmbbox.currentTextChanged.connect(self.grouping_changed)
        self.ui.load_report_btn.clicked.connect(self.load_report)

        self.ui.return_btn.clicked.connect(lambda: return_btn_clicked(self, parent))

    def report_type_changed(self):
        self.ui.load_report_btn.setDisabled(True)
        if self.ui.report_type_cmbbox.currentText() == 'Earnings':
            self.ui.grouping_cmbbox.clear()
            self.ui.grouping_cmbbox.setEnabled(True)
            self.ui.grouping_cmbbox.addItems([''] + ['Category', 'Type'])
            self.ui.db_months_str = backend.get_months_from_db('Earnings', finances.db)
            self.ui.first_month_cmbbox.setEnabled(True)
            self.ui.first_month_cmbbox.clear()
            self.ui.first_month_cmbbox.addItems([] + self.ui.db_months_str)
            self.ui.last_mont_cmbbox.setEnabled(True)
            self.ui.last_mont_cmbbox.clear()
            self.ui.last_mont_cmbbox.addItems([] + self.ui.db_months_str)
        elif self.ui.report_type_cmbbox.currentText() == 'Expenses':
            self.ui.grouping_cmbbox.clear()
            self.ui.grouping_cmbbox.setEnabled(True)
            self.ui.grouping_cmbbox.addItems([''] + ['Category', 'Subcategory', 'Product/service'])
            self.ui.db_months_str = backend.get_months_from_db('Expenses', finances.db)
            self.ui.first_month_cmbbox.setEnabled(True)
            self.ui.first_month_cmbbox.clear()
            self.ui.first_month_cmbbox.addItems([] + self.ui.db_months_str)
            self.ui.last_mont_cmbbox.setEnabled(True)
            self.ui.last_mont_cmbbox.clear()
            self.ui.last_mont_cmbbox.addItems([] + self.ui.db_months_str)
        elif self.ui.report_type_cmbbox.currentText() == 'Savings':
            self.ui.grouping_cmbbox.clear()
            self.ui.grouping_cmbbox.setDisabled(True)
            self.ui.db_months_str = backend.get_months_from_db('Savings', finances.db)
            self.ui.first_month_cmbbox.setEnabled(True)
            self.ui.first_month_cmbbox.clear()
            self.ui.first_month_cmbbox.addItems([] + self.ui.db_months_str)
            self.ui.last_mont_cmbbox.setEnabled(True)
            self.ui.last_mont_cmbbox.clear()
            self.ui.last_mont_cmbbox.addItems([] + self.ui.db_months_str)
            self.ui.load_report_btn.setEnabled(True)
        else:
            self.ui.report_table.hide()
            self.ui.first_month_cmbbox.setDisabled(True)
            self.ui.first_month_cmbbox.clear()
            self.ui.last_mont_cmbbox.setDisabled(True)
            self.ui.last_mont_cmbbox.clear()

    def grouping_changed(self):
        if self.ui.grouping_cmbbox.currentText() != '':
            self.ui.load_report_btn.setEnabled(True)
        else:
            self.ui.load_report_btn.setDisabled(True)

    def load_report(self):
        if self.ui.first_month_cmbbox.currentText() == '' or self.ui.last_mont_cmbbox.currentText() == '':
            return
        months_list_numeric = backend.turn_month_year_strs_to_numeric_tuples(self.ui.first_month_cmbbox.currentText(),
                                                                             self.ui.last_mont_cmbbox.currentText())
        self.ui.report_table.show()
        self.ui.report_table.clear()
        if self.ui.report_type_cmbbox.currentText() == 'Earnings':
            if self.ui.grouping_cmbbox.currentText() == 'Category':
                report_lists = backend.make_several_months_earnings_report('Earning_category_name',
                                                                           months_list_numeric, 'Earning_category_name',
                                                                           finances.db)
            elif self.ui.grouping_cmbbox.currentText() == 'Type':
                report_lists = backend.make_several_months_earnings_report('Earning_type_name, Earning_category_name',
                                                                           months_list_numeric, 'Earning_type_name',
                                                                           finances.db)
            else:
                return
            header_font = QtGui.QFont()
            header_font.setFamily("Candara")
            header_font.setPointSize(12)
            header_font.setBold(True)
            self.ui.report_table.clear()
            self.ui.report_table.setColumnCount(len(report_lists))
            # print(report_lists)
            row_count = len(report_lists[0])
            self.ui.report_table.setRowCount(row_count)
            for row_num, data in enumerate(report_lists[0]):
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                self.ui.report_table.setVerticalHeaderItem(row_num, item)
                # print(data)
                self.ui.report_table.verticalHeaderItem(row_num).setText(data[0])
            for col_num, zipped_data in enumerate(zip(months_list_numeric, report_lists)):
                # print(f'Zipped data: {zipped_data}')
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                self.ui.report_table.setHorizontalHeaderItem(col_num, item)
                self.ui.report_table.horizontalHeaderItem(col_num).setText(
                    f'{backend.turn_numeric_month_to_str(zipped_data[0][0])}, {zipped_data[0][1]}')
                month_table = QtWidgets.QTableWidget()
                month_table.setColumnCount(1)
                month_table.setRowCount(len(zipped_data[1]))
                data_font = QtGui.QFont()
                data_font.setFamily("Candara")
                data_font.setPointSize(10)
                data_font.setBold(False)
                total_font = QtGui.QFont()
                total_font.isCopyOf(data_font)
                total_font.setBold(True)
                for row_num, row in enumerate(zipped_data[1]):
                    if self.ui.grouping_cmbbox.currentText() == 'Category':
                        # print(f'Row: {row_num}, Data: {row}')
                        if str(row[1]) == 'None':
                            value = ''
                        else:
                            value = str(row[1])
                        month_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(value))
                        month_table.item(row_num, 0).setFont(data_font)
                        if row[0] == 'Total':
                            month_table.item(row_num, 0).setFont(total_font)
                    elif self.ui.grouping_cmbbox.currentText() == 'Type':
                        if row[0] != 'Total':
                            if str(row[2]) == 'None':
                                value = ''
                            else:
                                value = str(row[2])
                            month_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(value))
                            month_table.item(row_num, 0).setFont(data_font)
                            # if col_num == 0:
                            #     month_table.setVerticalHeaderItem(row_num, QtWidgets.QTableWidgetItem(str(row[1])))
                        else:
                            month_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(row[1])))
                            month_table.item(row_num, 0).setFont(total_font)
                            # if col_num == 0:
                            #     month_table.setVerticalHeaderItem(row_num, QtWidgets.QTableWidgetItem(''))

                month_table.horizontalHeader().setVisible(False)
                month_table.verticalHeader().setVisible(False)
                # month_table.setMaximumWidth(month_table.columnWidth(0))
                self.ui.report_table.setColumnWidth(col_num, month_table.columnWidth(0) * month_table.columnCount())
                print(f'ColumnCount {month_table.columnCount()}')
                self.ui.report_table.setCellWidget(0, col_num, month_table)
                self.ui.report_table.setSpan(0, col_num, row_count, 1)
                month_table.horizontalScrollBar().setVisible(False)
                month_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                month_table.setStyleSheet('QTableWidget {border: 0 px;}')
            if self.ui.grouping_cmbbox.currentText() == 'Type':
                self.ui.report_table.insertColumn(0)
                self.ui.report_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Category'))
                self.ui.report_table.horizontalHeaderItem(0).setFont(header_font)
                for row_num, row in enumerate(report_lists[0]):
                    if row[0] == 'Total':
                        pass
                    else:
                        self.ui.report_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row[1]))
                        header_font.setPointSize(10)
                        self.ui.report_table.item(row_num, 0).setFont(header_font)
            # self.ui.report_table.setRowHeight(0, self.ui.report_table.rowHeight(0) + 5)
        elif self.ui.report_type_cmbbox.currentText() == 'Expenses':
            if self.ui.grouping_cmbbox.currentText() == 'Category':
                report_lists = backend.make_several_months_expenses_report('Expense_category_name',
                                                                           months_list_numeric, 'Expense_category_name',
                                                                           finances.db)
            elif self.ui.grouping_cmbbox.currentText() == 'Subcategory':
                report_lists = backend.make_several_months_expenses_report(
                    'Expense_subcategory_name, Expense_category_name', months_list_numeric, 'Expense_subcategory_name',
                    finances.db)
            elif self.ui.grouping_cmbbox.currentText() == 'Product/service':
                report_lists = backend.make_several_months_expenses_report(
                    'Product_service_name, Expense_subcategory_name, Expense_category_name', months_list_numeric,
                    'Product_service_name', finances.db)
            else:
                return
            print(f'Report lists: {report_lists}')
            header_font = QtGui.QFont()
            header_font.setFamily("Candara")
            header_font.setPointSize(12)
            header_font.setBold(True)
            self.ui.report_table.clear()
            self.ui.report_table.setColumnCount(len(report_lists))
            # print(report_lists)
            row_count = len(report_lists[0])
            self.ui.report_table.setRowCount(row_count)
            print('Setting vertical headers')
            for row_num, data in enumerate(report_lists[0]):
                print(f'Row num: {row_num}, Data: {data}')
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                self.ui.report_table.setVerticalHeaderItem(row_num, item)
                # print(data)
                self.ui.report_table.verticalHeaderItem(row_num).setText(data[0])
            self.ui.report_table.insertRow(0)
            self.ui.report_table.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(''))
            print('Filling table')
            for col_num, zipped_data in enumerate(zip(months_list_numeric, report_lists)):
                print('Making headers')
                print(f'Col num: {col_num}, Zipped_date: {zipped_data}')
                # print(f'Zipped data: {zipped_data}')
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                self.ui.report_table.setHorizontalHeaderItem(col_num, item)
                self.ui.report_table.horizontalHeaderItem(col_num).setText(
                    f'{backend.turn_numeric_month_to_str(zipped_data[0][0])}, {zipped_data[0][1]}')
                month_table = QtWidgets.QTableWidget()
                month_table.setColumnCount(3)
                for column_num, header in enumerate(['Quantity', 'Total amount', 'Average price']):
                    item = QtWidgets.QTableWidgetItem()
                    item.setFont(header_font)
                    month_table.setHorizontalHeaderItem(column_num, item)
                    month_table.horizontalHeaderItem(column_num).setText(header)
                month_table.setRowCount(len(zipped_data[1]))
                data_font = QtGui.QFont()
                data_font.setFamily("Candara")
                data_font.setPointSize(10)
                data_font.setBold(False)
                total_font = QtGui.QFont()
                total_font.isCopyOf(data_font)
                total_font.setBold(True)
                print('Inserting values')
                for row_num, row in enumerate(zipped_data[1]):
                    print(f'Row num: {row_num}, Row: {row}')
                    if self.ui.grouping_cmbbox.currentText() == 'Category':
                        # print(f'Row: {row_num}, Data: {row}')
                        for column in range(3):
                            if row[0] == 'Total' and column == 2:
                                continue
                            if str(row[column+1]) == 'None':
                                value = ''
                            else:
                                value = str(row[column+1])
                            month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(value))
                            month_table.item(row_num, column).setFont(data_font)
                            if row[0] == 'Total':
                                month_table.item(row_num, column).setFont(total_font)
                    elif self.ui.grouping_cmbbox.currentText() == 'Subcategory':
                        for column in range(3):
                            if row[0] == 'Total':
                                if column == 0:
                                    month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(str(row[1])))
                                    month_table.item(row_num, column).setFont(total_font)
                                elif column == 1:
                                    month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(str(row[2])))
                                    month_table.item(row_num, column).setFont(total_font)
                                else:
                                    continue
                            else:
                                if str(row[column+2]) == 'None':
                                    value = ''
                                else:
                                    value = str(row[column+2])
                                month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(value))
                                month_table.item(row_num, column).setFont(data_font)
                    elif self.ui.grouping_cmbbox.currentText() == 'Product/service':
                        for column in range(3):
                            if row[0] == 'Total':
                                if column == 0:
                                    month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(str(row[1])))
                                    month_table.item(row_num, column).setFont(total_font)
                                elif column == 1:
                                    month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(str(row[2])))
                                    month_table.item(row_num, column).setFont(total_font)
                                else:
                                    continue
                            else:
                                if str(row[column + 3]) == 'None':
                                    value = ''
                                else:
                                    value = str(row[column + 3])
                                month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(value))
                                month_table.item(row_num, column).setFont(data_font)

                month_table.verticalHeader().setVisible(False)
                # month_table.setMaximumWidth(month_table.columnWidth(0))
                self.ui.report_table.setColumnWidth(col_num, month_table.columnWidth(0)*month_table.columnCount())
                print(f'ColumnCount {month_table.columnCount()}')
                self.ui.report_table.setCellWidget(0, col_num, month_table)
                self.ui.report_table.setSpan(0, col_num, row_count+1, 1)
                month_table.horizontalScrollBar().setVisible(False)
                month_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                month_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                month_table.setStyleSheet('QTableWidget {border: 0 px;}')
            print('Inserting categories column')
            if self.ui.grouping_cmbbox.currentText() == 'Subcategory':
                self.ui.report_table.insertColumn(0)
                self.ui.report_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Category'))
                self.ui.report_table.horizontalHeaderItem(0).setFont(header_font)
                for row_num, row in enumerate(['']+report_lists[0]):
                    if row == '':
                        self.ui.report_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row))
                    elif row[0] == 'Total':
                        pass
                    else:
                        self.ui.report_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row[1]))
                        header_font.setPointSize(10)
                        self.ui.report_table.item(row_num, 0).setFont(header_font)
            elif self.ui.grouping_cmbbox.currentText() == 'Product/service':
                for column in ('Category', 'Subcategory'):
                    self.ui.report_table.insertColumn(0)
                    self.ui.report_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem(column))
                    self.ui.report_table.horizontalHeaderItem(0).setFont(header_font)
                for row_num, row in enumerate(['']+report_lists[0]):
                    if row == '':
                        for column in range(2):
                            self.ui.report_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(row))
                    elif row[0] == 'Total':
                        pass
                    else:
                        for column in range(2):
                            self.ui.report_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(row[column+1]))
                            header_font.setPointSize(10)
                            self.ui.report_table.item(row_num, column).setFont(header_font)
        elif self.ui.report_type_cmbbox.currentText() == 'Savings':
            report_lists = backend.make_several_months_savings_report(months_list_numeric, finances.db)
            print(f'Report lists: {report_lists}')
            header_font = QtGui.QFont()
            header_font.setFamily("Candara")
            header_font.setPointSize(12)
            header_font.setBold(True)
            self.ui.report_table.clear()
            self.ui.report_table.setColumnCount(len(report_lists)-1)
            print(len(report_lists))
            row_count = len(report_lists[0]) + 1
            self.ui.report_table.setRowCount(row_count)
            print('Setting vertical headers')
            for row_num, row_name in enumerate(['Month start savings', 'Total earnings', 'Total expenses', 'Growth',
                                                'Total']):
                print(row_num)
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                self.ui.report_table.setVerticalHeaderItem(row_num, item)
                # print(data)
                self.ui.report_table.verticalHeaderItem(row_num).setText(row_name)
            print('Filling table')
            for col_num, zipped_data in enumerate(zip(months_list_numeric, report_lists)):
                print('Making headers')
                print(f'Col num: {col_num}, Zipped_date: {zipped_data}')
                # print(f'Zipped data: {zipped_data}')
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                self.ui.report_table.setHorizontalHeaderItem(col_num, item)
                self.ui.report_table.horizontalHeaderItem(col_num).setText(
                    f'{backend.turn_numeric_month_to_str(zipped_data[0][0])}, {zipped_data[0][1]}')
                month_table = QtWidgets.QTableWidget()
                month_table.setRowCount(row_count)
                month_table.setColumnCount(1)
                data_font = QtGui.QFont()
                data_font.setFamily("Candara")
                data_font.setPointSize(10)
                data_font.setBold(False)
                total_font = QtGui.QFont()
                total_font.isCopyOf(data_font)
                total_font.setBold(True)
                print('Inserting values')
                for row_num, row in enumerate(zipped_data[1]):
                    print(f'Row num: {row_num}, Row: {row}')
                    # print(f'Row: {row_num}, Data: {row}')
                    if str(row) == 'None':
                        value = ''
                    else:
                        value = str(row)
                        print(month_table.rowCount())
                    month_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(value))
                    month_table.item(row_num, 0).setFont(data_font)
                if col_num == len(report_lists)-2:
                    value = str(report_lists[-1][1])
                    month_table.setItem(len(report_lists[0]), 0, QtWidgets.QTableWidgetItem(value))
                month_table.verticalHeader().setVisible(False)
                month_table.horizontalHeader().setVisible(False)
                # month_table.setMaximumWidth(month_table.columnWidth(0))
                self.ui.report_table.setColumnWidth(col_num, month_table.columnWidth(0) * month_table.columnCount())
                print(f'ColumnCount {month_table.columnCount()}')
                self.ui.report_table.setCellWidget(0, col_num, month_table)
                self.ui.report_table.setSpan(0, col_num, row_count + 1, 1)
                month_table.horizontalScrollBar().setVisible(False)
                month_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                month_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                month_table.setStyleSheet('QTableWidget {border: 0 px;}')


def new_window_btn_clicked(window, new_window_class):
    window.new_window = new_window_class(window)
    window.new_window.show()
    window.close()


def return_btn_clicked(window, parent_window):
    parent_window.show()
    window.close()


def update_cmbbox(cmbbox, category_type: str, update_func, db, parent_id=None):
    cmbbox.clear()
    try:
        cmbbox.addItems([''] + update_func(db) + [f'Add new {category_type}'])
    except TypeError:
        cmbbox.addItems([''] + update_func(parent_id, db) + [f'Add new {category_type}'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    finances = MainWindow()
    finances.show()
    sys.exit(app.exec())
