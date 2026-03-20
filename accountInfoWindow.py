from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
import pymysql.cursors
from db import getConnection  


class AccountInfoWindow(QWidget):
    goMenu = pyqtSignal() 

    def __init__(self):  
        super().__init__()
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
        
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.goMenu.emit)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def view_account(self):
        acc_no = self.acc_input.text().strip()
        if not acc_no:
            QMessageBox.warning(self, "Input Error", "Please enter an account number.")
            return

        try:
            conn = getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)  # pymysql dict cursor
            cursor.execute(
                "SELECT * FROM accounts WHERE account_number = %s", (acc_no,)
            )
            account = cursor.fetchone()

            if not account:
                QMessageBox.warning(self, "Error", "Account not found. Please create a new one first.")
                return

            info = (
                f"Full Name:     {account['first_name']} {account['middle_name']} {account['last_name']}\n"
                f"Address:       {account['address']}\n"
                f"Birthday:      {account['birthday']}\n"
                f"Gender:        {account['gender']}\n"
                f"Account Type:  {account['account_type']}\n"
                f"Balance:       ₱{account['balance']:,.2f}"
            )
            self.result.setText(info)

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.open:
                conn.close()
