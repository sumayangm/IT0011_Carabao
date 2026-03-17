from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import mysql.connector


class AccountInfoWindow(QWidget):

    def __init__(self, menu_window):
        super().__init__()
        self.menu_window = menu_window
        self.setWindowTitle("View Account Information")
        self.setGeometry(500, 250, 400, 420)
        layout = QVBoxLayout()
        title = QLabel("Account Information")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.acc_input)
        view_btn = QPushButton("View Account")
        view_btn.clicked.connect(self.view_account)
        layout.addWidget(view_btn)
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)
        back_btn = QPushButton("Go Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def view_account(self):

        acc_no = self.acc_input.text()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="carabao_bank"
            )

            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM accounts WHERE account_number=%s",
                (acc_no,)
            )

            account = cursor.fetchone()

            cursor.close()
            conn.close()

            if not account:
                QMessageBox.warning(self, "Error", "Account not found")
                return

            info = f"""
Full Name: {account['first_name']} {account['middle_name']} {account['last_name']}
Address: {account['address']}
Birthday: {account['birthday']}
Gender: {account['gender']}
Account Type: {account['account_type']}
Current Balance: {account['balance']}
"""
            self.result.setText(info)

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def go_back(self):
        self.menu_window.show()
        self.close()
