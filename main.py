import csv
from datetime import datetime
from collections import defaultdict
from pathlib import Path

FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Travel", "Study", "Bills", "Fun", "Health", "Shopping", "Other"]


def ensure_file():
    """Create the CSV file with a header if it does not exist."""
    if not FILE.exists():
        with FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


def load_expenses():
    """Load saved expenses from the CSV file."""
    ensure_file()
    with FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_expense(row):
    """Append one validated expense to the CSV file."""
    ensure_file()
    with FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow(row)


def get_valid_date():
    """Prompt until the user enters a valid YYYY-MM-DD date."""
    while True:
        value = input("Date (YYYY-MM-DD, or Enter for today): ").strip()
        if not value:
            value = datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Example of the required format: 2026-10-25")


def get_valid_amount():
    """Prompt until the user enters a non-negative numeric amount."""
    while True:
        value = input("Amount: ").strip()
        try:
            amount = float(value)
            if amount < 0:
                print("Amount cannot be negative.")
                continue
            if amount != amount or amount == float("inf") or amount == float("-inf"):
                print("Please enter a finite number.")
                continue
            return f"{amount:.2f}"
        except ValueError:
            print("Invalid amount. Please enter a number such as 120.50.")


def add_expense():
    print("\n--- Add Expense ---")
    date = get_valid_date()
    print("Suggested categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()
    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip().title()

    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount = get_valid_amount()
    row = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    save_expense(row)
    print("Expense saved successfully to expenses.csv.")


def print_expenses(rows):
    if not rows:
        print("No expenses found.")
        return

    print("\n{:<12} {:<15} {:<28} {:>12}".format(
        "Date", "Category", "Description", "Amount"
    ))
    print("-" * 70)
    for row in rows:
        print("{:<12} {:<15} {:<28} {:>12.2f}".format(
            row["date"],
            row["category"][:15],
            row["description"][:28],
            float(row["amount"]),
        ))
    print("-" * 70)
    print(f"Records shown: {len(rows)}")


def view_all_expenses():
    print("\n--- All Expenses ---")
    print_expenses(load_expenses())


def filter_expenses():
    rows = load_expenses()
    if not rows:
        print("No expenses to filter yet.")
        return

    print("\n--- Filter Expenses ---")
    print("1. By category")
    print("2. By month (YYYY-MM)")
    choice = input("Choose filter (1-2): ").strip()

    if choice == "1":
        category = input("Enter category: ").strip().casefold()
        filtered = [row for row in rows if row["category"].casefold() == category]
    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month. Use the format YYYY-MM, for example 2026-10.")
            return
        filtered = [row for row in rows if row["date"][:7] == month]
    else:
        print("Invalid filter choice.")
        return

    print_expenses(filtered)
    if filtered:
        total = sum(float(row["amount"]) for row in filtered)
        print(f"Filtered total: {total:.2f}")


def show_summary():
    rows = load_expenses()
    if not rows:
        print("No expenses available for summary.")
        return

    totals = defaultdict(float)
    grand_total = 0.0
    biggest = None

    for row in rows:
        amount = float(row["amount"])
        totals[row["category"]] += amount
        grand_total += amount
        if biggest is None or amount > float(biggest["amount"]):
            biggest = row

    print("\n--- Spending Summary by Category ---")
    for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{category:<18} {total:>10.2f}")

    print("-" * 30)
    print(f"{'Grand total':<18} {grand_total:>10.2f}")
    print("\n--- Biggest Single Expense ---")
    print(f"Date: {biggest['date']}")
    print(f"Category: {biggest['category']}")
    print(f"Description: {biggest['description']}")
    print(f"Amount: {float(biggest['amount']):.2f}")


def main():
    ensure_file()
    while True:
        print("\n====================================")
        print("       PERSONAL EXPENSE TRACKER")
        print("====================================")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Category summary statistics")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Your expenses are saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
