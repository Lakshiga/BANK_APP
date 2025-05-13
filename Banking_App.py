import os
import re
import time
import random
from datetime import datetime
import pwinput
import hashlib

ACCOUNT_FILE = "Bank_Account.txt"
CUSTOMER_FILE = "Customer.txt"
USER_FILE = "Users.txt"
TRANSACTION_FILE = "Transactions.txt"

def generate_account_number():
    return str(random.randint(10000, 99999))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, stored_password_hash):
    return hash_password(input_password) == stored_password_hash

def encrypt_password(password):
    return "*" * len(password) 

def write_to_file(filename, data):
    with open(filename, 'a') as f:
        f.write(data + '\n')

def generate_user_id():
    existing = read_file(USER_FILE)
    return f"U_{1000 + len(existing) + 1}"

def generate_customer_id():
    existing = read_file(CUSTOMER_FILE)
    return f"C_{10000 + len(existing) + 1}"

def read_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def save_all_lines(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line + '\n')

# def first_login():
#     print("=== First Time Admin Setup ===")
#     username = input("Enter admin username: ")
#     password = pwinput.pwinput("Enter admin password: ")
#     write_to_file(USER_FILE, f"{username}||admin||{hash_password(password)}")
#     print("✅ Admin created successfully.")
#     return username, "admin"


def first_login():
    print("=== First Time Admin Setup ===")
    username = input("Enter admin username: ")

    while True:
        password = pwinput.pwinput("Enter admin password (At least 8 characters with uppercase, lowercase, number, symbol): ")
        if is_valid_password(password):
            break
        print("❌ Invalid password. It must include uppercase, lowercase, number, and special character.")

    write_to_file(USER_FILE, f"{username}||admin||{hash_password(password)}")
    print("✅ Admin created successfully.")
    return username, "admin"


def login():
    users = read_file(USER_FILE)
    if not users:
        return first_login()

    print("=== Login ===")
    username = input("Enter Your Username: ")
    password = pwinput.pwinput("Enter your Password: ")

    for user in users:
        parts = user.strip().split('||')
        if len(parts) == 3:
            uname, role, passwd = parts
        elif len(parts) == 4:
            _, uname, role, passwd = parts 
        elif len(parts) == 5:
            _, _, uname, role, passwd = parts
        else:
            continue 

        if uname == username and passwd == hash_password(password):
            print("✅ Login successful !")
            return uname, role

    print("❌ Invalid credentials.")
    return login()


def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[\W_]', password) 
    )

def is_valid_nic(nic):
    """Validate NIC number format"""
    return len(nic) >= 5

def is_valid_phone(phone):
    return re.fullmatch(r'07\d{8}', phone)

def create_customer():
    print("=== Create Customer Account ===")

    users = read_file(USER_FILE)
    existing_usernames = {user.strip().split('||')[1] for user in users if len(user.strip().split('||')) >= 2}

    while True:
        username = input("Enter your username: ")
        if username in existing_usernames:
            print("❌ Username already exists. Try a different one.")
        elif username.strip() == "":
            print("❌ Username cannot be empty.")
        else:
            break

    while True:
        password = pwinput.pwinput("Set password (At least 8 characters with uppercase, lowercase, number, symbol): ")
        if not is_valid_password(password):
            print("❌ Invalid password. It must include uppercase, lowercase, number, and special character.")
        else:
            break

    while True:
        try:
            balance = float(input("Enter initial balance (>= 0): "))
            if balance < 0:
                print("❌ Balance cannot be negative.")
            else:
                break
        except ValueError:
            print("❌ Invalid number. Please enter a valid amount.")

    while True:
        nic = input("Enter NIC No: ")
        if not is_valid_nic(nic):
            print("❌ Invalid NIC number. Must be more than 5 digits.")
        else:
            break

    while True:
        contact = input("Enter Contact No: ")
        if not is_valid_phone(contact):
            print("❌ Invalid phone number. Must be 10 digits.")
        else:
            break

    account_number = generate_account_number()
    user_id = generate_user_id()
    customer_id = generate_customer_id()

    write_to_file(ACCOUNT_FILE, f"{account_number}||{username}||{hash_password(password)}||{balance}")
    write_to_file(CUSTOMER_FILE, f"{customer_id}||{username}||{account_number}||{nic}||{contact}")
    write_to_file(USER_FILE, f"{user_id}||{account_number}||{username}||user||{hash_password(password)}")

    print(f"✅ Successful Customer created!")
    print(f"🆔 User ID: {user_id}")
    print(f"🏦 Account Number: {account_number}")
    print(f"👤 Customer ID: {customer_id}")

def find_account(account_number):
    accounts = read_file(ACCOUNT_FILE)
    for acc in accounts:
        acc_no, uname, passwd, bal = acc.split('||')
        if acc_no == account_number:
            return acc_no, uname, passwd, float(bal)
    return None  

