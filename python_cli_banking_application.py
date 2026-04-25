# ============================================================
# FINAL PROJECT DESCRIPTION
# ============================================================
# Author: Jose Sanchez Nuñez
# Course: COP1047C-2263-8684
# Date: April 25, 2026
# GitHub: https://github.com/jsancheznunez/PythonFinalProject.git
#
# In this final project, you will build a Python-based 
# Command-Line Interface (CLI) Banking Application that 
# simulates real-world banking operations.
#
# This project showcases your understanding of key programming 
# concepts including:
# - Functions
# - Loops
# - Classes (OOP)
# - File I/O (JSON persistence)
# - Data visualization (pandas & matplotlib)
# - Searching and sorting algorithms
# - Recursive logic
# ============================================================

# ==============================
# CLI BANKING APPLICATION (FULL)
# ==============================
# Features:
# - OOP (Account, Transaction, Bank)
# - File persistence (JSON)
# - Searching & sorting
# - Recursive logic (transaction sum)
# - Data visualization (pandas + matplotlib)
# - CLI interface

import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "bank_data.json"

# -----------------------------
# Models
# -----------------------------
class Transaction:
    def __init__(self, amount, t_type, date=None):
        self.amount = amount
        self.type = t_type
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {"amount": self.amount, "type": self.type, "date": self.date}


class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction(amount, "deposit"))

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        self.balance -= amount
        self.transactions.append(Transaction(amount, "withdraw"))
        return True

    # Recursive total calculation
    def recursive_total(self, tx_list=None):
        if tx_list is None:
            tx_list = self.transactions
        if not tx_list:
            return 0
        return tx_list[0].amount + self.recursive_total(tx_list[1:])

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "transactions": [t.to_dict() for t in self.transactions]
        }

    @staticmethod
    def from_dict(data):
        acc = Account(data["name"], data["balance"])
        acc.transactions = [Transaction(t["amount"], t["type"], t["date"]) for t in data["transactions"]]
        return acc


# -----------------------------
# Bank System
# -----------------------------
class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_data()

    def create_account(self, name):
        if name in self.accounts:
            print("Account already exists")
            return
        self.accounts[name] = Account(name)
        self.save_data()
        print("Account created")

    def get_account(self, name):
        return self.accounts.get(name)

    # Searching
    def search_accounts(self, keyword):
        return [acc for acc in self.accounts.values() if keyword.lower() in acc.name.lower()]

    # Sorting
    def sort_accounts_by_balance(self, reverse=False):
        return sorted(self.accounts.values(), key=lambda x: x.balance, reverse=reverse)

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.accounts.items()}, f, indent=4)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for name, acc_data in data.items():
                self.accounts[name] = Account.from_dict(acc_data)

    def visualize_account(self, name):
        acc = self.get_account(name)
        if not acc or not acc.transactions:
            print("No data to visualize")
            return

        df = pd.DataFrame([t.to_dict() for t in acc.transactions])
        df['date'] = pd.to_datetime(df['date'])

        deposits = df[df['type'] == 'deposit']
        withdrawals = df[df['type'] == 'withdraw']

        plt.figure()
        plt.plot(deposits['date'], deposits['amount'], label='Deposits')
        plt.plot(withdrawals['date'], withdrawals['amount'], label='Withdrawals')
        plt.legend()
        plt.title(f"Transactions for {name}")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.show()


# -----------------------------
# CLI
# -----------------------------

def main():
    bank = Bank()

    while True:
        print("""
1. Create Account
2. Deposit
3. Withdraw
4. View Balance
5. Search Accounts
6. Sort Accounts
7. Recursive Total (All Transactions)
8. Visualize Account
9. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            bank.create_account(input("Name: "))

        elif choice == "2":
            name = input("Name: ")
            acc = bank.get_account(name)
            if acc:
                acc.deposit(float(input("Amount: ")))
                bank.save_data()

        elif choice == "3":
            name = input("Name: ")
            acc = bank.get_account(name)
            if acc and acc.withdraw(float(input("Amount: "))):
                bank.save_data()

        elif choice == "4":
            acc = bank.get_account(input("Name: "))
            if acc:
                print("Balance:", acc.balance)

        elif choice == "5":
            results = bank.search_accounts(input("Search: "))
            for acc in results:
                print(acc.name, acc.balance)

        elif choice == "6":
            sorted_accs = bank.sort_accounts_by_balance(reverse=True)
            for acc in sorted_accs:
                print(acc.name, acc.balance)

        elif choice == "7":
            acc = bank.get_account(input("Name: "))
            if acc:
                print("Total Transactions:", acc.recursive_total())

        elif choice == "8":
            bank.visualize_account(input("Name: "))

        elif choice == "9":
            break

        else:
            print("Invalid")


if __name__ == "__main__":
    main()


# ==============================
# README.md
# ==============================
"""
# CLI Banking Application

## How to Run
1. Install dependencies:
   pip install pandas matplotlib
2. Run the app:
   python app.py

## Features
- Create and manage accounts
- Deposit and withdraw money
- Persistent storage using JSON
- Search accounts by name
- Sort accounts by balance
- Recursive transaction total calculation
- Data visualization of transactions

## Challenges / Reflections
- Managing persistent data without a database required careful JSON handling
- Designing recursion for transaction totals helped reinforce algorithmic thinking
- Keeping CLI simple but functional required balancing usability vs features
- Visualization adds real-world analytical value to the system
"""
