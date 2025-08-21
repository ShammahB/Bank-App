#  🏦 Bank App

This application is a simple console-based app in python that allows users to: create an account, log in securely, deposit and withdraw money, check balances and view transaction history.

---

## 📜 Table of Contents
  -[Core features]
  -[Technologies Used]
  -[App Structure]
  -[Usage]
  -[Installations]
  -[Code Snippet]
  -[Future Improvements]
  -[Contributions]
  =[License]
  -[contact]

  ---

 ## #️⃣ Core Features

 User Management
  - Register new users
  - secure login (with password hashing)
  - Account authentication
 Banking Operations
   - Deposit and withdraw funds
   - Check balance
   - Transaction history
  Data Storage
    - Store user credentials and balances
    - store transaction logs
  Security
    - Password hashing
    - Input validation and error handling

---

## 🔌Technologies Used

- Programming language: Python 3.12
- Database: SQLite
- GUI: PyQt5

---

## 🏦 App Structure

-Bank app/ 
|-database.py-|-bank.db     # Handles files and storage
|-utils.py                  # Authentication
|-model_user.py             # User-class 
|-model_account.py          # Bank Operation
|-GUI-|-dasboard_window.py  
      |-login_window.py

---

## 📈 Usage

- Launch the app and create a new account on the login window dash
- Then log in with your credentials
- Deposit funds with the "deposit" option, withdraw funds with the "withdraw" option.
- View transaction history for any account

---

## 🚀 Installations

- Clone the repo:
  '''bash
  git clone https://github.com/ShammahB/Bank-App.git
- Navigate to the project directory
- Install dependencies
- Set environment variables
  export DB_USER = 'your_user'
  export DB_PASSWORD = 'your_password'
- Run the application

---

## 👩‍💻 Code Snippet

    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QInputDialog, QMessageBox, QTableWidget, QTableWidgetItem)
    from model_account import Account

    class DashboardWindow(QWidget):
        def __init__(self, db, user):
            super().__init__()
            self.db = db
            self.user = user
            self.setWindowTitle(f"SwiftBank - Dashboard ({self.user.username})")
            self.acct = Account.get_by_user_id(self.db, user.id)
            self.balance_label = QLabel(self._balance_text())
            self.deposit_button = QPushButton("Deposit")
            self.withdraw_button = QPushButton("Withdraw")
            self.transaction_button = QPushButton("Show Transaction")
            self.initUI()

---

## 🛠️ Future Improvements
- Multi-currency support
- Transfers between accounts
- Recurring payments and scheuled transfers
- Integration with third party APIs(e.g., payment gateways)
- Security enhancements. e.g Two-factor authentication
- Improve load times for large transaction histories
- Mobile app version
---

## 🗨 Contributions

- Contributions are welcome! Please fork the repo and create a pull request.
- Follow the code style and include tests for new features.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE)

---

## 👩‍💻 Contact
- Author: Oluwabunmi Shammah Akosile
- Email: olawunmi.lola15@gmail.com
- Projet link: https://github.com/ShammahB/Bank-App
  
  
