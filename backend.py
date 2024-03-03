import sqlite3
import datetime


def create_expense_categories_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Expense_categories(
    Expense_category_ID INTEGER PRIMARY KEY,
    Expense_category_name VARCHAR(256) NOT NULL
    )
"""
    execute_query_without_returns(query, db)


def add_expense_category(expense_category_name, db):
    query = f"""INSERT INTO Expense_categories (Expense_category_name)
VALUES(?)"""
    execute_query_without_returns(query, db, expense_category_name)


def get_all_expense_categories(db):
    query = '''SELECT Expense_category_name FROM Expense_categories'''
    return execute_select_query(query, db)


def create_expense_subcategories_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Expense_subcategories(
    Expense_subcategory_ID INTEGER PRIMARY KEY,
    Expense_subcategory_name VARCHAR(256) NOT NULL,
    Expense_category_ID INTEGER NOT NULL,
    FOREIGN KEY(Expense_category_ID) REFERENCES Expense_categories(Expense_category_ID)
    )
"""
    execute_query_without_returns(query, db)


def add_expense_subcategory(expense_subcategory_name, expense_category_name, db):
    query = f"""INSERT INTO Expense_subcategories(Expense_subcategory_name, Expense_category_ID)
VALUES(?, ?)"""
    query_id = f"""SELECT Expense_category_ID FROM Expense_categories
    WHERE Expense_category_name = ?"""
    expense_category_id = execute_select_query(query_id, db, expense_category_name)[0]
    execute_query_without_returns(query, db, expense_subcategory_name, expense_category_id)


def get_all_expense_subcategories_in_category(expense_category_name, db):
    if expense_category_name == '' or expense_category_name is None:
        return []
    query = f"""SELECT Expense_subcategory_name FROM Expense_subcategories
    WHERE Expense_category_ID = ?
    """
    query_id = f"""SELECT Expense_category_ID FROM Expense_categories
    WHERE Expense_category_name = ?"""
    expense_category_id = execute_select_query(query_id, db, expense_category_name)[0]
    return execute_select_query(query, db, expense_category_id)


def create_product_service_table(db):
    query = """CREATE TABLE IF NOT EXISTS Products_services(
    Product_service_ID INTEGER PRIMARY KEY,
    Product_service_name VARCHAR(256) NOT NULL,
    Expense_subcategory_ID INTEGER NOT NULL,
    FOREIGN KEY(Expense_subcategory_ID) REFERENCES Expense_subcategories(Expense_subcategory_ID)
    )
    """
    execute_query_without_returns(query, db)


def add_product_service(product_service_name, expense_subcategory_name, db):
    query = f"""INSERT INTO Products_services(Product_service_name, Expense_subcategory_ID)
    VALUES(?, ?)"""
    query_id = f"""SELECT Expense_subcategory_ID FROM Expense_subcategories
    WHERE Expense_subcategory_name = ?"""
    expense_subcategory_id = execute_select_query(query_id, db, expense_subcategory_name)[0]
    execute_query_without_returns(query, db, product_service_name, expense_subcategory_id)


def get_all_products_services_in_subcategory(expense_subcategory_name, db):
    if expense_subcategory_name == '' or expense_subcategory_name is None:
        return []
    query = f"""SELECT Product_service_name FROM Products_services
    WHERE Expense_subcategory_ID = ?
    """
    query_id = f"""SELECT Expense_subcategory_ID FROM Expense_subcategories
    WHERE Expense_subcategory_name = ?
    """
    expense_subcategory_id = execute_select_query(query_id, db, expense_subcategory_name)[0]
    return execute_select_query(query, db, expense_subcategory_id)


def create_expenses_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Expenses(
Expense_ID INTEGER PRIMARY KEY,
Product_service_ID INTEGER NOT NULL,
Month INTEGER NOT NULL,
Year INTEGER NOT NULL,
Quantity REAL NOT NULL,
Total_amount REAL NOT NULL,
FOREIGN KEY(Product_service_ID) REFERENCES Products_services(Product_service_ID)
)
"""
    execute_query_without_returns(query, db)


def add_expenses(product_service_name, month, year, quantity,
                 total_amount, db):
    insert_expense_query = f"""INSERT INTO 
    Expenses(Product_service_ID, Month, Year, Quantity, Total_amount)
    VALUES(?, ?, ?, ?, ?)
