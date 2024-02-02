import sqlite3
import pandas
import datetime


def create_expense_categories_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Expense_categories(
    Expense_category VARCHAR(256) PRIMARY KEY
    )
"""
    execute_query_without_returns(query, db)


def add_expense_category(expense_category, db):
    query = f"""INSERT INTO Expense_categories(Expense_category)
VALUES('{expense_category}')"""
    execute_query_without_returns(query, db)


def get_all_expense_categories(db):
    query = '''SELECT Expense_category FROM Expense_categories'''
    results = execute_select_query(query, db)
    return results


def create_expense_subcategories_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Expense_subcategories(
    Expense_subcategory VARCHAR(256) PRIMARY KEY,
    Expense_category VARCHAR(256) NOT NULL,
    FOREIGN KEY (Expense_category) REFERENCES Expense_categories(Expense_category)
    )
"""
    execute_query_without_returns(query, db)


def add_expense_subcategory(expense_subcategory, expense_category, db):
    query = f"""INSERT INTO Expense_subcategories(Expense_subcategory, Expense_category)
VALUES('{expense_subcategory}', '{expense_category}')"""
    execute_query_without_returns(query, db)


def get_all_expense_subcategories(expense_category, db):
    query = f"""SELECT Expense_subcategory FROM Expense_subcategories
    WHERE Expense_category = '{expense_category}'
    """
    results = execute_select_query(query, db)
    return results


def create_product_service_table(db):
    query = """CREATE TABLE IF NOT EXISTS Products_services(
    Product_service VARCHAR(256) PRIMARY KEY,
    Expense_category VARCHAR(256) NOT NULL,
    Expense_subcategory VARCHAR(256),
    FOREIGN KEY(Expense_category) REFERENCES Expense_categories(Expense_category),
    FOREIGN KEY(Expense_subcategory) REFERENCES Expense_subcategories(Expense_subcategory)
    )
    """
    execute_query_without_returns(query, db)


def add_product_service(product_service, expense_category, expense_subcategory, db):
    query = f"""INSERT INTO Products_services(Product_service, Expense_category, Expense_subcategory)
    VALUES('{product_service}', '{expense_category}', '{expense_subcategory}')"""
    execute_query_without_returns(query, db)


def get_all_products_services(expense_category, expense_subcategory, db):
    query = f"""SELECT Product_service FROM Products_services
    WHERE Expense_category = '{expense_category}' AND Expense_subcategory = '{expense_subcategory}'
    """
    results = execute_select_query(query, db)
    return results


def create_expenses_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Expenses (
Expense_ID INTEGER PRIMARY KEY,
Product_service VARCHAR(256) NOT NULL,
Expense_category VARCHAR(256) NOT NULL,
Expense_subcategory VARCHAR(256),
Year INTEGER NOT NULL,
Month VARCHAR(30) NOT NULL,
Quantity INTEGER NOT NULL,
Total_amount INTEGER NOT NULL,
FOREIGN KEY (Expense_category) REFERENCES Expense_categories(Expense_category),
FOREIGN KEY (Expense_subcategory) REFERENCES Expense_subcategories(Expense_subcategory),
FOREIGN KEY (Product_service) REFERENCES Products_services(Product_service)
)
"""
    execute_query_without_returns(query, db)


def add_expenses(product_service, expense_category, expense_subcategory, month, year, quantity, total_amount, db):
    query = f"""INSERT INTO 
    Expenses(Product_service, Expense_category, Expense_subcategory, Year, Month, Quantity, Total_amount)
    VALUES('{product_service}', '{expense_category}', '{expense_subcategory}',
{year}, '{month}', {quantity}, {total_amount})
"""
    execute_query_without_returns(query, db)


def create_earning_types_table(db):
    query = """CREATE TABLE IF NOT EXISTS Earning_types(
    Earning_type VARCHAR(256) PRIMARY KEY
    )
    """
    execute_query_without_returns(query, db)


def add_earning_type(earning_type, db):
    query = f"""INSERT INTO Earning_types(Earning_type)
    VALUES('{earning_type}')
    """
    execute_query_without_returns(query, db)
    
    
def get_all_earning_types(db):
    query = """SELECT Earning_type FROM Earning_types
    """
    results = execute_select_query(query, db)
    return results


def create_earnings_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Earnings (
    Earning_ID INTEGER PRIMARY KEY,
    Earning_type VARCHAR(256) NOT NULL,
    Year INTEGER NOT NULL,
    Month VARCHAR(30) NOT NULL,
    Amount INTEGER NOT NULL,
    FOREIGN KEY (Earning_type) REFERENCES Earning_types(Earning_type)
    )
    """
    execute_query_without_returns(query, db)


def add_earnings(earning_type, month, year, amount, db):
    query = f"""INSERT INTO Earnings(Earning_type, Year, Month, Amount)
        VALUES('{earning_type}', '{year}', '{month}', {amount})
    """
    execute_query_without_returns(query, db)


def change_record():
    pass


def make_query(column, value, table, db):
    query = f"""SELECT * FROM {table}
    WHERE {column} = {value}
    """
    execute_query_without_returns(query, db)


def calculate_average():
    pass


def execute_query_without_returns(query, db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()


def execute_select_query(query, db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        results = [atuple[0] for atuple in cursor.fetchall()]
    return results


def get_current_month():
    return datetime.date.today().strftime('%B')


def get_current_year():
    return datetime.date.today().year


if __name__ == "__main__":
    database = 'finances_db.db'
    create_expense_categories_table(database)
    # create_subcategories_table(database)
    # create_month_earnings_table('Feb', 2024, database)
    # create_month_expenses_table('Feb', 2024, database)
    # add_expense_category('Food', database)
    # add_subcategory('Rent', 'Apartment', database)
    # add_subcategory('Communal services', 'Apartment', database)
    # add_earnings('Feb', 2024, 'Stipend', 2204, database)
    # add_expenses('Feb', 2024, 'Apartment', 'Rent', 20000, 1, database)
    # add_earnings('Feb', 2024, 'Stipend', 2024, database)
    # add_expenses('Feb', 2024, 'Apartment', 'Communal services', 4000, 1, database)
    print(type(get_all_expense_categories(database)))
    print(get_all_expense_categories(database))
    # with sqlite3.connect(database) as connection:
    #     cursor = connection.cursor()
    #     query = """SELECT SUM(Quantity) FROM(
    #     SELECT * FROM 'Feb, 2024 expenses'
    #     WHERE Category='Apartment')"""
    #     cursor.execute(query)
    #     results = cursor.fetchall()
    #     for result in results:
    #         print(result[0])

    print(f'{get_current_month()}, {get_current_year()}')
