# import random

# # Files
# ACCOUNT_FILE = "accounts.txt"
# TRANSACTION_FILE = "transactions.txt"

# # Data
# accounts = {}
# ADMIN_USERNAME = "admin"
# ADMIN_PASSWORD = "admin123"


# # Load existing accounts from file
# def load_accounts():
#     try:
#         with open(ACCOUNT_FILE, "r") as f:
#             for line in f:
#                 parts = line.strip().split("|")
#                 if len(parts) == 4:
#                     acc_num, username, password, balance = parts
#                     accounts[username] = {
#                         'account_number': acc_num,
#                         'password': password,
#                         'balance': float(balance)
#                     }
#     except FileNotFoundError:
#         pass


# # Save all accounts to file
# def save_all_accounts():
#     with open(ACCOUNT_FILE, "w") as f:
#         for username, info in accounts.items():
#             f.write(f"{info['account_number']}|{username}|{info['password']}|{info['balance']}\n")


# # Record a transaction in a text file
# def record_transaction(account_number, action, amount, balance):
#     with open(TRANSACTION_FILE, "a") as f:
#         f.write(f"{account_number} | {action} | Amount: {amount} | Balance: {balance}\n")


# # Generate unique account number
# def generate_account_number():
#     return str(random.randint(10000, 99999))


# # Admin login
# def admin_login():
#     print("\n--- Admin Login ---")
#     username = input("Enter Admin Username: ")
#     password = input("Enter Admin Password: ")
#     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#         print("✅ Admin login successful!")
#         admin_menu()
#     else:
#         print("❌ Invalid admin credentials.")


# # Admin menu
# def admin_menu():
#     while True:
#         print("\n--- Admin Panel ---")
#         print("1. Create New User Account")
#         print("2. Logout")
#         choice = input("Choose an option: ")

#         if choice == '1':
#             create_user_account()
#         elif choice == '2':
#             print("🔒 Admin logged out.")
#             break
#         else:
#             print("❌ Invalid option. Try again.")


# # Create user account (Admin Only)
# def create_user_account():
#     print("\n--- Create New User Account ---")
#     username = input("Enter new username: ")
#     if username in accounts:
#         print("❌ Username already exists.")
#         return

#     password = input("Set password for user: ")
#     try:
#         balance = float(input("Enter initial balance (>= 0): "))
#         if balance < 0:
#             raise ValueError
#     except ValueError:
#         print("❌ Invalid balance.")
#         return

#     acc_num = generate_account_number()
#     accounts[username] = {
#         'account_number': acc_num,
#         'password': password,
#         'balance': balance
#     }
#     save_all_accounts()
#     record_transaction(acc_num, "Account Created", balance, balance)
#     print(f"✅ User account created successfully. Account No: {acc_num}")


# # User login
# def user_login():
#     print("\n--- User Login ---")
#     username = input("Enter Username: ")
#     password = input("Enter Password: ")
#     if username in accounts and accounts[username]['password'] == password:
#         print(f"✅ Welcome {username}!")
#         user_menu(username)
#     else:
#         print("❌ Invalid credentials.")


# # User menu
# def user_menu(username):
#     while True:
#         print("\n--- User Dashboard ---")
#         print("1. Deposit")
#         print("2. Withdraw")
#         print("3. Check Balance")
#         print("4. View Transaction History")
#         print("5. Logout")
#         choice = input("Choose an option: ")

#         if choice == '1':
#             deposit(username)
#         elif choice == '2':
#             withdraw(username)
#         elif choice == '3':
#             check_balance(username)
#         elif choice == '4':
#             show_transaction_history(accounts[username]['account_number'])
#         elif choice == '5':
#             print("🔒 Logged out.")
#             break
#         else:
#             print("❌ Invalid choice.")


# def deposit(username):
#     try:
#         amount = float(input("Enter amount to deposit: "))
#         if amount <= 0:
#             raise ValueError
#     except ValueError:
#         print("❌ Invalid amount.")
#         return

#     accounts[username]['balance'] += amount
#     save_all_accounts()
#     record_transaction(accounts[username]['account_number'], "Deposit", amount, accounts[username]['balance'])
#     print("✅ Deposit successful.")


# def withdraw(username):
#     try:
#         amount = float(input("Enter amount to withdraw: "))
#         if amount <= 0 or amount > accounts[username]['balance']:
#             raise ValueError
#     except ValueError:
#         print("❌ Invalid or insufficient amount.")
#         return

#     accounts[username]['balance'] -= amount
#     save_all_accounts()
#     record_transaction(accounts[username]['account_number'], "Withdrawal", amount, accounts[username]['balance'])
#     print("✅ Withdrawal successful.")


# def check_balance(username):
#     print(f"💰 Current Balance: {accounts[username]['balance']}")