"""
    query_id = """SELECT Product_service_ID FROM Products_services
    WHERE Product_service_name = ?"""
    product_service_id = execute_select_query(query_id, db, product_service_name)[0]
    execute_query_without_returns(insert_expense_query, db, product_service_id, month, year, quantity, total_amount)

    current_total_expenses = execute_select_query(f"""SELECT Total_expenses FROM Savings
    WHERE Month = {month} AND Year = {year}""", db)[0]
    update_total_expenses_query = f"""UPDATE Savings
    SET Total_expenses = {current_total_expenses + total_amount}
    WHERE Month = {month} AND Year = {year}
    """
    execute_query_without_returns(update_total_expenses_query, db)
    update_savings_growth(db, month, year)


def create_earning_categories_table(db):
    query = """CREATE TABLE IF NOT EXISTS Earning_categories(
    Earning_category_ID INTEGER PRIMARY KEY,
    Earning_category_name VARCHAR(256) NOT NULL
    )
    """
    execute_query_without_returns(query, db)


def add_earning_category(earning_category_name, db):
    query = """INSERT INTO Earning_categories(Earning_category_name)
    VALUES(?)"""
    execute_query_without_returns(query, db, earning_category_name)


def get_all_earning_categories(db):
    query = """SELECT Earning_category_name FROM Earning_categories"""
    return execute_select_query(query, db)


def create_earning_types_table(db):
    query = """CREATE TABLE IF NOT EXISTS Earning_types(
    Earning_type_ID INTEGER PRIMARY KEY, 
    Earning_type_name VARCHAR(256) NOT NULL,
    Earning_category_ID INTEGER NOT NULL,
    FOREIGN KEY(Earning_category_ID) REFERENCES Earning_categories(Earning_category_ID)
    )
    """
    execute_query_without_returns(query, db)


def add_earning_type(earning_type_name, earning_category_name, db):
    query = f"""INSERT INTO Earning_types(Earning_type_name, Earning_category_ID)
    VALUES(?, ?)
    """
    query_id = f"""SELECT Earning_category_ID FROM Earning_categories
    WHERE Earning_category_name = ?"""
    print(execute_select_query(query_id, db, earning_category_name))
    earning_category_id = execute_select_query(query_id, db, earning_category_name)[0]
    execute_query_without_returns(query, db, earning_type_name, earning_category_id)
    
    
def get_all_earning_types_in_category(earning_category_name, db):
    if earning_category_name == '' or earning_category_name is None:
        return []
    query = """SELECT Earning_type_name FROM Earning_types
    WHERE Earning_category_ID = ?
    """
    query_id = f"""SELECT Earning_category_ID FROM Earning_categories
    WHERE Earning_category_name = ?"""
    earning_category_id = execute_select_query(query_id, db, earning_category_name)[0]
    return execute_select_query(query, db, earning_category_id)


def create_earnings_table(db):
    query = f"""CREATE TABLE IF NOT EXISTS Earnings (
    Earning_ID INTEGER PRIMARY KEY,
    Earning_type_ID INTEGER NOT NULL,
    Month INTEGER NOT NULL,
    Year INTEGER NOT NULL,
    Amount REAL NOT NULL,
    FOREIGN KEY (Earning_type_ID) REFERENCES Earning_types(Earning_type_ID)
    )
    """
    execute_query_without_returns(query, db)


def add_earnings(earning_type_name, month, year, amount, db):
    query = f"""INSERT INTO Earnings(Earning_type_id, Month, Year, Amount)
        VALUES(?, ?, ?, ?)
    """
    query_id = """SELECT Earning_type_id FROM Earning_types
    WHERE Earning_type_name = ?
    """
    earning_type_id = execute_select_query(query_id, db, earning_type_name)[0]
    execute_query_without_returns(query, db, earning_type_id, month, year, amount)

    current_total_earnings = execute_select_query(f"""SELECT Total_earnings FROM Savings
        WHERE Month = {month} AND Year = {year}""", db)[0]
    update_total_earnings_query = f"""UPDATE Savings
        SET Total_earnings = {current_total_earnings + amount}
        WHERE Month = {month} AND Year = {year}
        """
    execute_query_without_returns(update_total_earnings_query, db)
    update_savings_growth(db, month, year)


def create_savings_table(db):
    create_table_query = """CREATE TABLE IF NOT EXISTS Savings(
    Savings_ID INTEGER PRIMARY KEY,
    Month INTEGER NOT NULL,
    Year INTEGER NOT NULL,
    Month_start_savings REAL NOT NULL,
    Total_earnings REAL,
    Total_expenses REAL,
    Growth REAL
    )
    """
    execute_query_without_returns(create_table_query, db)


def add_savings(db, month, year,  month_start_savings):
    month_start_savings = float(month_start_savings)
    insert_query = """INSERT INTO Savings(Month, Year, Month_start_savings, Total_earnings, Total_expenses, Growth)
    VALUES(?, ?, ?, 0, 0, 0)
    """
    execute_query_without_returns(insert_query, db, month, year, month_start_savings)


def update_savings_growth(db, month, year):
    update_growth_query = f"""UPDATE Savings
        SET GROWTH = (SELECT Total_earnings FROM Savings
        WHERE Month = {month} AND Year = {year}) - (SELECT Total_expenses FROM Savings
    WHERE Month = {month} AND Year = {year})
    WHERE Month = {month} AND Year = {year}"""
    execute_query_without_returns(update_growth_query, db)


def check_if_savings_empty(db):
    get_all_savings_query = "SELECT * FROM Savings"
    result = execute_select_query(get_all_savings_query, db)
    if result:
        return False
    else:
        return True


def check_if_current_month_savings_empty(db, month, year):
    get_current_month_savings_query = f"""SELECT * FROM Savings
