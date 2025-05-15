import pandas as pd
import datetime

# File to save the budget data
FILENAME = "budget_tracker.csv"

# Set your monthly budget limit here
MONTHLY_LIMIT = 2000

# Load or create the spreadsheet
try:
    df = pd.read_csv(FILENAME)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Type", "Amount", "Description"])
    df.to_csv(FILENAME, index=False)

def add_entry(entry_type, amount, description):
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Type": entry_type.capitalize(),  # Income or Expense
        "Amount": float(amount),
        "Description": description
    }
    global df
    new_row_df = pd.DataFrame([[new_entry["Date"], new_entry["Type"], new_entry["Amount"], new_entry["Description"]]],
                          columns=["Date", "Type", "Amount", "Description"])
    df = pd.concat([df, new_row_df], ignore_index=True)
    df.to_csv(FILENAME, index=False)

# Function to check budget status
def check_budget():
    monthly_expenses = df[(df["Type"] == "Expense") & 
                          (pd.to_datetime(df["Date"]).dt.month == datetime.now().month)]
    total_spent = monthly_expenses["Amount"].sum()
    print(f"\n💰 Total spent this month: ${total_spent:.2f}")
    print(f"📊 Monthly limit: ${MONTHLY_LIMIT:.2f}")
    if total_spent > MONTHLY_LIMIT:
        print("⚠️ You're over your budget!")
    else:
        print("✅ You're within budget.")


while True:
    print("\n1. Add Expense\n2. Add Income\n3. Check Budget\n4. Exit")
    choice = input("Select an option: ")

    if choice == "1":
        amt = input("Enter expense amount: ")
        desc = input("Enter expense description: ")
        add_entry("Expense", amt, desc)

    elif choice == "2":
        amt = input("Enter income amount: ")
        desc = input("Enter income description: ")
        add_entry("Income", amt, desc)

    elif choice == "3":
        check_budget()

    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Try again.")
