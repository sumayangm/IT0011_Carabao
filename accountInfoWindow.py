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

        pin_label = QLabel("Enter PIN:")
        pin_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(pin_label)
 
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(6)
        layout.addWidget(self.pin_input)

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
        
    def showEvent(self, event):
        self.acc_input.clear()
        self.pin_input.clear()
        self.result.clear()
        super().showEvent(event)

    def view_account(self):
        acc_no = self.acc_input.text().strip()
        pin = self.pin_input.text().strip()
 
        if not acc_no:
            QMessageBox.warning(self, "Input Error", "Please enter an account number.")
            return
 
        if not pin:
            QMessageBox.warning(self, "Input Error", "Please enter your PIN.")
            return
 
        if not pin.isdigit():
            QMessageBox.warning(self, "Invalid PIN", "PIN must contain numbers only.")
            return
 
        try:
            conn = getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
 
            cursor.execute(
                "SELECT * FROM accounts WHERE account_number = %s AND pin = %s",
                (acc_no, pin)
            )
            account = cursor.fetchone()
 
            if not account:
                QMessageBox.critical(
                    self,
                    "Access Denied",
                    "Invalid account number or PIN.\nPlease try again."
                )
                self.pin_input.clear()
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
            self.pin_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.open:
                conn.close()