WHERE Month = {month} AND Year = {year}"""
    result = execute_select_query(get_current_month_savings_query, db)
    if result:
        return False
    else:
        return True


def get_current_month_savings(db, month, year):
    select_current_month_savings_query = f"""SELECT Month_start_savings + Growth FROM Savings
        WHERE Month = {month} AND Year = {year}"""
    return execute_select_query(select_current_month_savings_query, db)[0]


def get_last_month_savings(db, month, year):
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    select_last_month_savings_query = f"""SELECT Month_start_savings + Growth FROM Savings
    WHERE Month = {month} AND Year = {year}"""
    return execute_select_query(select_last_month_savings_query, db)[0]


def change_record():
    pass


def make_several_months_expenses_report(columns, months_list, group_by, db):
    results = []
    with sqlite3.connect(db) as connection:
        connection.isolation_level = None
        cursor = connection.cursor()
        for month in months_list:
            cursor.execute('begin')
            try:
                create_view_query = f"""CREATE VIEW IF NOT EXISTS 'Expenses {month}' AS
                    SELECT Products_services.Product_service_name, Expense_categories.Expense_category_name,
                    Expense_subcategories.Expense_subcategory_name, Temp_table.Quantity,
                    Temp_table.Total_amount FROM Products_services
                    FULL JOIN Expense_subcategories
                    ON Products_services.Expense_subcategory_ID = Expense_subcategories.Expense_subcategory_ID
                    FULL JOIN Expense_categories
                    ON Expense_subcategories.Expense_category_ID = Expense_categories.Expense_category_ID
                    FULL JOIN
                    (SELECT * FROM Expenses
                    WHERE Month = {month[0]} AND Year = {month[1]}) AS Temp_table
                    ON Products_services.Product_service_ID = Temp_table.Product_service_ID
                    """
                cursor.execute(create_view_query)
                month_report_query = f"""SELECT {columns}, SUM(Quantity), SUM(Total_amount), 
                ROUND((Total_amount)/SUM(Quantity), 2) FROM 'Expenses {month}'
    GROUP BY {group_by}"""
                cursor.execute(month_report_query)
                month_results = cursor.fetchall()
                total_query = f"SELECT SUM(Quantity), SUM(Total_amount) FROM 'Expenses {month}'"
                print(cursor.execute(total_query).fetchall())
                month_results.append(('Total', *cursor.execute(total_query).fetchall()[0]))
                results.append(month_results)
                cursor.execute('commit')
            except sqlite3.Error as e:
                print(e)
                cursor.execute('rollback')
        return results


def make_several_months_earnings_report(columns, months_list, group_by, db):
    results = []
    with sqlite3.connect(db) as connection:
        connection.isolation_level = None
        cursor = connection.cursor()
        for month in months_list:
            cursor.execute('begin')
            try:
                create_view_query = f"""CREATE VIEW IF NOT EXISTS 'Earnings {month}' AS
                SELECT Earning_types.Earning_type_name, Earning_categories.Earning_category_name,
                Temp_table.Amount FROM Earning_types
                FULL JOIN Earning_categories
                ON Earning_types.Earning_category_ID = Earning_categories.Earning_category_ID
                FULL JOIN
                (SELECT * FROM Earnings
                WHERE Month = {month[0]} AND Year = {month[1]}) AS Temp_table
                ON Earning_types.Earning_type_ID = Temp_table.Earning_type_ID
                """
                cursor.execute(create_view_query)
                month_report_query = f"""SELECT {columns}, SUM(Amount) FROM 'Earnings {month}'
