import sys
import os

# Optional: Uncomment the two lines below if running from outside the project folder
# os.chdir(r"C:\Users\Karan Raj\OneDrive\Desktop\Education\Pythonproject")
# sys.path.append(r"C:\Users\Karan Raj\OneDrive\Desktop\Education\Pythonproject")

import storage

# =====================================================================
# SECTION 1: INPUT HANDLING AND VALIDATION MODULE
# MEMBER: Avni (Roll No: S26CSEU1279)
# WORK: Takes user inputs and uses try-except to stop invalid entries
# =====================================================================

def get_valid_amount(prompt_text):
    while True:
        try:
            amount = float(input(prompt_text))
            if amount <= 0:
                print("Amount should be more than 0. Try again.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Error: Please enter a valid number for the amount.")


def get_non_empty_text(prompt_text):
    while True:
        text = input(prompt_text).strip()
        # Replace commas so CSV file format does not break
        text = text.replace(",", " ")
        if text == "":
            print("Error: This field cannot be empty. Please type something.")
        else:
            return text


def add_expense_input():
    print("\n--- Add a New Expense ---")
    date = get_non_empty_text("Enter date in DD-MM-YYYY format (e.g. 15-11-2026): ")
    print("Common categories: Food, Travel, Hostel, Study, Shopping, Other")
    category = get_non_empty_text("Enter category: ").title()
    amount = get_valid_amount("Enter the amount in Rs: ")
    note = get_non_empty_text("Enter short note (e.g. Canteen lunch, Auto fare): ")

    record = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }
    print("Successfully added:", category, "- Rs.", amount)
    return record


def set_income_and_budget_input():
    print("\n--- Set Monthly Income / Pocket Money & Budget ---")
    income = get_valid_amount("Enter your total monthly pocket money or income (Rs): ")
    while True:
        budget = get_valid_amount("Enter your monthly spending budget limit (Rs): ")
        if budget > income:
            print("Note: Your budget is higher than your income!")
            confirm = input("Do you still want to keep this budget? (yes/no): ").strip().lower()
            if confirm == "yes" or confirm == "y":
                break
        else:
            break
    return income, budget


# =====================================================================
# SECTION 2: ANALYSIS MODULE
# MEMBER: Manashvi (Roll No: S26CSEU1222)
# WORK: Calculates total spending, groups by category, and filters month
# =====================================================================

def calculate_total_expenses(expenses):
    total = 0.0
    for item in expenses:
        total = total + item["Amount"]
    return round(total, 2)


def get_category_totals(expenses):
    category_dict = {}
    for item in expenses:
        cat = item["Category"]
        amt = item["Amount"]
        if cat in category_dict:
            category_dict[cat] = round(category_dict[cat] + amt, 2)
        else:
            category_dict[cat] = round(amt, 2)
    return category_dict


def find_highest_and_lowest_category(category_dict):
    highest_cat = "None"
    highest_amt = 0.0
    lowest_cat = "None"
    lowest_amt = -1.0

    for cat in category_dict:
        amt = category_dict[cat]
        if amt > highest_amt:
            highest_amt = amt
            highest_cat = cat
        if lowest_amt == -1.0 or amt < lowest_amt:
            lowest_amt = amt
            lowest_cat = cat

    if lowest_amt == -1.0:
        lowest_amt = 0.0

    return highest_cat, highest_amt, lowest_cat, lowest_amt


def show_category_analysis(expenses):
    print("\n--- Category-Wise Expense Analysis ---")
    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    total_spent = calculate_total_expenses(expenses)
    category_dict = get_category_totals(expenses)

    print("Total Money Spent: Rs.", total_spent)
    print("\nBreakdown by Category:")
    for cat in category_dict:
        cat_amt = category_dict[cat]
        percentage = round((cat_amt / total_spent) * 100, 1)
        print("- " + cat + ": Rs. " + str(cat_amt) + " (" + str(percentage) + "%)")

    high_cat, high_amt, low_cat, low_amt = find_highest_and_lowest_category(category_dict)
    print("\nHighest Spending Category:", high_cat, "(Rs.", high_amt, ")")
    print("Lowest Spending Category:", low_cat, "(Rs.", low_amt, ")")


