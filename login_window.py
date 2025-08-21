import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QApplication, QMessageBox, QLineEdit)
from database import Database
from model_user import User
from model_account import Account
from dashboard_window import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏦 SwiftBank App - Login / Register")
        self.db = Database("bank.db")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.msg = QLabel("")
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.initUI()

# connecting the two buttons (login and register) created to action

    def initUI(self):
        self.login_button.clicked.connect(self.do_login)
        self.register_button.clicked.connect(self.do_register)

# Setting the Layouts

        hbox = QHBoxLayout()
        hbox.addWidget(self.login_button)
        hbox.addWidget(self.register_button)
        hbox.addLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.username)
        vbox.addWidget(self.password)
        vbox.addLayout(hbox)
        vbox.addWidget(self.msg)
        self.setLayout(vbox)

        self.setStyleSheet("""
                    QLabel, QPushButton{
                        font-family: calibri;
                        font-weight: bold;
                    }
                    QPushButton#login_button{
                        background-color: hsl(200, 100%, 85%);
                        border-radius: 10px;
                    }
                    QPushButton#register_button{
                        background-color: hsl(268, 29%, 59%);
                        border-radius: 10px; 
                    }
                """)

    def do_login(self):
        u = self.username.text().strip()
        p = self.password.text()
        user = User.authenticate(self.db, u, p)
        if not user:
            self.msg.setText("Invalid Username")
            return
        self.open_dashboard(user)

    def do_register(self):
        u = self.username.text().strip()
        p = self.password.text()
        try:
            user = User.register(self.db, u, p)
            QMessageBox.information(self, "Success", f"User '{u}' registered.")
            self.open_dashboard(user)
        except Exception as e:
            QMessageBox.warning(self, "Registration Error", str(e))

    def open_dashboard(self, user):
            self.dashboard = DashboardWindow(self.db, user)
            self.dashboard.show()
            self.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())



