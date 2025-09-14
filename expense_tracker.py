import json
import os
import csv
from datetime import datetime
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# File names
JSON_FILE = "expenses.json"
CSV_FILE = "expenses.csv"

# Default categories
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Other"]

# Load expenses from JSON
def load_expenses():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []

# Save expenses to JSON
def save_expenses(expenses):
    with open(JSON_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# Add expense
def add_expense(expenses):
    try:
        amount = float(input(Fore.CYAN + "💵 Amount (PKR): "))
    except ValueError:
        print(Fore.RED + "❌ Please enter a valid number!")
        return

    print(Fore.YELLOW + "\nAvailable Categories:")
    for i, c in enumerate(CATEGORIES, start=1):
        print(f"{i}. {c}")
    category_choice = input(Fore.CYAN + "Choose category number (or type custom): ")

    if category_choice.isdigit() and 1 <= int(category_choice) <= len(CATEGORIES):
        category = CATEGORIES[int(category_choice) - 1]
    else:
        category = category_choice

    description = input(Fore.CYAN + "📝 Description: ")

    date_input = input(Fore.CYAN + "📅 Date (YYYY-MM-DD) [Leave blank for today]: ")
    try:
        date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d") if date_input else datetime.now().strftime("%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "❌ Invalid date format! Using today's date.")
        date = datetime.now().strftime("%Y-%m-%d")

    expenses.append({"amount": amount, "category": category, "description": description, "date": date})
    save_expenses(expenses)
    print(Fore.GREEN + "✅ Expense added successfully!")

# View expenses
def view_expenses(expenses):
    if not expenses:
        print(Fore.YELLOW + "⚠ No expenses recorded yet.")
        return
    print(Fore.MAGENTA + "\n📊 Your Expenses:")
    for i, e in enumerate(expenses, start=1):
        print(f"{i}. {e['amount']} PKR | {e['category']} | {e['description']} | {e['date']}")

# Edit expense
def edit_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input(Fore.CYAN + "✏ Enter expense number to edit: ")) - 1
        if index < 0 or index >= len(expenses):
            print(Fore.RED + "❌ Invalid expense number.")
            return

        new_amount = input("💵 New amount (leave blank to keep): ")
        if new_amount:
            try:
                expenses[index]["amount"] = float(new_amount)
            except ValueError:
                print(Fore.RED + "❌ Invalid number! Skipping amount update.")

        new_category = input("📂 New category (leave blank to keep): ")
        if new_category:
            expenses[index]["category"] = new_category

        new_description = input("📝 New description (leave blank to keep): ")
        if new_description:
            expenses[index]["description"] = new_description

        new_date = input("📅 New date (YYYY-MM-DD, leave blank to keep): ")
        if new_date:
            try:
                expenses[index]["date"] = datetime.strptime(new_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "❌ Invalid date format! Skipping date update.")

        save_expenses(expenses)
        print(Fore.GREEN + "✅ Expense updated!")

    except ValueError:
        print(Fore.RED + "❌ Please enter a valid number.")

# Delete expense
def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input(Fore.CYAN + "❌ Enter expense number to delete: ")) - 1
        if index < 0 or index >= len(expenses):
            print(Fore.RED + "❌ Invalid expense number.")
            return
        removed = expenses.pop(index)
        save_expenses(expenses)
        print(Fore.GREEN + f"🗑 Deleted: {removed['amount']} PKR | {removed['category']}")
    except ValueError:
        print(Fore.RED + "❌ Please enter a valid number.")

# Search expenses
def search_expenses(expenses):
    keyword = input(Fore.CYAN + "🔍 Search by keyword or category: ").lower()
    results = [e for e in expenses if keyword in e['category'].lower() or keyword in e['description'].lower()]
    if results:
        print(Fore.MAGENTA + "\n📊 Search Results:")
        for i, e in enumerate(results, start=1):
            print(f"{i}. {e['amount']} PKR | {e['category']} | {e['description']} | {e['date']}")
    else:
        print(Fore.YELLOW + "⚠ No matching expenses found.")

# Show summary
def show_summary(expenses):
    if not expenses:
        print(Fore.YELLOW + "⚠ No expenses to summarize.")
        return
    summary, total = {}, 0
    for e in expenses:
        summary[e['category']] = summary.get(e['category'], 0) + e['amount']
        total += e['amount']
    print(Fore.MAGENTA + "\n📊 Expense Summary:")
    for cat, amt in summary.items():
        print(Fore.CYAN + f"📂 {cat}: {amt} PKR")
    print(Fore.GREEN + f"💵 TOTAL: {total} PKR")

# Sort expenses
def sort_expenses(expenses):
    if not expenses:
        print(Fore.YELLOW + "⚠ No expenses to sort.")
        return
    print(Fore.YELLOW + "\nSort by:")
    print("1. Date")
    print("2. Amount")
    choice = input(Fore.CYAN + "Choose option: ")
    if choice == "1":
        sorted_expenses = sorted(expenses, key=lambda x: x['date'])
    elif choice == "2":
        sorted_expenses = sorted(expenses, key=lambda x: x['amount'], reverse=True)
    else:
        print(Fore.RED + "❌ Invalid choice.")
        return
    print(Fore.MAGENTA + "\n📊 Sorted Expenses:")
    for i, e in enumerate(sorted_expenses, start=1):
        print(f"{i}. {e['amount']} PKR | {e['category']} | {e['description']} | {e['date']}")

# Export to CSV
def export_csv(expenses):
    if not expenses:
        print(Fore.YELLOW + "⚠ No expenses to export.")
        return
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["amount", "category", "description", "date"])
        writer.writeheader()
        writer.writerows(expenses)
    print(Fore.GREEN + f"✅ Expenses exported to {CSV_FILE}")

# Menu
def print_menu():
    print(Fore.BLUE + "\n🌟=================================🌟")
    print(Fore.YELLOW + "        💰 Expense Tracker 💰")
    print(Fore.BLUE + "🌟=================================🌟\n")
    print(Fore.GREEN  + "🟢 1. ➕ Add Expense")
    print(Fore.CYAN   + "🔵 2. 📋 View Expenses")
    print(Fore.MAGENTA+ "🟠 3. ✏ Edit Expense")
    print(Fore.RED    + "🔴 4. ❌ Delete Expense")
    print(Fore.YELLOW + "🟣 5. 🔍 Search / Filter")
    print(Fore.CYAN   + "🟡 6. 📊 Summary")
    print(Fore.BLUE   + "🟢 7. 📑 Sort Expenses")
    print(Fore.MAGENTA+ "🟠 8. 💾 Export to CSV")
    print(Fore.RED    + "⚫ 9. 🚪 Exit")
    print(Fore.BLUE   + "=====================================")

# Main loop
def main():
    expenses = load_expenses()
    while True:
        print_menu()
        choice = input(Fore.CYAN + "👉 Choose an option: ")
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            search_expenses(expenses)
        elif choice == "6":
            show_summary(expenses)
        elif choice == "7":
            sort_expenses(expenses)
        elif choice == "8":
            export_csv(expenses)
        elif choice == "9":
            print(Fore.GREEN + "👋 Exiting... Goodbye!")
            break
        else:
            print(Fore.RED + "❌ Invalid choice.")

if __name__ == "__main__":
    main()