def filter_by_month(expenses):
    print("\n--- Filter Expenses by Month ---")
    if len(expenses) == 0:
        print("No expenses available to filter.")
        return

    month_year = get_non_empty_text("Enter month and year in MM-YYYY format (e.g. 11-2026): ")
    found_count = 0
    month_total = 0.0

    print("\nExpenses recorded in month:", month_year)
    for item in expenses:
        if month_year in item["Date"]:
            found_count = found_count + 1
            month_total = month_total + item["Amount"]
            print(
                str(found_count) + ". Date: " + item["Date"] +
                " | Category: " + item["Category"] +
                " | Rs. " + str(item["Amount"]) +
                " | Note: " + item["Note"]
            )

    if found_count == 0:
        print("No expenses found for", month_year)
    else:
        print("Total items in", month_year, ":", found_count)
        print("Total spent in", month_year, ": Rs.", round(month_total, 2))


# =====================================================================
# SECTION 3: BUDGET AND ALERT MODULE
# MEMBER: Pranjal (Roll No: S26CSEU1209)
# WORK: Checks budget limit, prints warnings, and shows full summary
# =====================================================================

def check_budget_alerts(total_spent, income, budget, expenses):
    print("\n--- Budget Status and Alerts ---")
    if budget <= 0:
        print("You have not set a monthly budget yet.")
        print("Please choose Option 2 from the main menu to set your budget.")
        return

    remaining_budget = round(budget - total_spent, 2)
    remaining_income = round(income - total_spent, 2)
    usage_percent = round((total_spent / budget) * 100, 1)

    print("Monthly Pocket Money / Income : Rs.", income)
    print("Monthly Budget Limit          : Rs.", budget)
    print("Total Expenses So Far         : Rs.", total_spent)
    print("Budget Used                   :", usage_percent, "%")

    # Rule-based budget warning checks
    if total_spent > budget:
        overspent = round(total_spent - budget, 2)
        print("\n[ALERT] WARNING: You have crossed your monthly budget by Rs.", overspent)
    elif usage_percent >= 80:
        print("\n[ALERT] CAREFUL: You have used", usage_percent, "% of your budget.")
        print("You only have Rs.", remaining_budget, "left to spend for this month.")
    else:
        print("\n[STATUS] SAFE: You are within your budget.")
        print("Remaining budget available: Rs.", remaining_budget)

    print("Estimated Savings from Income : Rs.", remaining_income)

    # Simple rule-based suggestion using highest category
    if len(expenses) > 0:
        category_dict = get_category_totals(expenses)
        high_cat, high_amt, low_cat, low_amt = find_highest_and_lowest_category(category_dict)
        print("Suggestion: Your highest spending is on", high_cat, "(Rs.", high_amt, ").")
        if total_spent > (budget * 0.5):
            print("Try cutting down on", high_cat, "expenses to save more money this month.")


def view_all_expenses(expenses):
    print("\n--- All Recorded Expenses ---")
    if len(expenses) == 0:
        print("No expenses found.")
        return

    count = 1
    for item in expenses:
        print(
            str(count) + ". Date: " + item["Date"] +
            " | Category: " + item["Category"] +
            " | Amount: Rs. " + str(item["Amount"]) +
            " | Note: " + item["Note"]
        )
        count = count + 1

    total = calculate_total_expenses(expenses)
    print("----------------------------------------")
    print("Total Items:", len(expenses), "| Total Spent: Rs.", total)


# =====================================================================
# SECTION 4: MAIN MENU, SEARCH, AND EDIT/DELETE MODULE
# MEMBER: Karan (Roll No: S26CSEU1211)
# WORK: Main loop, category search, edit/delete, and module integration
# =====================================================================

def search_by_category(expenses):
    print("\n--- Search Expenses by Category ---")
    if len(expenses) == 0:
        print("No expenses available to search.")
        return

    search_cat = get_non_empty_text("Enter category name to search: ").title()
    found_count = 0
    cat_total = 0.0

    print("\nMatching records for category:", search_cat)
    for item in expenses:
        if item["Category"] == search_cat:
            found_count = found_count + 1
            cat_total = cat_total + item["Amount"]
            print(
                str(found_count) + ". Date: " + item["Date"] +
                " | Rs. " + str(item["Amount"]) +
                " | Note: " + item["Note"]
            )

    if found_count == 0:
        print("No expenses found in this category.")
    else:
        print("Total spent in", search_cat, ": Rs.", round(cat_total, 2))


