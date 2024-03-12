import sys
import backend
import PyQt6
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QComboBox
from ui import main_window_ui
from ui import add_earnings_or_expenses_ui
from ui import show_reports_ui


class MainWindow(QMainWindow):
    """
    Main window of the programme. It shows current month and year, current savings and projected savings for this month.
    It has the following buttons to open additional windows: Add earnings or expenses, Reports, Settings.
    At the very first start of the programme, it will prompt user to input his/her starting savings amount.

    Attributes:
        ui : Ui_MainWindow
            stores ui info loaded from prepared ui outline file
        new_window : initially None; child windows class when calling function of opening new windows
            is used for the function of opening new Widget windows and preserving parent-child relations
            between the main and child windows
        db : str
            stores database file name with file format
        year : int
            stores current year
        month : int
            stores current month
        savings : float
            stores current savings


    Methods:
         update_savings_info():
            updates savings attribute according to newly added earnings or expenses
         input_current_savings_btn_clicked():
            adds starting savings amount to the database when inputting it at the first start of the programme
    """
    def __init__(self):
        super().__init__()
        self.ui = main_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        print(type(self.ui))
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

    def update_savings_info(self) -> None:
        self.savings = str(backend.get_month_savings(self.db, self.month, self.year))
        self.ui.savings_lbl.setText('Savings: ' + self.savings)

    def input_current_savings_btn_clicked(self) -> None:
        """
        Inserts the first record in Savings table,
        when the respective button is clicked at the first start of the programme.
        :return: None
        """
        backend.add_savings(self.db, self.month, self.year, float(self.ui.current_savings_inpt.text()))
        self.ui.input_current_savings_frm.hide()
        self.ui.main_frm.show()
        self.update_savings_info()


