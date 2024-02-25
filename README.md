

Banking Application Using Python

ABOUT

In this project, I have created a Banking Application using Python and MySQL. Data entered by the user are stored in MYSQL database in tabular form.

This Python-based banking application offers a robust suite of features including account management, fund transfers, and beneficiary management, all accessible through a user-friendly interface. With a focus on security and convenience, users can register new cards, update account details, and perform transactions with ease, ensuring a seamless banking experience. Its comprehensive functionality and intuitive design make it a reliable solution for modern banking needs.

*Requirement 
1.Python Latest Version
2.Visual Code 
3.Mysql

*Module Used In python Code 
datetime
mysql.connector 
decimal random

Before Running This Code in Your System Make Sure you have created the User , Accounts, Cards, Beneficiaries and Transactions Table.

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL, aadhar VARCHAR(12) UNIQUE NOT NULL, mobile VARCHAR(10) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL);

CREATE TABLE Accounts (
    account_number BIGINT AUTO_INCREMENT PRIMARY KEY,user_id INT,balance DECIMAL(10, 2),FOREIGN KEY (user_id) REFERENCES Users(id) AUTO_INCREMENT = 100000000000);

CREATE TABLE Beneficiaries (
    id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, beneficiary_name VARCHAR(255), account_number VARCHAR(20), bank_name VARCHAR(255), FOREIGN KEY (user_id) REFERENCES Users(id));

CREATE TABLE Cards (
    id INT AUTO_INCREMENT PRIMARY KEY,user_id INT,card_type ENUM('debit', 'credit'),card_number VARCHAR(16),pin VARCHAR(4),cvv VARCHAR(3),FOREIGN KEY (user_id) REFERENCES Users(id));

CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY, sender_id INT NOT NULL, beneficiary_id INT NOT NULL, amount DECIMAL(10, 2) NOT NULL, transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (sender_id) REFERENCES Users(id), FOREIGN KEY (beneficiary_id) REFERENCES Users(id));

Some glimse of the Code is Shown below.

![Screenshot from 2024-02-23 12-52-14](https://github.com/Sanjana176/Banking_Application/assets/160119835/c2abc036-768c-45dc-b57b-15e7ba5c6c32)
![Screenshot from 2024-02-23 12-52-39](https://github.com/Sanjana176/Banking_Application/assets/160119835/5e51af41-d5ba-416c-8f50-65fcc6fc7d9a)
![Screenshot from 2024-02-23 12-53-03](https://github.com/Sanjana176/Banking_Application/assets/160119835/a7f87661-3668-4f6e-a1b4-206c96ed12d5)



