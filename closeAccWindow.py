from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
import pymysql.cursors
from db import getConnection  


class CloseAccWindow(QWidget):
    goMenu = pyqtSignal()  

    def __init__(self):  
        super().__init__()
        self.setWindowTitle("Close Account")
        self.setGeometry(500, 250, 350, 220)
        
        layout = QVBoxLayout()
        title = QLabel("Close Account")
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

        close_btn = QPushButton("Close Account")
        close_btn.clicked.connect(self.close_account)
        layout.addWidget(close_btn)
        
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.goMenu.emit)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)

    def showEvent(self, event):
        self.acc_input.clear()
        self.pin_input.clear()
        super().showEvent(event)

    def close_account(self):
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
                "SELECT balance FROM accounts WHERE account_number = %s AND pin = %s",
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

            balance = account["balance"]

            confirm = QMessageBox.question(
                self,
                "Confirm Close Account",
                f"Remaining Balance: ₱{balance:,.2f}\n\nAre you sure you want to close this account?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                cursor.execute(
                    "DELETE FROM transactions WHERE account_number = %s", (acc_no,)
                )
                cursor.execute(
                    "DELETE FROM accounts WHERE account_number = %s", (acc_no,)
                )
                conn.commit()

                QMessageBox.information(
                    self,
                    "Account Closed",
                    f"Account successfully closed.\nReturned Balance: ₱{balance:,.2f}"
                )

                self.acc_input.clear()
                self.pin_input.clear()
                self.goMenu.emit()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            if 'conn' in locals() and conn.open:
                conn.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.open:
                conn.close()