def update_account(account_number, new_balance):
    accounts = read_file(ACCOUNT_FILE)
    updated = []
    for acc in accounts:
        acc_no, uname, passwd = acc.split('||')
        if acc_no == account_number:
            updated.append(f"{acc_no}||{uname}||{passwd}||{new_balance}")
        else:
            updated.append(acc)
    save_all_lines(ACCOUNT_FILE, updated)

def record_transaction(account_number, action, last_bal, new_bal):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_to_file(TRANSACTION_FILE, f"{account_number}||{dt}||{action}||{last_bal}||{new_bal}")

def deposit(account_number):
    acc = find_account(account_number)
    if not acc:
        print("❌ Account not found.")
        return
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("❌ Invalid amount.")
            return
    except:
        print("❌ Invalid input.")
        return

    new_balance = acc[3] + amount
    update_account(account_number, new_balance)
    record_transaction(account_number, "deposit", acc[3], new_balance)
    print(f"✅ Deposit successful. Amount: {amount}, Your current balance is: {new_balance}.")

def withdraw(account_number):
    acc = find_account(account_number)
    if not acc:
        print("❌ Account not found.")
        return
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0 or amount > acc[3]:
            print("❌ Insufficient amount.")
            return
    except:
        print("❌ Invalid input.")
        return

    new_balance = acc[3] - amount
    update_account(account_number, new_balance)
    record_transaction(account_number, "withdraw", acc[3], new_balance)
    print(f"✅ Withdrawal successful. Amount: {amount}, Your current balance is: {new_balance}.")

def fund_transfer():
    sender_acc = input("Enter your account number: ")
    receiver_acc = input("Enter recipient account number: ")
    amount = float(input("Enter amount to transfer: "))

    accounts = read_file(ACCOUNT_FILE)
    updated_accounts = []
    sender_found = False
    receiver_found = False
    sender_balance = 0
    receiver_balance = 0

    for acc in accounts:
        parts = acc.strip().split('||')
        acc_no = parts[0]

        try:
            balance = float(parts[3])
        except (IndexError, ValueError):
            print(f"❌ Error reading balance for account {acc_no}. Skipping.")
            updated_accounts.append(acc)
            continue

        if acc_no == sender_acc:
            sender_found = True
            sender_balance = balance
            if balance < amount:
                print("❌ Insufficient funds.")
                return
            balance -= amount
            parts[3] = str(balance)

        elif acc_no == receiver_acc:
            receiver_found = True
            receiver_balance = balance
            balance += amount
            parts[3] = str(balance)

        updated_accounts.append('||'.join(parts))

    if not sender_found:
        print("❌ Sender account not found.")
        return
    if not receiver_found:
        print("❌ Receiver account not found.")
        return

    save_all_lines(ACCOUNT_FILE, updated_accounts)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    transaction_log = [
        f"{sender_acc}||Transfer Out||{amount}||{receiver_acc}||{timestamp}||Current Balance: {sender_balance - amount}",
        f"{receiver_acc}||Transfer In||{amount}||{sender_acc}||{timestamp}||Current Balance: {receiver_balance + amount}"
    ]
    
    with open(TRANSACTION_FILE, 'a') as f:
        for log in transaction_log:
            f.write(log + '\n')

    print("✅ Transfer successful.")


def check_balance(account_number):
    acc = find_account(account_number)
    if acc:
        print(f"Current Balance: {acc[3]}")
    else:
        print("❌ Account not found.")

def reset_password():
    account_number = input("Enter your account number: ")
    current_password = pwinput.pwinput("Enter your current password: ")
    current_password_hashed = hash_password(current_password)

    accounts = read_file(ACCOUNT_FILE)
    updated_accounts = []
    account_found = False
    user_name = None  

    for acc in accounts:
        parts = acc.strip().split('||')
        if len(parts) != 4:
            updated_accounts.append(acc.strip())
            continue

        acc_no, name, stored_password, balance = parts

        if acc_no == account_number and stored_password == current_password_hashed:
            account_found = True
            user_name = name
            new_password = pwinput.pwinput("Enter new password: ")
            confirm_password = pwinput.pwinput("Confirm new password: ")
            if new_password != confirm_password:
                print("❌ Passwords do not match.")
                return
            new_password_hashed = hash_password(new_password)
            updated_line = f"{acc_no}||{name}||{new_password_hashed}||{balance}"
            updated_accounts.append(updated_line)
            print("✅ Password updated successfully.")
        else:
            updated_accounts.append(acc.strip())

    if not account_found:
        print("❌ Incorrect account number or password.")
        return

    save_all_lines(ACCOUNT_FILE, updated_accounts)

   
    if user_name:
        users = read_file(USER_FILE)
        updated_users = []

        for user in users:
            parts = user.strip().split('||')
            if len(parts) == 3:
                uname, role, passwd = parts
                if uname == user_name:
                    passwd = new_password_hashed
                updated_users.append(f"{uname}||{role}||{passwd}")
            elif len(parts) == 4:
                _, uname, role, passwd = parts
                if uname == user_name:
                    passwd = new_password_hashed
                updated_users.append(f"{account_number}||{uname}||{role}||{passwd}")
            elif len(parts) == 5:
                _, _, uname, role, passwd = parts
                if uname == user_name:
                    passwd = new_password_hashed
                updated_users.append(f"{account_number}||--||{uname}||{role}||{passwd}")
            else:
                updated_users.append(user.strip())

        save_all_lines(USER_FILE, updated_users)

