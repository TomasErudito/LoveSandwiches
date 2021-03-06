"""
This module is cool
"""
from pprint import pprint
from google.oauth2.service_account import Credentials
import gspread

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, sheet_name):
    """
    Update worksheet, add new row with the list data provided
    """
    pprint(data)
    print(f"Updating {sheet_name} worksheet...\n")
    the_worksheet = SHEET.worksheet(sheet_name)
    the_worksheet.append_row(data)
    print(f"{sheet_name} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stockand calculate surplus for each item
    """
    print("Calculating surplus data\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_five():
    """
    Collect 5 entries
    """
    sales= SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:-1])
    return columns


def calculate_stock(data):
    """
    Calculate average and add 10%
    """
    print("Calculating stock data\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average_stock = sum(int_column)/ len(int_column)
        stock_num = average_stock * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_column = get_last_five()
    stock_data = calculate_stock(sales_column)
    update_worksheet(stock_data, "stock")


print("welcome to my program")


main()
