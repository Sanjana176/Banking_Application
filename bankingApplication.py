from decimal import Decimal 
import mysql.connector      
import random               
import re
from datetime import datetime

# Connect to MySQL database
def connect_to_database():   
    try:
        connection = mysql.connector.connect(  
            host="localhost",
            port="3306",
            user="root",
            password="Sanj@2001",
            database="Banking_db"
        )
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

def validate_aadhar(aadhar):
    # Aadhar should be 12 digits
    if not re.match(r'^\d{12}$', aadhar):
        return False
    return True

'''def validate_mobile(mobile):
    # Mobile number should be 10 digits
    if not re.match(r'^\d{10}$', mobile):
        return False
    return True'''
def validate_mobile(mobile):
    # Mobile number should be 10 digits and should not start with 0
    if not re.match(r'^[1-9]\d{9}$', mobile):
        return False
    return True



def validate_username(username):
    # Username should not include special characters, should not contain integers, and should be limited to 15 characters per name
    if not re.match(r'^[a-zA-Z ]{1,15}(?: [a-zA-Z ]{1,15})?$', username):
        return False
    return True


def validate_account_number(account_number):
    # Account number should be exactly 12 digits and contain only numbers
    if not re.match(r'^\d{12}$', account_number):
        return False
    return True

def validate_password(password):
    # Password should be at least 8 characters long, contain at least one special character, and not contain any spaces
    if len(password) < 8:
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    if ' ' in password:
        return False
    return True

def mobile_number_exists(cursor, mobile):  
    query = "SELECT COUNT(*) FROM Users WHERE mobile = %s"
    cursor.execute(query, (mobile,))
    count = cursor.fetchone()[0]
    return count > 0

def username_exists(cursor, username):
    query = "SELECT COUNT(*) FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    count = cursor.fetchone()[0]
    return count > 0

# Function to display account info and balance
def display_account_info(cursor, user_id):   
    query = "SELECT * FROM Accounts WHERE user_id = %s"  
    cursor.execute(query, (user_id,))      
    account_info = cursor.fetchone()      
    if account_info:
        print("Account Info:")
        print("Account Number:", account_info[0])
        print("Balance:", account_info[2])
    else:
        print("Account not found.")

def add_funds(cursor, connection, user_id):
    try:
        # Get the current balance of the user's account
        query = "SELECT balance FROM Accounts WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        current_balance = cursor.fetchone()[0]

        # Prompt the user to enter the amount to add
        amount_to_add = Decimal(input("Enter the amount to add: "))
        
        # Validate the amount (must be positive)
        if amount_to_add <= 0:
            print("Invalid amount. Please enter a positive value.")
            return

        # Update the balance in the database
        new_balance = current_balance + amount_to_add
        update_query = "UPDATE Accounts SET balance = %s WHERE user_id = %s"
        cursor.execute(update_query, (new_balance, user_id))
        connection.commit()

        print("Funds added successfully.")
        print("New balance:", new_balance)
    
    except mysql.connector.Error as e:
        connection.rollback()  # Roll back the transaction in case of error
        print("Error adding funds:", e)

# Function to display list of beneficiaries
def list_beneficiaries(cursor, user_id):
    query = "SELECT * FROM Beneficiaries WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    beneficiaries = cursor.fetchall()     #This line fetches all rows of the result of the executed query.
    if beneficiaries:
        print("List of Beneficiaries:")
        for beneficiary in beneficiaries:
            print("Name:", beneficiary[2])
            print("Account Number:", beneficiary[3])
            print("Bank Name:", beneficiary[4])
    else:
        print("No beneficiaries found.")

# Function to display list of cards
def list_cards(cursor, user_id):
    query = "SELECT * FROM Cards WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    cards = cursor.fetchall()
    if cards:
        print("List of Cards:")
        for card in cards:
            print("Card Type:", card[2])
            print("Card Number:", card[3])
            print("PIN:", card[4])
            print("CVV:", card[5])
    else:
        print("No cards found.")

# Function to add beneficiary
def add_beneficiary(cursor, connection, user_id):
    beneficiary_name = input("Enter beneficiary name: ")
    while True:
        account_number = input("Enter account number: ")
        if not validate_account_number(account_number):
            print("Invalid account number. Account number should be exactly 12 digits and contain only numbers.")
            continue
        else:
            break
    
    # Check if the beneficiary account number already exists for this user
    query = "SELECT COUNT(*) FROM Beneficiaries WHERE user_id = %s AND account_number = %s"
    cursor.execute(query, (user_id, account_number))
    count = cursor.fetchone()[0]
    if count > 0:
        print("Beneficiary with this account number already exists for this user.")
        return
    
    bank_name = input("Enter bank name: ")
    query = "INSERT INTO Beneficiaries (user_id, beneficiary_name, account_number, bank_name) VALUES (%s, %s, %s, %s)"
    data = (user_id, beneficiary_name, account_number, bank_name)
    cursor.execute(query, data)
    connection.commit()
    print("Beneficiary added successfully.")
    
