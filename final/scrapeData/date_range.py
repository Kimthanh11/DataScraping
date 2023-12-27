from datetime import datetime

def get_year(date_string):
    return str(datetime.strptime(date_string, "%d/%m/%Y").year)

def get_quarter_year(date_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    quarter = (date.month - 1) // 3 + 1
    return str(quarter)

# Define your start_day and end_day variables here or pass them as arguments
start_day ="30/12/2019"
end_day = "30/06/2023"

# Functions to get year, quarter, and month from start and end dates
def get_start_year():
    return get_year(start_day)

def get_end_year():
    return get_year(end_day)

def get_start_quarter_year():
    return get_quarter_year(start_day)

def get_end_quarter_year():
    return get_quarter_year(end_day)

def get_month(date_string):
    return str(datetime.strptime(date_string, "%d/%m/%Y").strftime("%m")).replace("0", "")