# def show_transaction_history(account_number):
#     print("\n📜 Transaction History:")
#     found = False
#     try:
#         with open(TRANSACTION_FILE, "r") as f:
#             for line in f:
#                 if line.startswith(account_number):
#                     print(line.strip())
#                     found = True
#     except FileNotFoundError:
#         print("No transaction history found.")
#         return

#     if not found:
#         print("📭 No transactions available.")


# # Main menu
# def main_menu():
#     load_accounts()
#     while True:
#         print("\n=== Welcome to Mini Banking App ===")
#         print("1. Admin Login")
#         print("2. User Login")
#         print("3. Exit")
#         choice = input("Choose an option: ")

#         if choice == '1':
#             admin_login()
#         elif choice == '2':
#             user_login()
#         elif choice == '3':
#             print("👋 Exiting program. Goodbye!")
#             break
#         else:
#             print("❌ Invalid choice.")


# # Start the application
# if __name__ == "__main__":
#     main_menu()












import random
import hashlib
import pwinput

# Files
ACCOUNT_FILE = "accounts.txt"
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
            f.write(f"{info['account_number']}|{username}|{info['password']}|{info['balance']}|{info['role']}\n")

# Record a transaction
def record_transaction(account_number, action, amount, balance):
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{account_number}|{action}|Amount: {amount}|Balance: {balance}\n")

# Generate unique account number
def generate_account_number():
    return str(random.randint(10000, 99999))

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, stored_password_hash):
    return hash_password(input_password) == stored_password_hash

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

    password = pwinput.pwinput("Set password: ")
    try:
        balance = float(input("Enter initial balance (>= 0): "))
        if balance < 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid balance.")
        return

    role = input("Enter role (admin/user): ").strip().lower()
    if role not in ['admin', 'user']:
        print("❌ Invalid role.")
        return

    acc_num = generate_account_number()
    accounts[username] = {
        'account_number': acc_num,
        'password': hash_password(password),
        'balance': balance,
        'role': role
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






import os
import hashlib
import datetime
import pwinput

# File paths
BANK_ACCOUNT_FILE = "Bank_Account.txt"
CUSTOMER_FILE = "Customer.txt"
USERS_FILE = "Users.txt"
TRANSACTIONS_FILE = "Transactions.txt"

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_account_number():
    return str(int(datetime.datetime.now().timestamp()))

def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load data from files
def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                username, role, balance = line.strip().split("|")
                users[username] = {"role": role, "balance": float(balance)}
    return users

def load_accounts():
    accounts = {}
    if os.path.exists(BANK_ACCOUNT_FILE):
        with open(BANK_ACCOUNT_FILE, "r") as f:
            for line in f:
                acc_num, username, password_hash, balance = line.strip().split("|")
                accounts[acc_num] = {"username": username, "password": password_hash, "balance": float(balance)}
    return accounts

def load_customers():
    customers = {}
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, "r") as f:
            for line in f:
                username, acc_num, nic, contact = line.strip().split("|")
                customers[username] = {"account_number": acc_num, "nic": nic, "contact": contact}
    return customers

# Save data to files
def save_user(username, role, balance):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}|{role}|{balance}\n")

def save_account(acc_num, username, password_hash, balance):
    with open(BANK_ACCOUNT_FILE, "a") as f:
        f.write(f"{acc_num}|{username}|{password_hash}|{balance}\n")

def save_customer(username, acc_num, nic, contact):
    with open(CUSTOMER_FILE, "a") as f:
        f.write(f"{username}|{acc_num}|{nic}|{contact}\n")

def record_transaction(acc_num, action, last_balance, amount, new_balance):
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{acc_num}|{get_current_datetime()}|{action}|{last_balance}|{amount}|{new_balance}\n")

# Admin functionalities
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Customer Account")
        print("2. Deposit to Customer Account")
        print("3. Withdraw from Customer Account")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_customer_account()
        elif choice == "2":
            modify_balance("deposit")
        elif choice == "3":
            modify_balance("withdraw")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def create_customer_account():
    print("\n--- Create Customer Account ---")
    username = input("Enter username: ")
    password = pwinput.pwinput("Enter password: ")
    nic = input("Enter NIC number: ")
    contact = input("Enter contact number: ")
    try:
        balance = float(input("Enter initial balance: "))
    except ValueError:
        print("Invalid balance amount.")
        return

    acc_num = generate_account_number()
    password_hash = hash_password(password)

    save_account(acc_num, username, password_hash, balance)
    save_customer(username, acc_num, nic, contact)
    save_user(username, "customer", balance)
    record_transaction(acc_num, "Account Created", 0.0, balance, balance)
    print(f"Customer account created successfully. Account Number: {acc_num}")