# Function to update account info

def update_account_info(cursor, connection, user_id):
    new_address = input("Enter new address: ")
    
    while True:
        new_mobile = input("Enter new mobile number: ")
        if not validate_mobile(new_mobile):
            print("Invalid mobile number. Mobile number should be 10 digits exact and only numbers.")
            continue
        else:
            break
    
    query = "UPDATE Users SET address = %s, mobile = %s WHERE id = %s"
    data = (new_address, new_mobile, user_id)
    cursor.execute(query, data)
    connection.commit()
    print("Account info updated successfully.")
    query = "SELECT * FROM Users WHERE id = %s"
    cursor.execute(query, (user_id,))
    account_info = cursor.fetchone()
    if account_info:
        print("Updated Account Details:")
        print("Address:", account_info[2])
        print("Mobile:", account_info[4])
    else:
        print("Account not found.")
# Function to transfer funds
def transfer_funds(cursor, connection, user_id):
    beneficiary_number = input("Enter beneficiary account number: ")
    amount = Decimal(input("Enter amount to transfer: "))  # Convert amount to Decimal
    if amount <= 0:
            print("Invalid amount. Please enter a positive value.")
            return

    # Check if the beneficiary account exists in the Beneficiaries table
    query = "SELECT * FROM Beneficiaries WHERE user_id = %s AND account_number = %s"
    cursor.execute(query, (user_id, beneficiary_number))
    beneficiary = cursor.fetchone()
    if not beneficiary:
        print("Beneficiary account not found. Please add the beneficiary first.")
        return

    # Check if the user has sufficient balance
    query = "SELECT balance FROM Accounts WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    sender_balance = cursor.fetchone()[0]
    if sender_balance < amount:
        print("Insufficient balance. Transaction aborted.")
        return

    # Consume any unread results before executing the update query
    cursor.fetchall()

    # Deduct the transferred amount from the sender's account balance
    new_sender_balance = sender_balance - amount
    update_sender_query = "UPDATE Accounts SET balance = %s WHERE user_id = %s"
    cursor.execute(update_sender_query, (new_sender_balance, user_id))
    connection.commit()  # Consume the result

    # Add the transferred amount to the beneficiary's account balance
    update_beneficiary_query = "UPDATE Accounts SET balance = balance + %s WHERE user_id = %s"
    cursor.execute(update_beneficiary_query, (amount, beneficiary[0]))

    # Insert transaction record
    insert_transaction_query = "INSERT INTO Transactions (sender_id, beneficiary_id, amount) VALUES (%s, %s, %s)"
    cursor.execute(insert_transaction_query, (user_id, beneficiary[0], amount))

    connection.commit()
    print("Funds transferred successfully.")



def view_transactions(cursor, user_id):
    try:
        # SQL query to fetch transaction details along with sender and beneficiary names for a specific user
        query = """
        SELECT t.transaction_id, u1.username AS sender_name, b.beneficiary_name,
               t.amount, t.transaction_date
        FROM Transactions t
        INNER JOIN Users u1 ON t.sender_id = u1.id
        INNER JOIN Beneficiaries b ON t.beneficiary_id = b.id
        WHERE t.sender_id = %s OR t.beneficiary_id = %s
        """
        
        # Execute the query with user_id as parameter
        cursor.execute(query, (user_id, user_id))
        
        # Fetch all rows
        transactions = cursor.fetchall()
        
        # Check if transactions are found
        if not transactions:
            print("No transactions found.")
        else:
            # Print column headers
            print("{:<15} {:<20} {:<20} {:<10} {:<25}".format(
                "Transaction ID", "Sender Name", "Beneficiary Name", "Amount", "Transaction Date"))
            print("="*90)
            
            # Print each transaction
            for transaction in transactions:
                # Determine if the user is the sender or beneficiary
                if transaction[1] == user_id:  # User is the sender
                    user_role = "Sender"
                else:  # User is the beneficiary
                    user_role = "Beneficiary"
                
                # Format the transaction date
                transaction_date = transaction[4].strftime("%Y-%m-%d %H:%M:%S")
                
                print("{:<15} {:<20} {:<20} {:<10} {:<25}".format(
                    transaction[0], transaction[1], transaction[2], transaction[3], transaction_date))
    
    except mysql.connector.Error as err:
        print("Error:", err)





# Function to change MPIN

