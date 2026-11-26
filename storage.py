# =====================================================================
# MODULE: STORAGE MODULE (storage.py)
# MEMBER: Arun (Roll No: S25CSEU1305)
# WORK: File handling to save and load data from CSV and TXT files
# =====================================================================

EXPENSE_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"


def load_expenses():
    expenses = []
    try:
        file = open(EXPENSE_FILE, "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            clean_line = line.strip()
            if clean_line != "":
                parts = clean_line.split(",")
                # Skip the header line if present
                if parts[0] == "Date":
                    continue
                if len(parts) == 4:
                    record = {
                        "Date": parts[0],
                        "Category": parts[1],
                        "Amount": float(parts[2]),
                        "Note": parts[3]
                    }
                    expenses.append(record)
    except FileNotFoundError:
        # If the file does not exist yet, return an empty list
        expenses = []

    return expenses


def save_expense_to_file(record):
    # Check if file is new so we can write column headers first
    file_exists = False
    try:
        check_file = open(EXPENSE_FILE, "r")
        first_line = check_file.readline()
        check_file.close()
        if first_line != "":
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    file = open(EXPENSE_FILE, "a")
    if not file_exists:
        file.write("Date,Category,Amount,Note\n")

    line = (
        record["Date"] + "," +
        record["Category"] + "," +
        str(record["Amount"]) + "," +
        record["Note"] + "\n"
    )
    file.write(line)
    file.close()


def save_all_expenses(expenses):
    # Rewrites the full list to CSV after an expense is edited or deleted
    file = open(EXPENSE_FILE, "w")
    file.write("Date,Category,Amount,Note\n")
    for record in expenses:
        line = (
            record["Date"] + "," +
            record["Category"] + "," +
            str(record["Amount"]) + "," +
            record["Note"] + "\n"
        )
        file.write(line)
    file.close()


def save_budget_and_income(income, budget):
    file = open(BUDGET_FILE, "w")
    file.write(str(income) + "," + str(budget) + "\n")
    file.close()


def load_budget_and_income():
    income = 0.0
    budget = 0.0
    try:
        file = open(BUDGET_FILE, "r")
        line = file.readline().strip()
        file.close()
        if line != "":
            parts = line.split(",")
            income = float(parts[0])
            budget = float(parts[1])
    except FileNotFoundError:
        income = 0.0
        budget = 0.0

    return income, budget