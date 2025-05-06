# import os
# import hashlib
# import datetime
# import pwinput

# # File paths
# BANK_ACCOUNT_FILE = "Bank_Account.txt"
# CUSTOMER_FILE = "Customer.txt"
# USERS_FILE = "Users.txt"
# TRANSACTIONS_FILE = "Transactions.txt"

# # Helper functions
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def generate_account_number():
#     return str(int(datetime.datetime.now().timestamp()))

# def get_current_datetime():
#     return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# # Load data from files
# def load_users():
#     users = {}
#     if os.path.exists(USERS_FILE):
#         with open(USERS_FILE, "r") as f:
#             for line in f:
#                 username, role, balance = line.strip().split("|")
#                 users[username] = {"role": role, "balance": float(balance)}
#     return users

# def load_accounts():
#     accounts = {}
#     if os.path.exists(BANK_ACCOUNT_FILE):
#         with open(BANK_ACCOUNT_FILE, "r") as f:
#             for line in f:
#                 acc_num, username, password_hash, balance = line.strip().split("|")
#                 accounts[acc_num] = {"username": username, "password": password_hash, "balance": float(balance)}
#     return accounts

# def load_customers():
#     customers = {}
#     if os.path.exists(CUSTOMER_FILE):
#         with open(CUSTOMER_FILE, "r") as f:
#             for line in f:
#                 username, acc_num, nic, contact = line.strip().split("|")
#                 customers[username] = {"account_number": acc_num, "nic": nic, "contact": contact}
#     return customers

# # Save data to files
# def save_user(username, role, balance):
#     with open(USERS_FILE, "a") as f:
#         f.write(f"{username}|{role}|{balance}\n")

# def save_account(acc_num, username, password_hash, balance):
#     with open(BANK_ACCOUNT_FILE, "a") as f:
#         f.write(f"{acc_num}|{username}|{password_hash}|{balance}\n")

# def save_customer(username, acc_num, nic, contact):
#     with open(CUSTOMER_FILE, "a") as f:
#         f.write(f"{username}|{acc_num}|{nic}|{contact}\n")

# def record_transaction(acc_num, action, last_balance, amount, new_balance):
#     with open(TRANSACTIONS_FILE, "a") as f:
#         f.write(f"{acc_num}|{get_current_datetime()}|{action}|{last_balance}|{amount}|{new_balance}\n")

# # Admin functionalities
# def admin_menu():
#     while True:
#         print("\n--- Admin Menu ---")
#         print("1. Create Customer Account")
#         print("2. Deposit to Customer Account")
#         print("3. Withdraw from Customer Account")
#         print("4. Logout")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             create_customer_account()
#         elif choice == "2":
#             modify_balance("deposit")
#         elif choice == "3":
#             modify_balance("withdraw")
#         elif choice == "4":
#             break
#         else:
#             print("Invalid choice.")

# def create_customer_account():
#     print("\n--- Create Customer Account ---")
#     username = input("Enter username: ")
#     password = pwinput.pwinput("Enter password: ")
#     nic = input("Enter NIC number: ")
#     contact = input("Enter contact number: ")
#     try:
#         balance = float(input("Enter initial balance: "))
#     except ValueError:
#         print("Invalid balance amount.")
#         return

#     acc_num = generate_account_number()
#     password_hash = hash_password(password)

#     save_account(acc_num, username, password_hash, balance)
#     save_customer(username, acc_num, nic, contact)
#     save_user(username, "customer", balance)
#     record_transaction(acc_num, "Account Created", 0.0, balance, balance)
#     print(f"Customer account created successfully. Account Number: {acc_num}")

# def modify_balance(action):
#     acc_num = input("Enter account number: ")
#     accounts = load_accounts()
#     if acc_num not in accounts:
#         print("Account not found.")
#         return
#     try:
#         amount = float(input(f"Enter amount to {action}: "))
#     except ValueError:
#         print("Invalid amount.")
#         return

#     last_balance = accounts[acc_num]["balance"]
#     if action == "deposit":
#         new_balance = last_balance + amount
#     elif action == "withdraw":
#         if amount > last_balance:
#             print("Insufficient funds.")
#             return
#         new_balance = last_balance - amount
#     else:
#         print("Invalid action.")
#         return