def change_mpin(cursor, connection):
    card_number = input("Enter card number: ")

    # Check if the card exists in the database
    query = "SELECT * FROM Cards WHERE card_number = %s"
    cursor.execute(query, (card_number,))
    card = cursor.fetchone()

    if not card:
        print("Card not found. Please enter valid card details.")
        return

    while True:
        new_pin = input("Enter new PIN: ")
        if len(new_pin) != 4:
            print("Please enter 4 digit PIN.")
            continue

        # Ensure PIN consists of only digits
        if not new_pin.isdigit():
            print("Invalid PIN. Please enter only digits.")
            continue

        break

    while True:
        new_cvv = input("Enter new CVV: ")
        if len(new_cvv) != 3:
            print("IPlease enter 3 digit CVV.")
            continue

        # Ensure CVV consists of only digits
        if not new_cvv.isdigit():
            print("Invalid CVV. Please enter only digits.")
            continue

        break

    # Update the MPIN
    query = "UPDATE Cards SET pin = %s, cvv = %s WHERE card_number = %s"
    data = (new_pin, new_cvv, card_number)
    cursor.execute(query, data)
    connection.commit()
    print("MPIN changed successfully.")

#function to check if a card already exists
def card_number_exists(card_number):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Cards WHERE card_number = %s"
        cursor.execute(query, (card_number,))
        count = cursor.fetchone()[0]

        return count > 0
    
    except mysql.connector.Error as e:
        print("Error checking card number:", e)
        return False
    
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to register new credit card

def register_new_credit_card(cursor, connection, user_id):
    try:
        # Input validation for card number
        while True:
            card_number = input("Enter card number: ")
            if len(card_number) == 12 and card_number.isdigit():
                break
            else:
                print("Invalid card number. Please enter a 12-digit number.")

        # Input validation for card type
        while True:
            card_type = input("Enter card type (debit/credit): ").lower()
            if card_type in ['debit', 'credit']:
                break
            else:
                print("Invalid card type. Please enter either 'debit' or 'credit'.")

        # Input validation for CVV
        while True:
            cvv = input("Enter CVV: ")
            if len(cvv) == 3 and cvv.isdigit():
                break
            else:
                print("Invalid CVV. Please enter a 3-digit number.")

        # Input validation for PIN
        while True:
            pin = input("Enter PIN: ")
            if len(pin) == 4 and pin.isdigit():
                break
            else:
                print("Invalid PIN. Please enter a 4-digit number.")

        # Check if the card number already exists in the database
        if card_number_exists(card_number):
            print("Card already registered.")
            return
        
        # Insert the new credit card details into the 'Cards' table
        credit_card_query = "INSERT INTO Cards (user_id, card_type, card_number, pin, cvv) VALUES (%s, %s, %s, %s, %s)"
        credit_card_data = (user_id, card_type, card_number, pin, cvv)
        cursor.execute(credit_card_query, credit_card_data)
        connection.commit()
        print("New credit card registered successfully.")
    
    except mysql.connector.Error as e:
        print("Error registering new credit card:", e)

# Function to generate a random 12-digit card number
def generate_card_number():
    while True:
        card_number = ''.join(str(random.randint(0, 9)) for _ in range(12))
        if not card_number_exists(card_number):
            return card_number

def generate_cvv():
    return ''.join(str(random.randint(0, 9)) for _ in range(3))

def generate_pin():
    return ''.join(str(random.randint(0, 9)) for _ in range(4))

# Function to check if a CVV already exists in the database
def cvv_exists(cvv):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Cards WHERE cvv = %s"
        cursor.execute(query, (cvv,))
        count = cursor.fetchone()[0]

        return count > 0
    
    except mysql.connector.Error as e:
        print("Error checking CVV:", e)
        return False
    
    finally:
        if connection:
            cursor.close()
            connection.close()

def generate_account_number():
    while True:
        # Generate a 12-digit account number
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(12))
        
        # Check if the generated account number already exists in the database
        if not account_number_exists(account_number):
            return account_number

