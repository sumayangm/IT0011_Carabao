import random
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QDateEdit, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from datetime import date
from db import getConnection
class RegistrationError(Exception):
    pass
class RegistrationWindow(QWidget):
    goMenu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration Window")
        layout = QVBoxLayout()

        self.firstNameLabel = QLabel("First Name: ")
        self.firstNameInput = QLineEdit()
        layout.addWidget(self.firstNameLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.firstNameInput, alignment = Qt.AlignLeft)

        self.middleNameLabel = QLabel("Middle Name (N/A for None): ")
        self.middleNameInput = QLineEdit()
        layout.addWidget(self.middleNameLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.middleNameInput, alignment = Qt.AlignLeft)

        self.lastNameLabel = QLabel("Last Name: ")
        self.lastNameInput = QLineEdit()
        layout.addWidget(self.lastNameLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.lastNameInput, alignment = Qt.AlignLeft)

        self.addressNameLabel = QLabel("Address: ")
        self.addressNameInput = QLineEdit()
        layout.addWidget(self.addressNameLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.addressNameInput)

        self.birthdayLabel = QLabel("Birthday: ")
        self.birthdayInput = QDateEdit()
        self.birthdayInput.setCalendarPopup(True)
        self.birthdayInput.setDate(QDate.currentDate())
        layout.addWidget(self.birthdayLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.birthdayInput, alignment = Qt.AlignLeft)

        self.genderLabel = QLabel("Gender: ")
        self.genderInput = QComboBox()
        self.genderInput.addItem("Male")
        self.genderInput.addItem("Female")
        layout.addWidget(self.genderLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.genderInput, alignment = Qt.AlignLeft)

        self.accountTypeLabel = QLabel("Account Type: ")
        self.accountTypeInput = QComboBox()
        self.accountTypeInput.addItem("Savings Account")
        self.accountTypeInput.addItem("Current Account")
        layout.addWidget(self.accountTypeLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.accountTypeInput, alignment = Qt.AlignLeft)

        self.initialDepositLabel = QLabel("Initial Deposit: ")
        self.initialDepositInput = QLineEdit()
        layout.addWidget(self.initialDepositLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.initialDepositInput, alignment = Qt.AlignLeft)

        self.pinLabel = QLabel("PIN: ")
        self.pinInput = QLineEdit()
        self.pinInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pinLabel, alignment = Qt.AlignLeft)
        layout.addWidget(self.pinInput, alignment = Qt.AlignLeft)

        self.btnSubmitRegistration = QPushButton("Submit Registration")
        self.btnSubmitRegistration.clicked.connect(self.submitRegistration)
        layout.addWidget(self.btnSubmitRegistration)

        self.btnBack = QPushButton("Back")
        self.btnBack.clicked.connect(self.goMenu.emit)
        layout.addWidget(self.btnBack)

        self.setLayout(layout)

    def submitRegistration(self):
        try:
            conn = getConnection()

            today = date.today()
            birthday = self.birthdayInput.date().toPyDate()
            age = today.year - birthday.year -((today.month, today.day) < (birthday.month, birthday.day))
            #AGE VALIDATION
            if age < 18:
                raise RegistrationError("User must be 18 or older to register.")
                
            #PIN VALIDATION
            pinCheck = self.pinInput.text()
            if not pinCheck.isdigit():
                raise RegistrationError("PIN must contain numbers only.")
            if len(pinCheck) != 6:
                raise RegistrationError("PIN must contain exactly 6 digits.")
                
            #ACCOUNT AND DEPOSIT VALIDATION
            initialDeposit = float(self.initialDepositInput.text())
            accountType = self.accountTypeInput.currentText()
            if accountType == "Savings Account" and initialDeposit < 5000:
                raise RegistrationError("Minimum deposit for Savings Account is P5,000")
            if accountType == "Current Account" and initialDeposit < 10000:
                raise RegistrationError("Minimum deposit for Current Account is P10,000")

            accNumber = str(random.randint(1000000000, 9999999999))
                
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO accounts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                accNumber,
                self.firstNameInput.text().strip(),
                self.middleNameInput.text().strip(),
                self.lastNameInput.text().strip(),
                self.addressNameInput.text().strip(),
                self.birthdayInput.date().toPyDate(),
                self.genderInput.currentText(),
                self.accountTypeInput.currentText(),
                initialDeposit,
                self.pinInput.text()
            ))
            conn.commit()

            QMessageBox.information(self, "Registration Complete", f"Account successfully created!\n\nYour Account Number is:\n{accNumber}\n\nPlease keep this safe.")

            self.firstNameInput.clear()
            self.middleNameInput.clear()
            self.lastNameInput.clear()
            self.addressNameInput.clear()
            self.birthdayInput.setDate(QDate.currentDate())
            self.genderInput.setCurrentIndex(0)
            self.accountTypeInput.setCurrentIndex(0)
            self.initialDepositInput.clear()
            self.pinInput.clear()

            self.goMenu.emit()

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Initial deposit must be a valid number.")
        except RegistrationError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Database Error", str(e))
        finally:
            if 'cursor'in locals():
                cursor.close()
            if 'conn' in locals()and conn.open:
                conn.close()