GROUP BY {group_by}"""
                cursor.execute(month_report_query)
                month_results = cursor.fetchall()
                total_query = f"SELECT SUM(Amount) FROM 'Earnings {month}'"
                month_results.append(('Total', cursor.execute(total_query).fetchall()[0][0]))
                results.append(month_results)
                cursor.execute('commit')
                print(results)
            except sqlite3.Error as e:
                print(e)
                cursor.execute('rollback')
        return results


def make_several_months_savings_report(months_list, db):
    results = []
    with sqlite3.connect(db) as connection:
        connection.isolation_level = None
        cursor = connection.cursor()
        for month in months_list:
            cursor.execute('begin')
            try:
                select_query = f"""
                SELECT Month_start_savings, Total_earnings, Total_expenses, Growth FROM Savings
                WHERE Month = {month[0]} AND Year = {month[1]}
                """
                month_results = cursor.execute(select_query).fetchall()
                results.append(month_results[0])
                cursor.execute('commit')
            except sqlite3.Error as e:
                print(e)
                cursor.execute('rollback')
        total_query = f"""SELECT (Month_start_savings + Growth) FROM Savings
        WHERE Month = {months_list[-1][0]} AND Year = {months_list[-1][1]}"""
        total = cursor.execute(total_query).fetchall()
        results.append(('Total', total[0][0]))
        return results


def get_months_from_db(table, db):
    query = f"""SELECT Month, Year
    FROM {table}"""
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        res = sorted(list(set(cursor.fetchall())))
    res = list(map(join_month_year_tuple_to_str, res))
    return res


def get_current_month_numeric():
    return datetime.date.today().month


def get_current_month_str():
    return datetime.date.today().strftime('%B')


def get_current_year():
    return datetime.date.today().year


def turn_numeric_month_to_str(numeric_month):
    return datetime.datetime.strptime(f'{numeric_month}', '%m').strftime('%B')


def join_month_year_tuple_to_str(month_year_tuple):
    month_year_tuple = (turn_numeric_month_to_str(month_year_tuple[0]), month_year_tuple[1])
    month_year_tuple = list(map(str, month_year_tuple))
    ', '.join(month_year_tuple)
    return ', '.join(month_year_tuple)


def turn_month_year_strs_to_numeric_tuples(first_month_str, last_month_str):
    # print(first_month_str, last_month_str)
    first_month_str_list = first_month_str.split(', ')
    first_month_numeric = tuple([datetime.datetime.strptime(first_month_str_list[0], '%B').month,
                                 int(first_month_str_list[1])])
    last_month_str_list = last_month_str.split(', ')
    last_month_numeric = tuple([datetime.datetime.strptime(last_month_str_list[0], '%B').month,
                                int(last_month_str_list[1])])
    months_list = []
    for year in range(first_month_numeric[1], last_month_numeric[1] + 1):
        if first_month_numeric[1] == last_month_numeric[1]:
            for month in range(first_month_numeric[0], last_month_numeric[0] + 1):
                months_list.append((month, year))
        else:
            if year == first_month_numeric[1]:
                for month in range(first_month_numeric[0], 13):
                    months_list.append((month, year))
            elif year == last_month_numeric[1]:
                for month in range(1, last_month_numeric[0] + 1):
                    months_list.append((month, year))
            else:
                for month in range(1, 13):
                    months_list.append((month, year))
    return months_list


def populate_db(db):
    for table in ['Earning_categories', 'Earning_types', 'Earnings', 'Expense_categories', 'Expense_subcategories',
                  'Products_services', 'Expenses']:
        with sqlite3.connect(db) as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM {table}')
            connection.commit()
    earn_dict = {'Salary': ['Advance', 'Final'],
                 'Stipend': ['Stipend']}
    for category in earn_dict.keys():
        add_earning_category(category, db)
        for atype in earn_dict[category]:
            add_earning_type(atype, category, db)
            for month in range(2, 5):
                add_earnings(atype, month, 2024, 2000, db)
    exp_dict = {
        'Apartment': [{'Rent': ['Rent']}, {'Communal services': ['Electricity', 'Water', 'General']}],
        'Food': [{'Meat': ['Pork', 'Beef']}, {'Fruit': ['Banana', 'Orange']}]
    }
    for category in exp_dict.keys():
        add_expense_category(category, db)
        for subcategory in exp_dict[category]:
            add_expense_subcategory(list(subcategory.keys())[0], category, db)
            for product in subcategory[list(subcategory.keys())[0]]:
                add_product_service(product, list(subcategory.keys())[0], db)
                for month in range(2,5):
                    add_expenses(product, month, 2024, 2, 1000, db)


def execute_query_without_returns(query, db, *values):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        values = [str(value) for value in values]
        # print(values)
        cursor.execute(query, values)
        connection.commit()


def execute_select_query(query, db, *values):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        values = [str(value) for value in values]
        cursor.execute(query, values)
        results = [atuple[0] for atuple in cursor.fetchall()]
    return results


if __name__ == "__main__":
    database = 'finances_db.db'
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()

    # print(make_several_months_savings_report([(2, 2024), (3, 2024), (4, 2024)], database))
    print(check_if_savings_empty(database))
    # print(check_if_current_month_savings_empty(database, 4, 2024))
    # print(get_last_month_savings(database, 3, 2024))
