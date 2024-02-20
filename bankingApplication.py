from decimal import Decimal
import mysql.connector
import random

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
        
def register_user():
    print("Registration Process:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    address = input("Enter your address: ")
    aadhar = input("Enter your Aadhar number: ")
    mobile = input("Enter your mobile number: ")

    # Generate credit card details
    credit_card_number = generate_card_number()

    credit_card_pin = generate_pin()
    while True:
        credit_card_cvv = generate_cvv()
        if not cvv_exists(credit_card_cvv):
            break

    # Generate debit card details
    debit_card_number = generate_card_number()
    debit_card_pin = generate_pin()

    # Generate unique CVV
    while True:
        debit_card_cvv = generate_cvv()
        if not cvv_exists(debit_card_cvv):
            break

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
        initial_balance = 0000.00
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
        print("Error registering user:Please try again.", e)
    
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
                        print("9. Logout")
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