def account_number_exists(account_number):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Accounts WHERE account_number = %s"
        cursor.execute(query, (account_number,))
        count = cursor.fetchone()[0]

        return count > 0
    
    except mysql.connector.Error as e:
        print("Error checking account number:", e)
        return True  # Consider the account number exists in case of error
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
def register_user():
    print("Registration Process:")
    while True:
        username = input("Enter your username: ")
        if not validate_username(username):
            print("Invalid username. Username should not include special characters and should be limited to 15 characters.")
            continue
        
        # Check if the username already exists in the database
        connection = connect_to_database()
        cursor = connection.cursor()
        if username_exists(cursor, username):
            print("Username already exists. Please choose a different username.")
        else:
            break

    while True:
        password = input("Enter your password: ")
        if not validate_password(password):
            print("Invalid password. Password should be at least 8 characters long with one special character.")
            continue
        else:
            break

    address = input("Enter your address: ")

    while True:
        aadhar = input("Enter your Aadhar number: ")
        if not validate_aadhar(aadhar):
            print("Invalid Aadhar number. Aadhar should be 12 digits exact and should include only numbers.")
            continue
        else:
            break

    while True:
        mobile = input("Enter your mobile number: ")
        if not validate_mobile(mobile):
            print("Invalid mobile number. Mobile number should be 10 digits exact and only numbers.")
            continue
        
        # Check if the mobile number already exists in the database
        connection = connect_to_database()
        cursor = connection.cursor()
        if mobile_number_exists(cursor, mobile):
            print("Mobile number already registered. Please enter a different mobile number.")
        else:
            break

    # Generate credit card details
    credit_card_number = generate_card_number()
    credit_card_pin = generate_pin()
    credit_card_cvv = generate_cvv()

    # Generate debit card details
    debit_card_number = generate_card_number()
    debit_card_pin = generate_pin()
    debit_card_cvv = generate_cvv()

    # Generate unique account number
    account_number = generate_account_number()
     
    #initial bank balance will be zero
    
    # Save user, account, and card details to the database
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Insert user details into 'users' table
        user_query = "INSERT INTO Users (username, password, address, aadhar, mobile) VALUES (%s, %s, %s, %s, %s)"
        user_data = (username, password, address, aadhar, mobile)
        cursor.execute(user_query, user_data)

        # Retrieve the user_id of the newly inserted user
        user_id = cursor.lastrowid

        # Insert account details into 'accounts' table
        initial_balance = Decimal('0.00')
        account_query = "INSERT INTO Accounts (user_id, account_number, balance) VALUES (%s, %s, %s)"
        account_data = (user_id, account_number, initial_balance)
        cursor.execute(account_query, account_data)

        # Insert credit card details into 'cards' table
        credit_card_query = "INSERT INTO Cards (user_id, card_type, card_number, pin, cvv) VALUES (%s, 'credit', %s, %s, %s)"
        credit_card_data = (user_id, credit_card_number, credit_card_pin, credit_card_cvv)
        cursor.execute(credit_card_query, credit_card_data)

        # Insert debit card details into 'cards' table
        debit_card_query = "INSERT INTO Cards (user_id, card_type, card_number, pin, cvv) VALUES (%s, 'debit', %s, %s, %s)"
        debit_card_data = (user_id, debit_card_number, debit_card_pin, debit_card_cvv)
        cursor.execute(debit_card_query, debit_card_data)

        connection.commit()
        print("Registration successful! Please proceed to login.")
        print("Please change your pin of your cards on your next Login.")
    
    except mysql.connector.Error as e:
        print("Error registering user:", e)
        connection.rollback()
    
    finally:
        if connection:
            cursor.close()
            connection.close()

#login function
def login_user(cursor,connection):
    u = input("Enter Your Username : ")
    p = input("Enter Your Password : ")
    query = "SELECT * FROM Users WHERE username=%s AND password=%s"
    cursor.execute(query, (u, p))
    data = cursor.fetchall()
    if data:
        user_id = data[0][0]
        
        while True:
                        print("\n1. Display Account Info")
                        print("2. List Beneficiaries")
                        print("3. List Cards")
                        print("4. Add Beneficiary")
                        print("5. Update Account Info")
                        print("6. Transfer Funds")
                        print("7. Change MPIN")
                        print("8. Register New Credit Card")
                        print("9. Add Funds")
                        print("10. View Transactions")
                        print("0. Logout")
                        option = input("Enter your option: ")
            
                        if option == "1":
                            display_account_info(cursor, user_id)
                        elif option == "2":
                            list_beneficiaries(cursor, user_id)
                        elif option == "3":
                            list_cards(cursor, user_id)
                        elif option == "4":
                            add_beneficiary(cursor,connection, user_id)
                        elif option == "5":
                            update_account_info(cursor, connection, user_id)
                        elif option == "6":
                            transfer_funds(cursor, connection, user_id)
                        elif option == "7":
                            change_mpin(cursor, connection)
                        elif option == "8":
                            register_new_credit_card(cursor, connection, user_id)
                        elif option == "9":
                            add_funds(cursor, connection, user_id)
                        elif option == "10":
                            view_transactions(cursor,user_id)
                        elif option == "0":
                            break
                        else:
                            print("Invalid option. Please try again.")
    else:
        print("Invalid username or password.")
        return False  # Return False if login fails
    
# Main function
def main():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        while True:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                login_user(cursor,connection)
               
            elif choice == "2":
                register_user()
                pass
            elif choice == "3":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
        cursor.close()
        connection.close()


main()