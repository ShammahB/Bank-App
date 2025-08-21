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

# connecting buttons to  actions

    def initUI(self):
        self.deposit_button.clicked.connect(self.do_deposit)
        self.withdraw_button.clicked.connect(self.do_withdraw)
        self.transaction_button.clicked.connect(self.show_transaction)

# setting up the layout

        vbox = QVBoxLayout()

        vbox.addWidget(self.balance_label)
        vbox.addWidget(self.deposit_button)
        vbox.addWidget(self.withdraw_button)
        vbox.addWidget(self.transaction_button)

        self.setLayout(vbox)

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton#deposit_button{
                background-color: hsl(200, 100%, 85%);
                border-radius: 10px;
            }
            QPushButton#withdraw_button{
                background-color: hsl(268, 29%, 59%);
                border-radius: 10px; 
            }
            QPushButton#transaction_button{
                background-color: hsl(16, 94%, 60%);
                border-radius: 10px;    
        """)


    def _balance_text(self):
        return f"Balance: {self.acct.balance:.2f}"

    def refresh_balance(self):
        self.acct = Account.get_by_user_id(self.db, self.user.id)
        self.balance_label.setText(self._balance_text())

    def do_deposit(self):
        amount, ok = QInputDialog.getDouble(self, "Deposit", "Amount:", 0, 0, 1e12, 2)
        if not ok:
            return
        try:
            self.acct.deposit(self.db, float(amount))
            QMessageBox.information(self, "Success", f"Deposited {amount:.2f}")
            self.refresh_balance()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def do_withdraw(self):
        amount, ok = QInputDialog.getDouble(self, "Withdraw", "Amount:", 0, 0, 1e12, 2)
        if not ok:
            return
        try:
            self.acct.withdraw(self.db, float(amount))
            QMessageBox.information(self, "Success", f"Withdrew {amount:.2f}")
            self.refresh_balance()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_transaction(self):
        txns = self.acct.get_transactions(self.db, limit=50)
        if not txns:
            QMessageBox.information(self, "Transactions", "No transactions yet.")
            return

# creating a table with 3 columns (type, amount, timestamp) - it fills the table row by row with transaction data

        table = QTableWidget()
        table.setRowCount(len(txns))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Type", "Amount", "Timestamp"])

        for i, t in enumerate(txns):
            table.setItem(i, 0, QTableWidgetItem(t['txn_type']))
            table.setItem(i, 1, QTableWidgetItem(f"{t['amount']:.2f}"))
            table.setItem(i, 0, QTableWidgetItem(t['Timestamp']))
        table.resizeColumnsToContents()

# creating an open dialogue that shows the transaction table

        dlg = QInputDialog(self)
        dlg.setWindowTitle("Transactions")
        v = QVBoxLayout()
        v.addWidget(table)
        dlg.setLayout(v)
        dlg.exec_()







