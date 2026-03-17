import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class CloseAccountWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Close Account")
        self.setGeometry(500, 250, 350, 200)

        layout = QVBoxLayout()

        title = QLabel("Close Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        layout.addWidget(title)

        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")

        layout.addWidget(self.acc_input)

        close_button = QPushButton("Close Account")
        close_button.clicked.connect(self.close_account)

        layout.addWidget(close_button)

        self.setLayout(layout)

    def close_account(self):

        acc_no = self.acc_input.text().strip()

        if acc_no == "":
            QMessageBox.warning(self, "Error", "Please enter an account number.")
            return

        filename = f"{acc_no}.json"

        if not os.path.exists(filename):
            QMessageBox.warning(self, "Error", "Account does not exist.")
            return

        with open(filename, "r") as file:
            data = json.load(file)

        balance = data["balance"]

        confirm = QMessageBox.question(
            self,
            "Confirm Close Account",
            f"Remaining Balance: {balance}\n\nAre you sure you want to close this account?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:

            os.remove(filename)

            QMessageBox.information(
                self,
                "Account Closed",
                f"Account successfully closed.\nReturned Balance: {balance}"
            )

            self.close()