def edit_or_delete_expense(expenses):
    print("\n--- Edit or Delete an Expense ---")
    if len(expenses) == 0:
        print("No expenses available to edit or delete.")
        return

    # Show numbered list first so user can pick a record number
    view_all_expenses(expenses)

    try:
        item_no = int(input("\nEnter the expense number you want to change (1 to " + str(len(expenses)) + "): "))
        if item_no < 1 or item_no > len(expenses):
            print("Error: Invalid expense number.")
            return
    except ValueError:
        print("Error: Please enter a valid whole number.")
        return

    index = item_no - 1
    selected = expenses[index]
    print("Selected Record:", selected["Date"], "|", selected["Category"], "| Rs.", selected["Amount"], "|", selected["Note"])

    print("1. Edit this expense")
    print("2. Delete this expense")
    print("3. Cancel")
    action = input("Enter your choice (1, 2, or 3): ").strip()

    if action == "1":
        print("\nEnter new details for this expense:")
        new_date = get_non_empty_text("Enter new date (DD-MM-YYYY): ")
        new_category = get_non_empty_text("Enter new category: ").title()
        new_amount = get_valid_amount("Enter new amount in Rs: ")
        new_note = get_non_empty_text("Enter new short note: ")

        expenses[index] = {
            "Date": new_date,
            "Category": new_category,
            "Amount": new_amount,
            "Note": new_note
        }
        storage.save_all_expenses(expenses)
        print("Expense updated and saved to file successfully!")

    elif action == "2":
        removed = expenses.pop(index)
        storage.save_all_expenses(expenses)
        print("Deleted expense:", removed["Category"], "- Rs.", removed["Amount"])

    else:
        print("Action cancelled. No changes were made.")


def main():
    # Load previously saved data from files at program start
    expenses = storage.load_expenses()
    income, budget = storage.load_budget_and_income()

    print("Welcome to Personal Expense and Budget Analyzer!")
    print("Loaded", len(expenses), "previous expense records from file.")

    while True:
        print("\n=== Personal Expense Analyzer Menu ===")
        print("1. Add a New Expense")
        print("2. Set Monthly Income and Budget")
        print("3. View All Expenses")
        print("4. Category-Wise Analysis (Highest & Lowest)")
        print("5. Check Budget Status and Alerts")
        print("6. Search Expenses by Category")
        print("7. Filter Expenses by Month")
        print("8. Edit or Delete an Expense")
        print("9. Exit")

        choice = input("Enter your choice (1 to 9): ").strip()

        if choice == "1":
            new_record = add_expense_input()
            expenses.append(new_record)
            storage.save_expense_to_file(new_record)
            if budget > 0:
                total_now = calculate_total_expenses(expenses)
                if total_now > budget:
                    print("[Quick Alert] Total spending (Rs.", total_now, ") has exceeded your budget (Rs.", budget, ")!")

        elif choice == "2":
            income, budget = set_income_and_budget_input()
            storage.save_budget_and_income(income, budget)
            print("Monthly income and budget saved successfully!")

        elif choice == "3":
            view_all_expenses(expenses)

        elif choice == "4":
            show_category_analysis(expenses)

        elif choice == "5":
            total_spent = calculate_total_expenses(expenses)
            check_budget_alerts(total_spent, income, budget, expenses)

        elif choice == "6":
            search_by_category(expenses)

        elif choice == "7":
            filter_by_month(expenses)

        elif choice == "8":
            edit_or_delete_expense(expenses)

        elif choice == "9":
            print("\nSaving data and closing program.")
            print("Total expense items recorded:", len(expenses))
            print("Thank you for using Personal Expense Analyzer!")
            break

        else:
            print("Invalid choice! Please type a number from 1 to 9.")


if __name__ == "__main__":
    main()