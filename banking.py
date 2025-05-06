import datetime
import os
import hashlib
import pwinput

# File paths
ACCOUNT_FILE = "accounts.txt"
CUSTOMER_FILE = "Customer.txt"
USERS_FILE = "Users.txt"
TRANSACTION_FILE = "transactions.txt"


# Data
accounts = {}


# Load existing accounts from file
def load_accounts():
    try:
        with open(ACCOUNT_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    acc_num, username, password, balance, role = parts
                    accounts[username] = {
                        'account_number': acc_num,
                        'password': password,
                        'balance': float(balance),
                        'role': role
                    }
    except FileNotFoundError:
        pass

# Save all accounts to file
def save_all_accounts():
    with open(ACCOUNT_FILE, "w") as f:
        for username, info in accounts.items():
            f.write(f"{info['account_number']}|{username}|{info['password']}|{info['balance']}\n")

# Record a transaction
def record_transaction(acc_num, action, last_balance, amount):
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{acc_num}|{get_current_datetime()}|{action}|{last_balance}|{amount}\n")

# Generate unique account number
def generate_account_number():
    return "AC" + str(len(os.listdir(".")) + 1000)

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, stored_password_hash):
    return hash_password(input_password) == stored_password_hash

def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Admin menu
def admin_menu(username):
    while True:
        print("\n--- Admin Panel ---")
        print("1. Create New User Account")
        print("2. Delete User Account")
        print("3. Update User Account")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. Check Balance")
        print("7. View Transaction History")
        print("8. View All Accounts")
        print("9. Search Transactions")
        print("10. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            create_user_account()
        elif choice == '2':
            delete_user_account()
        elif choice == '3':
            update_user_account()
        elif choice == '4':
            deposit(username)
        elif choice == '5':
            withdraw(username)
        elif choice == '6':
            check_balance(username)
        elif choice == '7':
            show_transaction_history(accounts[username]['account_number'])
        elif choice == '8':
            view_all_accounts()
        elif choice == '9':
            search_transactions()
        elif choice == '10':
            print("🔒 Admin logged out.")
            break
        else:
            print("❌ Invalid option. Try again.")

# Create user account (for admin use)
def create_user_account():
    print("\n--- Create New User Account ---")
    username = input("Enter new username: ")
    if username in accounts:
        print("❌ Username already exists.")
        return
    nic = input("Enter NIC number: ")
    contact = input("Enter contact number: ")
    password = pwinput.pwinput("Set password: ")
    try:
        balance = float(input("Enter initial balance (>= 0): "))
        if balance < 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid balance.")
        return

    acc_num = generate_account_number()
    accounts[username] = {
        'account_number': acc_num,
        'password': hash_password(password),
        'balance': balance,
    }
    save_all_accounts()
    record_transaction(acc_num, "Account Created", balance, balance)
    print(f"✅ Account created successfully. Account No: {acc_num}")

# Delete user account
def delete_user_account():
    username = input("Enter username to delete: ")
    if username in accounts:
        del accounts[username]
        save_all_accounts()
        print("✅ User account deleted.")
    else:
        print("❌ Username not found.")

# Update user account
def update_user_account():
    username = input("Enter username to update: ")
    if username not in accounts:
        print("❌ Username not found.")
        return

    new_password = pwinput.pwinput("Enter new password: ")
    new_balance = float(input("Enter new balance: "))
    accounts[username]['password'] = hash_password(new_password)
    accounts[username]['balance'] = new_balance
    save_all_accounts()
    print("✅ Account updated successfully.")

# User login
def user_login():
    print("\n--- Login ---")
    username = input("Enter Username: ")
    password = pwinput.pwinput("Enter Password: ")

    if username in accounts:
        if check_password(password, accounts[username]['password']):
            print(f"✅ Welcome {username}!")
            if accounts[username]['role'] == 'admin':
                admin_menu(username)
            else:
                user_menu(username)
        else:
            print("❌ Invalid credentials.")
    else:
        # No accounts in system? First user becomes admin.
        if len(accounts) == 0:
            print("🔓 First user detected. Creating admin account...")
            acc_num = generate_account_number()
            hashed_pw = hash_password(password)
            accounts[username] = {
                'account_number': acc_num,
                'password': hashed_pw,
                'balance': 0.0,
                'role': 'admin'
            }
            save_all_accounts()
            record_transaction(acc_num, "Account Created (Admin)", 0.0, 0.0)
            print(f"✅ Admin account created for {username}.")
            admin_menu(username)
        else:
            print("❌ Invalid credentials.")

# User menu
def user_menu(username):
    while True:
        print("\n--- User Dashboard ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Transaction History")
        print("5. Search Transactions")
        print("6. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            deposit(username)
        elif choice == '2':
            withdraw(username)
        elif choice == '3':
            check_balance(username)
        elif choice == '4':
            show_transaction_history(accounts[username]['account_number'])
        elif choice == '5':
            search_transactions()
        elif choice == '6':
            print("🔒 Logged out.")
            break
        else:
            print("❌ Invalid choice.")

def deposit(username):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid amount.")
        return

    accounts[username]['balance'] += amount
    save_all_accounts()
    record_transaction(accounts[username]['account_number'], "Deposit", amount, accounts[username]['balance'])
    print("✅ Deposit successful.")

def withdraw(username):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0 or amount > accounts[username]['balance']:
            raise ValueError
    except ValueError:
        print("❌ Invalid or insufficient amount.")
        return

    accounts[username]['balance'] -= amount
    save_all_accounts()
    record_transaction(accounts[username]['account_number'], "Withdrawal", amount, accounts[username]['balance'])
    print("✅ Withdrawal successful.")

def check_balance(username):
    print(f"💰 Current Balance: {accounts[username]['balance']}")

def show_transaction_history(account_number):
    print("\n📜 Transaction History:")
    found = False
    try:
        with open(TRANSACTION_FILE, "r") as f:
            for line in f:
                if line.startswith(account_number):
                    print(line.strip())
                    found = True
    except FileNotFoundError:
        print("No transaction history found.")
        return

    if not found:
        print("📭 No transactions available.")

def view_all_accounts():
    print("\n📋 All Accounts:")
    for username, info in accounts.items():
        print(f"Username: {username}, Account No: {info['account_number']}, Balance: {info['balance']}, Role: {info['role']}")

def search_transactions():
    keyword = input("Enter account number, date or action to search: ").lower()
    found = False
    try:
        with open(TRANSACTION_FILE, "r") as f:
            for line in f:
                if keyword in line.lower():
                    print(line.strip())
                    found = True
    except FileNotFoundError:
        print("Transaction file not found.")
        return
    if not found:
        print("No matching transactions found.")

# Main menu
def main_menu():
    load_accounts()
    while True:
        print("\n=== Welcome to Secure Banking App ===")
        print("1. Login")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            user_login()
        elif choice == '2':
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

# Start application
if __name__ == "__main__":
    main_menu()


