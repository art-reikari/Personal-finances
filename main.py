import sys
import backend
import PyQt6
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
        self.month = backend.get_current_month()
        self.ui.month_year_lbl.setText(f'{self.ui.month_year_lbl.text()} {self.month}, {self.year}')

        backend.create_expense_categories_table(self.db)
        backend.create_expense_subcategories_table(self.db)
        backend.create_product_service_table(self.db)
        backend.create_expenses_table(self.db)
        backend.create_earning_types_table(self.db)
        backend.create_earnings_table(self.db)

        self.ui.add_earnings_expenses_btn.clicked.connect(
            lambda: new_window_btn_clicked(self, AddExpensesEarningsWindow))
        self.ui.show_reports_btn.clicked.connect(lambda: new_window_btn_clicked(self, ShowReportsWindow))
        # self.ui.settings_btn.clicked.connect(self.settings_btn_clicked)

    def btn_clicked(self):
        window = ShowReportsWindow(self)
        window.show()
        self.close()


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
            self.ui.category_lbl.setText('Type')
            self.ui.category_cmbbox.show()
            self.ui.total_lbl.show()
            self.ui.total_inpt.show()
            self.ui.subcategory_lbl.hide()
            self.ui.subcategory_cmbbox.hide()
            self.ui.subcategory_cmbbox.setDisabled(True)
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
            update_cmbbox(self.ui.category_cmbbox, 'type', backend.get_all_earning_types, finances.db)
        elif self.ui.choose_type_cmbbox.currentText() == 'Expenses':
            self.ui.category_lbl.show()
            self.ui.category_lbl.setText('Category')
            self.ui.category_cmbbox.show()
            self.ui.total_lbl.show()
            self.ui.total_inpt.show()
            self.ui.subcategory_lbl.show()
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
            if self.ui.category_cmbbox.currentText() == 'Add new type':
                self.ui.new_category_inpt.show()
            else:
                self.ui.new_category_inpt.hide()
        else:
            if self.ui.category_cmbbox.currentText() == 'Add new category':
                self.ui.new_category_inpt.show()
                update_cmbbox(self.ui.subcategory_cmbbox, 'subcategory',
                              backend.get_all_expense_subcategories, finances.db, None)
            else:
                self.ui.new_category_inpt.hide()
                update_cmbbox(self.ui.subcategory_cmbbox, 'subcategory',
                              backend.get_all_expense_subcategories, finances.db, self.ui.category_cmbbox.currentText())

    def subcategory_changed(self):
        if self.ui.subcategory_cmbbox.currentText() == 'Add new subcategory':
            self.ui.new_subcategory_inpt.show()
            update_cmbbox(self.ui.product_service_cmbbox, 'product or service', backend.get_all_products_services,
                          finances.db, None)
        else:
            self.ui.new_subcategory_inpt.hide()
            update_cmbbox(self.ui.product_service_cmbbox, 'product or service', backend.get_all_products_services,
                          finances.db, self.ui.category_cmbbox.currentText(), self.ui.subcategory_cmbbox.currentText())

    def product_service_changed(self):
        if self.ui.product_service_cmbbox.currentText() == 'Add new product or service':
            self.ui.new_product_service_inpt.show()
        else:
            self.ui.new_product_service_inpt.hide()

    def add_btn_clicked(self):
        if self.ui.choose_type_cmbbox.currentText() == 'Earnings':
            if self.ui.new_category_inpt.isVisible():
                earning_type = self.ui.new_category_inpt.text()
            else:
                earning_type = self.ui.category_cmbbox.currentText()
            amount = float(self.ui.total_inpt.text())
            backend.add_earnings(earning_type, finances.month, finances.year, amount, finances.db)
            if self.ui.category_cmbbox.currentText() == 'Add new type':
                backend.add_earning_type(earning_type, finances.db)
                update_cmbbox(self.ui.category_cmbbox, 'type', backend.get_all_earning_types, finances.db)
        else:
            print('We are inside first if!')
            if self.ui.new_category_inpt.isVisible():
                category = self.ui.new_category_inpt.text()
                backend.add_expense_category(category, finances.db)
            else:
                category = self.ui.category_cmbbox.currentText()
            if self.ui.new_subcategory_inpt.isVisible():
                print('We change our subcategory!')
                subcategory = self.ui.new_subcategory_inpt.text()
                backend.add_expense_subcategory(subcategory, category, finances.db)
            else:
                subcategory = self.ui.subcategory_cmbbox.currentText()
            if self.ui.new_product_service_inpt.isVisible():
                print('We change our product_service!')
                product_service = self.ui.new_product_service_inpt.text()
                backend.add_product_service(product_service, category, subcategory, finances.db)
            else:
                product_service = self.ui.product_service_cmbbox.currentText()
            qty = float(self.ui.qty_inpt.text())
            total = float(self.ui.total_inpt.text())
            backend.add_expenses(product_service, category, subcategory, finances.month, finances.year,
                                 qty, total, finances.db)
            if self.ui.category_cmbbox.currentText() == 'Add new category':
                update_cmbbox(self.ui.category_cmbbox, 'category', backend.get_all_expense_categories, finances.db)
            if self.ui.subcategory_cmbbox.currentText() == 'Add new subcategory':
                print('We update our subcategories db!')
                update_cmbbox(
                    self.ui.subcategory_cmbbox, 'subcategory', backend.get_all_expense_subcategories, finances.db,
                    category)
            if self.ui.product_service_cmbbox.currentText() == 'Add new product or service':
                update_cmbbox(self.ui.product_service_cmbbox, 'product or service', backend.get_all_products_services,
                              finances.db, category, subcategory)
        for element in self.ui.info_frm.children():
            if isinstance(element, QLineEdit):
                element.clear()
            elif isinstance(element, QComboBox):
                element.setCurrentIndex(0)
            else:
                pass


class ShowReportsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = show_reports_ui.Ui_Form()
        self.ui.setupUi(self)

        # self.ui.return_btn.clicked.connect(lambda: return_btn_clicked(self, parent))


def new_window_btn_clicked(window, new_window_class):
    window.new_window = new_window_class(window)
    window.new_window.show()
    window.close()


def return_btn_clicked(window, parent_window):
    parent_window.show()
    window.close()


def update_cmbbox(cmbbox, category_type: str, update_func, db, category=None, subcategory=None):
    cmbbox.clear()
    try:
        cmbbox.addItems([''] + update_func(db) + [f'Add new {category_type}'])
    except TypeError:
        try:
            cmbbox.addItems([''] + update_func(category, db) + [f'Add new {category_type}'])
        except TypeError:
            print(category)
            print(subcategory)
            cmbbox.addItems([''] + update_func(category, subcategory, db) + [f'Add new {category_type}'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    finances = MainWindow()
    finances.show()
    sys.exit(app.exec())
