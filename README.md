# Carabao Banking System – Final Project

## Overview

This project is a GUI-based **Mini Banking System** developed in Python. The system simulates core banking operations including account creation, deposits, withdrawals, balance inquiry, and account management.

The group name serves as the **Bank Name** and is displayed on all user interface windows of the system.

The program implements:

- User-defined classes  
- User-defined functions  
- Python collection types (list, dictionary, set, or tuple)  
- A Python GUI library (e.g., Tkinter or PyQt)  
- File handling or MySQL for data persistence  

Each account is stored in a separate file named after its account number. This file serves as the system database for that specific account.

---

## Main Menu

When the program starts, it displays the following menu:

1. Open a New Account  
2. Balance Inquiry  
3. Deposit  
4. Withdraw  
5. View Account Information  
6. Close Account  
7. Exit Program  

After every completed transaction, the system redisplays the main menu.

---

## Functional Requirements

### 1. Open a New Account

The system collects the following information:

- First Name  
- Middle Name  
- Last Name  
- Address  
- Birthday  
- Gender (M or F only)  
- Account Type (Savings Account or Current Account)  
- Initial Deposit  
- 6-digit PIN  

#### Validation Rules

- The user must be **18 years old or older**.
- Gender input must strictly be **M or F**.
- Minimum Initial Deposit:
  - Savings Account: **5000**
  - Current Account: **10000**
- PIN must be a **6-digit numeric value**.

A **random account number** is automatically generated.

After successful account creation:
- A file named after the generated account number is created.
- All account details are stored in that file.

---

### 2. Balance Inquiry

- The user enters the account number.
- If the account does not exist, the system informs the user and returns to the main menu.
- If valid, the current balance is displayed.

---

### 3. Deposit

- The user enters the account number.
- The system asks for the deposit amount.

#### Validation Rules

- Negative values are not allowed.
- Minimum deposit:
  - Savings Account: **300**
  - Current Account: **500**

The system asks for confirmation before processing.

If confirmed:
- The amount is added to the current balance.
- A success message is displayed.

---

### 4. Withdraw

- The user enters the account number.
- The system asks for the withdrawal amount.

#### Validation Rules

- Negative values are not allowed.
- The amount cannot exceed the current balance.
- Minimum withdrawal:
  - Savings Account: **300**
  - Current Account: **500**

The system asks for confirmation before processing.

If confirmed:
- The amount is deducted from the current balance.
- A success message is displayed.

---

### 5. View Account Information

Displays all stored account details:

- Full Name  
- Address  
- Birthday  
- Gender  
- Account Type  
- Initial Deposit  
- Current Balance  

---

### 6. Close Account

- The user enters the account number.
- The system asks for confirmation.

If confirmed:
- The remaining balance is returned to the user.
- The account file is deleted.
- All account data is cleared.
- A confirmation message is displayed.

---

### 7. Exit Program

- All in-memory account data is saved back to the corresponding files.
- A thank-you message is displayed.
- The names of the group members are shown.

---

## Data Handling and Persistence

- Each account has its own file named after the account number.
- When a user performs a transaction:
  - Account data is loaded from the file into a class structure for faster processing.
- When exiting the program:
  - All updated data is written back to the file.
- When closing an account:
  - The corresponding account file is permanently deleted.

---

## Optional Feature (Bonus)

### View Transaction History

An additional menu option may be implemented:

- Displays past deposit and withdrawal transactions.
- Transaction records are stored in the account file.

---

## Technical Implementation Requirements

The program must demonstrate:

- Use of user-defined classes (e.g., `Account`, `BankSystem`)
- Use of user-defined functions
- Use of at least one Python collection type
- Use of a Python GUI library
- Proper file handling or MySQL integration
- Input validation and error handling

---