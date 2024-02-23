use Banking_db;


CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    aadhar VARCHAR(12) UNIQUE NOT NULL,
    mobile VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE Accounts (
    account_number BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    balance DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES Users(id)
) AUTO_INCREMENT = 100000000000;


CREATE TABLE Beneficiaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    beneficiary_name VARCHAR(255),
    account_number VARCHAR(20),
    bank_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    card_type ENUM('debit', 'credit'),
    card_number VARCHAR(16),
    pin VARCHAR(4),
    cvv VARCHAR(3),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    beneficiary_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(id),
    FOREIGN KEY (beneficiary_id) REFERENCES Users(id)
);