def transaction_history(account_number):
    print(f"=== Transactions for {account_number} ===")
    transactions = read_file(TRANSACTION_FILE)
    for tx in transactions:
        acc_no, dt, act, last_b, cur_b = tx.split('||')
        if acc_no == account_number:
            print(f"{dt} || {act} || Last: {last_b} || Current: {cur_b}")

def search_details():
    print("Search by typing:")
    print(" - Full or partial account number (e.g., 10001)")
    print(" - A date (e.g., 2025-05-06) & A time (e.g., 09:30)")
    print(" - Action type: 'deposit' or 'withdraw'")
    
    keyword = input("Enter your search keyword: ").lower()
    transactions = read_file(TRANSACTION_FILE)
    accounts = read_file(CUSTOMER_FILE)
    found = False

    matched_accounts = []
    for acc in accounts:
        cust_id, uname, acc_number, nic, phone = acc.strip().split('||')
        if keyword in acc_number.lower():
            matched_accounts.append(acc_number)
            print("\n--- Account Details ---")
            print(f"Customer ID   : {cust_id}")
            print(f"Username      : {uname}")
            print(f"Account Number: {acc_number}")
            print(f"NIC No        : {nic}")
            print(f"Phone No      : {phone}")
            print("\n--- Transaction History ---")

    for tx in transactions:
        acc_no, dt, act, last_b, cur_b = tx.strip().split('||')
        if (keyword in acc_no.lower() or keyword in dt.lower() or keyword in act.lower()):
            print(f"{dt} || {act} || Account: {acc_no} || Last: {last_b} || Current: {cur_b}")
            found = True
        elif acc_no in matched_accounts:
            print(f"{dt} || {act} || Account: {acc_no} || Last: {last_b} || Current: {cur_b}")
            found = True

    if not found:
        print("❌ No transactions matched your search.")

def view_all_accounts():
    accounts = read_file(ACCOUNT_FILE)
    for acc in accounts:
        print(acc)

def manage_accounts():
    print("1. Delete Account\n2. Update Account Username")
    choice = input("Choice: ")
    if choice == '1':
        acc_no = input("Enter account number to delete: ")
         
        files_to_clean = [ACCOUNT_FILE, CUSTOMER_FILE, USER_FILE, TRANSACTION_FILE]

        for file in files_to_clean:
            lines = read_file(file)
            updated_lines = [line for line in lines if acc_no not in line]
            save_all_lines(file, updated_lines)
        print("✅ Successfully deleted account and all associated data.")


    elif choice == '2':
        acc_no = input("Enter account number to update: ")
        new_name = input("Enter new username: ")
        updated = []
        for acc in read_file(ACCOUNT_FILE):
            parts = acc.split('||')
            if parts[0] == acc_no:
                parts[1] = new_name
            updated.append('||'.join(parts))
        save_all_lines(ACCOUNT_FILE, updated)
        print("✅ Successful Username updated.")


def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Create Customer Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Money Transfer")
        print("5. Check Balance")
        print("6. Transaction History")
        print("7. Manage Accounts")
        print("8. View All Accounts")
        print("9. Search Details")
        print("10. Logout")
        choice = input("Choice: ")
        if choice == '1': create_customer()
        elif choice == '2': deposit(input("Enter account number: "))
        elif choice == '3': withdraw(input("Enter account number: "))
        elif choice == '4': fund_transfer()
        elif choice == '5': check_balance(input("Enter account number: "))
        elif choice == '6': transaction_history(input("Enter account number: "))
        elif choice == '7': manage_accounts()
        elif choice == '8': view_all_accounts()
        elif choice == '9': search_details()
        elif choice == '10': break
        else: print("❌ Invalid option.")

def user_menu(username):
    acc_no = None
    accounts = read_file(ACCOUNT_FILE)
    for acc in accounts:
        acc_number, uname, _, _ = acc.split('||')
        if uname == username:
            acc_no = acc_number
            break
    if not acc_no:
        print("❌ No account found for user.")
        return

    while True:
        print("\n=== User Menu ===")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Money Transfer")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Reset Password")
        print("7. Logout")
        print("8. Exit")
        choice = input("Choice: ")
        
        if choice == '1':
            deposit(acc_no)
        elif choice == '2':
            withdraw(acc_no)
        elif choice == '3':
            check_balance(acc_no)
        elif choice == '4':
            fund_transfer()
        elif choice == '5':
            transaction_history(acc_no)
        elif choice == '6':
            reset_password()
        elif choice == '7':
            break 
        elif choice == '8':
            print("👋 Thank you , Exiting the application. Goodbye!")
            exit() 
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    while True:
        username, role = login()
        if role == 'admin':
            admin_menu()
        else:
            user_menu(username)

