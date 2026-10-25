# Personal Expense Tracker with CSV

A beginner-friendly Python command-line application for recording daily expenses, storing them in a CSV file, filtering records, and summarising spending.

## Features
- Add expenses with date, category, description, and amount
- View all saved expenses
- Filter expenses by category or month (`YYYY-MM`)
- Summarise spending by category
- Display grand total and biggest single expense
- Validate dates and non-negative numeric amounts
- Save data in `expenses.csv` so it remains available after restarting
- Create the CSV file and header automatically if it is missing

## Requirements
- Python 3.10 or newer
- No external packages required

## How to run
1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open Terminal → New Terminal.
4. Run:

   ```powershell
   python main.py
   ```

   If `python` is not recognised on Windows, try `py main.py`.

5. Use the menu:
   - `1` Add expense
   - `2` View all expenses
   - `3` Filter expenses
   - `4` Category summary statistics
   - `5` Quit

## CSV format
The program creates `expenses.csv` with this header:

`date,category,description,amount`

Example row:

`2026-10-04,Food,Lunch,120.50`

The included `expenses.csv` contains fictional sample data only. You can replace it or add your own sample entries. Do not store real bank details or other sensitive financial information in this learning project.

## Concepts practised
CSV reading and writing, `csv.DictReader`, `csv.DictWriter`, date validation with `datetime.strptime`, loops, functions, filtering, dictionaries, totals, and exception handling.

## Author
Vinothini V