#     # Update account balance
#     accounts[acc_num]["balance"] = new_balance
#     # Rewrite BANK_ACCOUNT_FILE
#     with open(BANK_ACCOUNT_FILE, "w") as f:
#         for acc, info in accounts.items():
#             f.write(f"{acc}|{info['username']}|{info['password']}|{info['balance']}\n")
#     # Update USERS_FILE
#     users = load_users()
#     username = accounts[acc_num]["username"]
#     users[username]["balance"] = new_balance
#     with open(USERS_FILE, "w") as f:
#         for user, info in users.items():
#             f.write(f"{user}|{info['role']}|{info['balance']}\n")
#     # Record transaction
#     record_transaction(acc_num, action.capitalize(), last_balance, amount, new_balance)
#     print(f"{action.capitalize()} successful. New balance: {new_balance}")

# # User functionalities
# def user_menu(username):
#     accounts = load_accounts()
#     user_acc_num = None
#     for acc_num, info in accounts.items():
#         if info["username"] == username:
#             user_acc_num = acc_num
#             break
#     if not user_acc_num:
#         print("Account not found.")
#         return

#     while True:
#         print("\n--- User Menu ---")
#         print("1. Deposit")
#         print("2. Withdraw")
#         print("3. Check Balance")
#         print("4. View Transaction History")
#         print("5. Logout")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             user_deposit(user_acc_num)
#         elif choice == "2":
#             user_withdraw(user_acc_num)
#         elif choice == "3":
#             print(f"Current balance: {accounts[user_acc_num]['balance']}")
#         elif choice == "4":
#             view_transactions(user_acc_num)
#         elif choice == "5":
#             break
#         else:
#             print("Invalid choice.")

# def user_deposit(acc_num):
#     accounts = load_accounts()
#     try:
#         amount = float(input("Enter amount to deposit: "))
#     except ValueError:
#         print("Invalid amount.")
#         return
#     last_balance = accounts[acc_num]["balance"]
#     new_balance = last_balance + amount
#     accounts[acc_num]["balance"] = new_balance
#     # Update files
#     with open(BANK_ACCOUNT_FILE, "w") as f:
#         for acc, info in accounts.items():
#             f.write(f"{acc}|{info['username']}|{info['password']}|{info['balance']}\n")
#     users = load_users()
#     username = accounts[acc_num]["username"]
#     users[username]["balance"] = new_balance
#     with open(USERS_FILE, "w") as f:
#         for user, info in users.items():
#             f.write(f"{user}|{info['role']}|{info['balance']}\n")
#     record_transaction(acc_num, "Deposit", last_balance, amount, new_balance)
#     print(f"Deposit successful. New balance: {new_balance}")

# def user_withdraw(acc_num):
#     accounts = load_accounts()
#     try:
#         amount = float(input("Enter amount to withdraw: "))
#     except ValueError:
#         print("Invalid amount.")
#         return
#     last_balance = accounts[acc_num]["balance"]
#     if amount > last_balance:
#         print("Insufficient funds.")
#         return
#     new_balance = last_balance - amount
#     accounts[acc_num]["balance"] = new_balance
#     # Update files
#     with open(BANK_ACCOUNT_FILE, "w") as f:
#         for acc, info in accounts.items():
#             f.write(f"{acc}|{info['username']}|{info['password']}|{info['balance']}\n")
#     users = load_users()
#     username = accounts[acc_num]["username"]
#     users[username]["balance"] = new_balance
#     with open(USERS_FILE, "w") as f:
#         for user, info in users.items():
#             f.write(f"{user}|{info['role']}|{info['balance']}\n")
#     record_transaction(acc_num, "Withdraw", last_balance, amount, new_balance)
#     print(f"Withdrawal successful. New balance: {new_balance}")

# def view_transactions(acc_num):
#     if not os.path.exists(TRANSACTIONS_FILE):
#         print("No transactions found.")
#         return
#     with open(TRANSACTIONS_FILE, "r") as f:
#         for line in f:
#             record = line.strip().split("|")
#             if record[0] == acc_num:
#                 print(" | ".join(record))

# # Authentication
# def login():
#     users = load_users()
#     username = input("Enter username: ")
#     password = pwinput.pwinput("Enter password: ")
#     accounts = load_accounts()
#     acc_num = None
#     for acc, info in accounts.items():
#         if info["username"] == username:
#             acc_num = acc
#             stored_password = info["password"]
#             break
#     if not acc_num:
#         print("User not found.")
#         return
#         if hash_password(password) != stored_password:
#             print("Incorrect password.")
#         return

#     role = users[username]["role"]
#     print(f"Login successful! Logged in as {role.capitalize()}")
#     if role == "admin":
#         admin_menu()
#     else:
#         user_menu(username)

# # Entry point
# def main():
#     while True:
#         print("\n--- Welcome to the Simple Banking System ---")
#         print("1. Login")
#         print("2. Exit")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             login()
#         elif choice == "2":
#             print("Thank you for using the system. Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main()

 