def modify_balance(action):
    acc_num = input("Enter account number: ")
    accounts = load_accounts()
    if acc_num not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input(f"Enter amount to {action}: "))
    except ValueError:
        print("Invalid amount.")
        return

    last_balance = accounts[acc_num]["balance"]
    if action == "deposit":
        new_balance = last_balance + amount
    elif action == "withdraw":
        if amount > last_balance:
            print("Insufficient funds.")
            return
        new_balance = last_balance - amount
    else:
        print("Invalid action.")
        return

    # Update account balance
    accounts[acc_num]["balance"] = new_balance
    # Rewrite BANK_ACCOUNT_FILE
    with open(BANK_ACCOUNT_FILE, "w") as f:
        for acc, info in accounts.items():
            f.write(f"{acc}|{info['username']}|{info['password']}|{info['balance']}\n")
    # Update USERS_FILE
    users = load_users()
    username = accounts[acc_num]["username"]
    users[username]["balance"] = new_balance
    with open(USERS_FILE, "w") as f:
        for user, info in users.items():
            f.write(f"{user}|{info['role']}|{info['balance']}\n")
    # Record transaction
    record_transaction(acc_num, action.capitalize(), last_balance, amount, new_balance)
    print(f"{action.capitalize()} successful. New balance: {new_balance}")

# User functionalities
def user_menu(username):
    accounts = load_accounts()
    user_acc_num = None
    for acc_num, info in accounts.items():
        if info["username"] == username:
            user_acc_num = acc_num
            break
    if not user_acc_num:
        print("Account not found.")
        return

    while True:
        print("\n--- User Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Transaction History")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_deposit(user_acc_num)
        elif choice == "2":
            user_withdraw(user_acc_num)
        elif choice == "3":
            print(f"Current balance: {accounts[user_acc_num]['balance']}")
        elif choice == "4":
            view_transactions(user_acc_num)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def user_deposit(acc_num):
    accounts = load_accounts()
    try:
        amount = float(input("Enter amount to deposit: "))
    except ValueError:
        print("Invalid amount.")
        return
    last_balance = accounts[acc_num]["balance"]
    new_balance = last_balance + amount
    accounts[acc_num]["balance"] = new_balance
    # Update files
    with open(BANK_ACCOUNT_FILE, "w") as f:
        for acc, info in accounts.items():
            f.write(f"{acc}|{info['username']}|{info['password']}|{info['balance']}\n")
    users = load_users()
    username = accounts[acc_num]["username"]
    users[username]["balance"] = new_balance
    with open(USERS_FILE, "w") as f:
        for user, info in users.items():
            f.write(f"{user}|{info['role']}|{info['balance']}\n")
    record_transaction(acc_num, "Deposit", last_balance, amount, new_balance)
    print(f"Deposit successful. New balance: {new_balance}")

def user_withdraw(acc_num):
    accounts = load_accounts()
    try:
        amount = float(input("Enter amount to withdraw: "))
    except ValueError:
        print("Invalid amount.")
        return
    last_balance = accounts[acc_num]["balance"]
    if amount > last_balance:
        print("Insufficient funds.")
        return
    new_balance = last_balance - amount
    accounts[acc_num]["balance"] = new_balance
    # Update files
    with open(BANK_ACCOUNT_FILE, "w") as f:
        for acc, info in accounts.items():
            f.write(f"{acc}|{info['username']}|{info['password']}|{info['balance']}\n")
    users = load_users()
    username = accounts[acc_num]["username"]
    users[username]["balance"] = new_balance
    with open(USERS_FILE, "w") as f:
        for user, info in users.items():
            f.write(f"{user}|{info['role']}|{info['balance']}\n")
    record_transaction(acc_num, "Withdraw", last_balance, amount, new_balance)
    print(f"Withdrawal successful. New balance: {new_balance}")

def view_transactions(acc_num):
    if not os.path.exists(TRANSACTIONS_FILE):
        print("No transactions found.")
        return
    with open(TRANSACTIONS_FILE, "r") as f:
        for line in f:
            record = line.strip().split("|")
            if record[0] == acc_num:
                print(" | ".join(record))

# Authentication
def login():
    users = load_users()
    username = input("Enter username: ")
    password = pwinput.pwinput("Enter password: ")
    accounts = load_accounts()
    acc_num = None
    for acc, info in accounts.items():
        if info["username"] == username:
            acc_num = acc
            stored_password = info["password"]
            break
    if not acc_num:
        print("User not found.")
        return
        if hash_password(password) != stored_password:
            print("Incorrect password.")
        return

    role = users[username]["role"]
    print(f"Login successful! Logged in as {role.capitalize()}")
    if role == "admin":
        admin_menu()
    else:
        user_menu(username)

# Entry point
def main():
    while True:
        print("\n--- Welcome to the Simple Banking System ---")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            login()
        elif choice == "2":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

       

 