class AddExpensesEarningsWindow(QWidget):
    """
    Window that allows to add new expenses or earnings to the database.

    Attributes:
        ui: Ui_MainWindow
            stores ui info loaded from prepared ui outline file
    Methods:
        type_changed():
            changes visible input fields when the type of new record is changes (Earnings or Expenses or None)
        category_changed():
            changes contents of subcategory combobox when category is changed. If new category input is selected,
            shows input field for the name of this category. Otherwise, hides this field.
        subcategory_changed():
            changes product/service combobox when subcategory is changed. If new subcategory input is selected,
            shows input filed for the name of this subcategory. Otherwise, hides this field.
        product_service_changed():
            If new product/service input is selected, shows input field for the name of this product/service.
            Otherwise, hides the field.
        add_btn_clicked():
            When Add button is clicked, inserts new record in Expenses or Earnings table in the database and
            updates current savings attribute of the Main window.
            If new category is inputted, updates the category combobox.
    """
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

    def type_changed(self) -> None:
        """
        Changes visible input fields when the type of new record is changes (Earnings or Expenses or None)
        :return: None
        """
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

    def category_changed(self) -> None:
        """
        Changes contents of subcategory combobox when category is changed. If new category input is selected,
        shows input field for the name of this category. Otherwise, hides this field.
        :return: None
        """
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

    def subcategory_changed(self) -> None:
        """
        Changes product/service combobox when subcategory is changed. If new subcategory input is selected,
        shows input filed for the name of this subcategory. Otherwise, hides this field.
        :return: None
        """
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

    def product_service_changed(self) -> None:
        """
        If new product/service input is selected, shows input field for the name of this product/service.
        Otherwise, hides the field.
        :return: None
        """
        if self.ui.product_service_cmbbox.currentText() == 'Add new product or service':
            self.ui.new_product_service_inpt.show()
        else:
            self.ui.new_product_service_inpt.hide()

    def add_btn_clicked(self) -> None:
        """
        When Add button is clicked, inserts new record in Expenses or Earnings table in the database and
        updates current savings attribute of the Main window.
        If new category is inputted, updates the category combobox.
        :return: None
        """
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
            if self.ui.new_category_inpt.isVisible():
                category = self.ui.new_category_inpt.text()
                backend.add_expense_category(category, finances.db)
            else:
                category = self.ui.category_cmbbox.currentText()
            if self.ui.new_subcategory_inpt.isVisible():
                subcategory = self.ui.new_subcategory_inpt.text()
                backend.add_expense_subcategory(subcategory, category, finances.db)
            else:
                subcategory = self.ui.subcategory_cmbbox.currentText()
            if self.ui.new_product_service_inpt.isVisible():
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
    """
    Window that allows you to make reports on expenses, earnings and savings across chosen months.

    Attributes:
        ui: Ui_MainWindow
            stores ui info loaded from prepared ui outline file.
    Methods:
        report_type_changed():
        grouping_changed():
        load_report():


    """
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

    def report_type_changed(self) -> None:
        """
        Changes contents of Grouping combobox when report type is changes (Earnings, Expenses or Savings)
        :return: None
        """
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

    def grouping_changed(self) -> None:
        """
        Enables Load report button when valid grouping is selected, disables the button otherwise.
        :return: None
        """
        if self.ui.grouping_cmbbox.currentText() != '':
            self.ui.load_report_btn.setEnabled(True)
        else:
            self.ui.load_report_btn.setDisabled(True)

    def load_report(self) -> None:
        """
        Makes report according to the selected type, grouping and time period and shows it in the table in the windows
        :return: None
        """
        header_font = self.make_font('Candara', 12, True)
        data_font = self.make_font('Candara', 10, False)
        total_font = self.make_font('Candara', 10, True)
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
            row_names = list(map(lambda x: x[0], report_lists[0]))
            row_count = len(report_lists[0])
            self.make_report_table_row_headers(header_font, len(report_lists), row_count, row_names)
            for col_num, zipped_data in enumerate(zip(months_list_numeric, report_lists)):
                # print(f'Zipped data: {zipped_data}')
                month_table = self.structure_month_table(header_font, col_num, zipped_data, row_count, 1, [])
                for row_num, row in enumerate(zipped_data[1]):
                    if self.ui.grouping_cmbbox.currentText() == 'Category':
                        # print(f'Row: {row_num}, Data: {row}')
                        self.insert_month_table_values(1, 1, row, row_num, month_table, total_font, data_font)
                    elif self.ui.grouping_cmbbox.currentText() == 'Type':
                        self.insert_month_table_values(1, 2, row, row_num, month_table, total_font, data_font)

                self.set_month_table_appearance(month_table, False, False, col_num, row_count)
            if self.ui.grouping_cmbbox.currentText() == 'Type':
                self.insert_categories_columns(('Category',), header_font, report_lists[0], 1)
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
            row_names = list(map(lambda x: x[0], report_lists[0]))
            row_count = len(report_lists[0])
            self.make_report_table_row_headers(header_font, len(report_lists), row_count, row_names)
            self.ui.report_table.insertRow(0)
            self.ui.report_table.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(''))
            print('Filling table')
            for col_num, zipped_data in enumerate(zip(months_list_numeric, report_lists)):
                print('Making headers')
                print(f'Col num: {col_num}, Zipped_date: {zipped_data}')
                month_table = self.structure_month_table(header_font, col_num, zipped_data, row_count, 3,
                                                         ['Quantity', 'Total amount', 'Average price'])
                print('Inserting values')
                for row_num, row in enumerate(zipped_data[1]):
                    print(f'Row num: {row_num}, Row: {row}')
                    if self.ui.grouping_cmbbox.currentText() == 'Category':
                        self.insert_month_table_values(3, 1, row, row_num, month_table, total_font, data_font)
                    elif self.ui.grouping_cmbbox.currentText() == 'Subcategory':
                        self.insert_month_table_values(3, 2, row, row_num, month_table, total_font, data_font)
                    elif self.ui.grouping_cmbbox.currentText() == 'Product/service':
                        self.insert_month_table_values(3, 3, row, row_num, month_table, total_font, data_font)

                self.set_month_table_appearance(month_table, True, False, col_num, row_count+1)
            print('Inserting categories column')
            if self.ui.grouping_cmbbox.currentText() == 'Subcategory':
                self.insert_categories_columns(('Category',), header_font, ['']+report_lists[0], 1)
            elif self.ui.grouping_cmbbox.currentText() == 'Product/service':
                self.insert_categories_columns(('Category', 'Subcategory'), header_font, [''] + report_lists[0], 2)
        elif self.ui.report_type_cmbbox.currentText() == 'Savings':
            report_lists = backend.make_several_months_savings_report(months_list_numeric, finances.db)
            print(f'Report lists: {report_lists}')
            row_count = len(report_lists[0]) + 1
            self.make_report_table_row_headers(header_font, len(report_lists)-1, row_count,
                                               ('Month start savings', 'Total earnings',
                                                'Total expenses', 'Growth', 'Total'))
            print('Filling table')
            for col_num, zipped_data in enumerate(zip(months_list_numeric, report_lists)):
                print('Making headers')
                print(f'Col num: {col_num}, Zipped_date: {zipped_data}')
                month_table = self.structure_month_table(header_font, col_num, zipped_data, row_count, 1, [])
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
                if col_num == len(report_lists) - 2:
                    value = str(report_lists[-1][1])
                    month_table.setItem(len(report_lists[0]), 0, QtWidgets.QTableWidgetItem(value))

                self.set_month_table_appearance(month_table, False, False, col_num, row_count+1)

    def make_report_table_row_headers(self, header_font, column_count: int,
                                      row_count: int, row_names: list | tuple) -> None:
        """
        Makes headers for rows in the report table according to categories, subcategories,
        product/services or earning types selected.
        :param header_font: font which is used for row headers
        :param column_count: number of columns in the report table (virtually, number of months)
        :param row_count: number of rows in the report table
        :param row_names: headers for rows
        :return: None
        """
        self.ui.report_table.clear()
        self.ui.report_table.setColumnCount(column_count)
        self.ui.report_table.setRowCount(row_count)
        print('Setting vertical headers')
        for row_num, row_name in enumerate(row_names):
            print(f'Row num: {row_num}, Data: {row_name}')
            item = QtWidgets.QTableWidgetItem()
            item.setFont(header_font)
            self.ui.report_table.setVerticalHeaderItem(row_num, item)
            # print(data)
            self.ui.report_table.verticalHeaderItem(row_num).setText(row_name)

    def structure_month_table(self, header_font: PyQt6.QtGui.QFont, col_num: int, zipped_data: list | tuple,
                              row_count, column_count: int, headers: list) -> PyQt6.QtWidgets.QTableWidget:
        """
        Adds a header for a column in the report table and structures the month table for this column.
        Adds its own headers, defines number of rows and columns.
        :param header_font: font that is used for headers
        :param col_num: number of the column in the report table in which this month table is inserted
        :param zipped_data: zipped list containing report records and respective months
        :param row_count: number of rows in the month table
        :param column_count: number of columns in the month table
        :param headers: headers of the month table columns. Empty list if no headers are needed.
        :return: None
        """
        item = QtWidgets.QTableWidgetItem()
        item.setFont(header_font)
        self.ui.report_table.setHorizontalHeaderItem(col_num, item)
        self.ui.report_table.horizontalHeaderItem(col_num).setText(
            f'{backend.turn_numeric_month_to_str(zipped_data[0][0])}, {zipped_data[0][1]}')
        month_table = QtWidgets.QTableWidget()
        month_table.setColumnCount(column_count)
        if headers:
            for column_num, header in enumerate(headers):
                item = QtWidgets.QTableWidgetItem()
                item.setFont(header_font)
                month_table.setHorizontalHeaderItem(column_num, item)
                month_table.horizontalHeaderItem(column_num).setText(header)
        # month_table.setRowCount(len(zipped_data[1]))
        month_table.setRowCount(row_count)
        return month_table

    @staticmethod
    def insert_month_table_values(column_count: int, data_index: int, row: list | tuple, row_num: int,
                                  month_table: PyQt6.QtWidgets.QTableWidget, total_font: PyQt6.QtGui.QFont,
                                  data_font: PyQt6.QtGui.QFont) -> None:
        """
        Inserts values in the Month table column
        :param column_count: number of columns in the Month table
        :param data_index: starting index of the first data value in the row record
        :param row: current row record from the database
        :param row_num: current row number in the Report table
        :param month_table: Month table object
        :param total_font: font that is used for total quantities
        :param data_font: font that is used for usual data
        :return: None
        """
        for column in range(column_count):
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
                if str(row[column + data_index]) == 'None':
                    value = ''
                else:
                    value = str(row[column + data_index])
                month_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(value))
                month_table.item(row_num, column).setFont(data_font)

    def set_month_table_appearance(self, month_table: PyQt6.QtWidgets.QTableWidget, horizontal_header_visibility: bool,
                                   vertical_header_visibility: bool, col_num: int, row_count: int) -> None:
        """
        Adjusts Month table and report table appearance by changing columns width,
        visibility of headers and scroll bars.
        :param month_table: Month table object
        :param horizontal_header_visibility: boolean that defines if horizontal header should be visible
        :param vertical_header_visibility: boolean that defines if vertical header should be visible
        :param col_num: current Report table column number
        :param row_count: number of rows in the Report table
        :return: None
        """
        month_table.horizontalHeader().setVisible(horizontal_header_visibility)
        month_table.verticalHeader().setVisible(vertical_header_visibility)
        self.ui.report_table.setColumnWidth(col_num, month_table.columnWidth(0) * month_table.columnCount())
        print(f'ColumnCount {month_table.columnCount()}')
        self.ui.report_table.setCellWidget(0, col_num, month_table)
        self.ui.report_table.setSpan(0, col_num, row_count, 1)
        month_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        month_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        month_table.setStyleSheet('QTableWidget {border: 0 px;}')

    def insert_categories_columns(self, columns: list | tuple, header_font: PyQt6.QtGui.QFont, rows: list,
                                  column_count: int) -> None:
        """
        Inserts categories and subcategories columns in the report table if they are present in the report data.
        :param columns: names of columns to be inserted
        :param header_font: font that is used for headers
        :param rows: list of row records from the database
        :param column_count: number of columns to be inserted
        :return: None
        """
        for column in columns:
            self.ui.report_table.insertColumn(0)
            self.ui.report_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem(column))
            self.ui.report_table.horizontalHeaderItem(0).setFont(header_font)
        for row_num, row in enumerate(rows):
            if row == '':
                for column in range(column_count):
                    self.ui.report_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(row))
            elif row[0] == 'Total':
                continue
            else:
                for column in range(column_count):
                    self.ui.report_table.setItem(row_num, column, QtWidgets.QTableWidgetItem(row[column + 1]))
                    header_font.setPointSize(10)
                    self.ui.report_table.item(row_num, column).setFont(header_font)

    @staticmethod
    def make_font(family: str, size: int, bold: bool) -> PyQt6.QtGui.QFont:
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        return font


def new_window_btn_clicked(window, new_window_class):
    window.new_window = new_window_class(window)
    window.new_window.show()
    window.close()


def return_btn_clicked(window, parent_window):
    parent_window.show()
    window.close()


def update_cmbbox(cmbbox: PyQt6.QtWidgets.QComboBox, category_type: str, update_func: callable, db: str,
                  parent_name: None | str = None) -> None:
    """
    Updates contents of a combobox based on newly queried data from the table
    :param cmbbox: combobox to be updated
    :param category_type: string name of the category type (category, subcategory, product/service, type)
    :param update_func: function used to query new data from the database
    :param db: database file name with format
    :param parent_name: name of the parent element in the database structure
    :return: None
    """
    cmbbox.clear()
    try:
        cmbbox.addItems([''] + update_func(db) + [f'Add new {category_type}'])
    except TypeError:
        cmbbox.addItems([''] + update_func(parent_name, db) + [f'Add new {category_type}'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    finances = MainWindow()
    finances.show()
    sys.exit(app.exec())
