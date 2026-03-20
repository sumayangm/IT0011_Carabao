from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
import pymysql.cursors
from db import getConnection

class BalanceInquiryWindow(QWidget):
    goMenu = pyqtSignal()                          

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Balance Inquiry")

        layout = QVBoxLayout()                     
        layout.setSpacing(8)
        layout.setContentsMargins(24, 24, 24, 24)

        layout.addStretch()

        self.label = QLabel("Enter Account Number:")
        self.label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label)

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account Number")
        layout.addWidget(self.account_input)

        self.pin_label = QLabel("Enter PIN:")
        self.pin_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.pin_label)

        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(6)
        layout.addWidget(self.pin_input)

        self.check_button = QPushButton("Check Balance")
        self.check_button.clicked.connect(self.verify_pin)
        layout.addWidget(self.check_button)

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("btnBack")
        self.back_button.clicked.connect(self.goMenu.emit)  
        layout.addWidget(self.back_button)                  

        layout.addStretch()

        self.setLayout(layout)

    def showEvent(self, event):
        self.account_input.clear()
        self.pin_input.clear()
        super().showEvent(event)

    def verify_pin(self):
        account_number = self.account_input.text().strip()
        pin = self.pin_input.text().strip()

        if account_number == "":
            QMessageBox.warning(self, "Missing Input", "Please enter an account number.")
            return

        if pin == "":
            QMessageBox.warning(self, "Missing Input", "Please enter your PIN.")
            return

        if not pin.isdigit():
            QMessageBox.warning(self, "Invalid PIN", "PIN must contain numbers only.")
            return

        try:
            conn = getConnection()                 
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s AND pin = %s",
                (account_number, pin)
            )
            result = cursor.fetchone()

            if result is None:
                QMessageBox.critical(
                    self,
                    "Access Denied",
                    "Invalid account number or PIN.\nPlease try again."
                )
                self.pin_input.clear()
                return

            balance = float(result["balance"])

            QMessageBox.information(
                self,
                "Balance Inquiry",
                f"Account Number: {account_number}\nCurrent Balance: ₱{balance:,.2f}"
            )

            self.pin_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.open:   
                conn.close()