# Simplified and updated version
import datetime
import hashlib
import pwinput

# File paths
ACCOUNT_FILE = "Bank_Account.txt"
CUSTOMER_FILE = "Customer.txt"
USERS_FILE = "Users.txt"
TRANSACTION_FILE = "Transactions.txt"

accounts = {}
users = {}

# --- Utility Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- File I/O ---
def load_data():
    try:
        with open(ACCOUNT_FILE, "r") as f:
            for line in f:
                acc_num, username, password, balance = line.strip().split("|")
                accounts[username] = {
                    'account_number': acc_num,
                    'password': password,
                    'balance': float(balance)
                }
    except FileNotFoundError:
        pass

    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                username, role, balance = line.strip().split("|")
                users[username] = {
                    'role': role,
                    'balance': float(balance)
                }
    except FileNotFoundError:
        pass

def save_data():
    with open(ACCOUNT_FILE, "w") as f:
        for username, info in accounts.items():
            f.write(f"{info['account_number']}|{username}|{info['password']}|{info['balance']}\n")

    with open(USERS_FILE, "w") as f:
        for username, info in users.items():
            f.write(f"{username}|{info['role']}|{info['balance']}\n")

def append_customer(username, acc_num, nic, contact):
    with open(CUSTOMER_FILE, "a") as f:
        f.write(f"{username}|{acc_num}|{nic}|{contact}\n")

def record_transaction(acc_num, action, last_balance, amount, new_balance):
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{acc_num}|{get_current_datetime()}|{action}|{last_balance}|{amount}|{new_balance}\n")

# --- Core Functionalities ---
def generate_account_number():
    return f"AC{1000 + len(accounts)}"

def create_customer():
    print("\n--- Create New Customer Account ---")
    username = input("Username: ")
    if username in accounts:
        print("❌ Username already exists.")
        return

    password = pwinput.pwinput("Password: ")
    nic = input("NIC Number: ")
    contact = input("Contact Number: ")
    try:
        balance = float(input("Initial Balance: "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    acc_num = generate_account_number()
    hashed_pw = hash_password(password)

    accounts[username] = {'account_number': acc_num, 'password': hashed_pw, 'balance': balance}
    users[username] = {'role': 'customer', 'balance': balance}

    save_data()
    append_customer(username, acc_num, nic, contact)
    record_transaction(acc_num, "Account Created", 0, balance, balance)
    print(f"✅ Customer account created. Account No: {acc_num}")

def deposit_to_account():
    acc_num = input("Enter account number: ")
    amount = float(input("Enter amount to deposit: "))

    for username, info in accounts.items():
        if info['account_number'] == acc_num:
            last = info['balance']
            info['balance'] += amount
            users[username]['balance'] = info['balance']
            save_data()
            record_transaction(acc_num, "Deposit", last, amount, info['balance'])
            print("✅ Deposit successful.")
            return

    print("❌ Account not found.")

def withdraw_from_account():
    acc_num = input("Enter account number: ")
    amount = float(input("Enter amount to withdraw: "))

    for username, info in accounts.items():
        if info['account_number'] == acc_num:
            if info['balance'] < amount:
                print("❌ Insufficient funds.")
                return
            last = info['balance']
            info['balance'] -= amount
            users[username]['balance'] = info['balance']
            save_data()
            record_transaction(acc_num, "Withdraw", last, amount, info['balance'])
            print("✅ Withdrawal successful.")
            return

    print("❌ Account not found.")

# --- Menus ---
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Customer")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            create_customer()
        elif choice == '2':
            deposit_to_account()
        elif choice == '3':
            withdraw_from_account()
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice.")

def login():
    username = input("Username: ")
    password = pwinput.pwinput("Password: ")

    if username in accounts and check_password(password, accounts[username]['password']):
        if users[username]['role'] == 'admin':
            admin_menu()
        else:
            print("✅ Customer login successful. Limited access.")
    else:
        print("❌ Login failed.")

# --- Main ---
def main():
    load_data()
    if not users:
        print("🔐 No users found. Creating admin account...")
        username = input("Set admin username: ")
        password = pwinput.pwinput("Set admin password: ")
        acc_num = generate_account_number()
        hashed_pw = hash_password(password)
        accounts[username] = {'account_number': acc_num, 'password': hashed_pw}
        users[username] = {'role': 'admin'}
        save_data()
        print("✅ Admin created. Please login.")

    while True:
        print("\n=== Welcome to Secure Banking ===")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            login()
        elif choice == '2':
            break
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()
