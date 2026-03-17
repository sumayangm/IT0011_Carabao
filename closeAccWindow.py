from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import mysql.connector


class CloseAccWindow(QWidget):

    def __init__(self, menu_window):
        super().__init__()
        self.menu_window = menu_window
        self.setWindowTitle("Close Account")
        self.setGeometry(500, 250, 350, 220)
        layout = QVBoxLayout()
        title = QLabel("Close Account")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.acc_input)
        close_btn = QPushButton("Close Account")
        close_btn.clicked.connect(slf.close_account)
        layout.addWidget(close_btn)
        back_btn = QPushButton("Go Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def close_account(self):
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
                "SELECT balance FROM accounts WHERE account_number=%s",
                (acc_no,)
            )
            account = cursor.fetchone()

            if not account:
                QMessageBox.warning(self, "Error", "Account not found")
                cursor.close()
                conn.close()
                return

            balance = account["balance"]

            confirm = QMessageBox.question(
                self,
                "Confirm Close Account",
                f"Remaining Balance: {balance}\n\nAre you sure you want to close this account?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:

                cursor.execute(
                    "DELETE FROM transactions WHERE account_number=%s",
                    (acc_no,)
                )

                cursor.execute(
                    "DELETE FROM accounts WHERE account_number=%s",
                    (acc_no,)
                )
                conn.commit()
                QMessageBox.information(
                    self,
                    "Account Closed",
                    f"Account successfully closed.\nReturned Balance: {balance}"
                )
                self.menu_window.show()
                self.close()
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
    def go_back(self):
        self.menu_window.show()
        self.close()
