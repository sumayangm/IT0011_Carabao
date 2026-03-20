from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from db import getConnection

class WithdrawWindow(QWidget):
    goMenu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.msg = QMessageBox()
        self.setWindowTitle("Menu")
        self.sui()

    #--CLEAR LAYOUT
    def clrL (self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.takeAt(i)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    #--SQL
    #create function to get the account number
    def sui(self):
        self.clrL()

        self.accn = QLabel('Enter Account Number: ')
        self.accn.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.accn, alignment = Qt.AlignCenter)

        self.getAccn = QLineEdit()
        self.layout.addWidget(self.getAccn)

        self.p_btn()
        self.bck_btn()

    def check_accn(self):
        try:
            uc_accn = self.getAccn.text()
            self.Anum = uc_accn
        except ValueError:
            QMessageBox.critical(self, "ERROR", "Enter a valid account number")
            self.getAccn.clear()
            return
        self.asql()
        
    def asql(self):
        conn = getConnection()
        cur = conn.cursor()
        cur.execute(
            "SELECT balance, account_type FROM accounts WHERE account_number = %s", (self.Anum,)
        )
        result = cur.fetchone()
        if result is None:
            QMessageBox.critical(self, "ERROR", "Account number not found")
        else:
            self.bal = result[0]
            self.acct = result[1]
            cur.close()
            conn.close()

            if not self.verify_pin():    # PIN check before proceeding
                return

            self.anumchkd()
        
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals() and conn.open:
            conn.close()

    def verify_pin(self):
        try:
            conn = getConnection()
            cur = conn.cursor()
            cur.execute(
                "SELECT pin FROM accounts WHERE account_number = %s", (self.Anum,)
            )
            result = cur.fetchone()
            stored_pin = result[0] if result else None
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            return False
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals() and conn.open:
                conn.close()

        from PyQt5.QtWidgets import QInputDialog
        pin, ok = QInputDialog.getText(
            self, "PIN Verification",
            "Enter your PIN:",
            QLineEdit.Password
        )

        if not ok or pin.strip() == "":
            QMessageBox.warning(self, "Cancelled", "Transaction cancelled.")
            return False

        if pin.strip() != stored_pin:
            QMessageBox.critical(self, "Invalid PIN", "Incorrect PIN. Transaction cancelled.")
            return False

        return True

    def upd_bal(self, updBal):
        conn = getConnection()
        cur = conn.cursor()
        usql = ("UPDATE accounts SET balance = %s WHERE account_number = %s")
        cur.execute(usql, (updBal, self.Anum))
        conn.commit()
        cur.close()
        conn.close()
    #--END OF SQL

    def log_transaction(self, transaction_type, amount, new_balance):
        try:
            conn = getConnection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, new_balance) "
                "VALUES (%s, %s, %s, %s)",
                (self.Anum, transaction_type, amount, new_balance)
            )
            conn.commit()
        except Exception as e:
            pass  # logging failure should not block the transaction
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals() and conn.open:
                conn.close()
                
    #SAVINGS ACCOUNT
    def sa(self):
        self.clrL()
        self.sacur_bal = self.bal

        self.satitle = QLabel("SAVINGS ACCOUNT")
        self.satitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.satitle, alignment = Qt.AlignCenter)

        self.saCB = QLabel(f'Current Balance:\nPhp {self.sacur_bal:.2f}')
        self.saCB.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.saCB, alignment = Qt.AlignCenter)
        
        self.sa_enter_bal()

    #CURRENT ACCOUNT
    def ca(self):
        self.clrL()
        self.cacur_bal = self.bal

        self.catitle = QLabel("CURRENT ACCOUNT")
        self.catitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.catitle, alignment = Qt.AlignCenter)

        self.caCB = QLabel(f'Current Balance:\nPhp {self.cacur_bal:.2f}')
        self.caCB.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.caCB, alignment = Qt.AlignCenter)

        self.ca_enter_bal()
        
    #SA: enter amount function
    def sa_enter_bal(self):
        self.sEB = QLabel('Enter Amount: ')
        self.sEB.setStyleSheet("font-size: 15px")
        self.sEB.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sEB, alignment = Qt.AlignCenter)

        self.sentBal = QLineEdit()
        self.layout.addWidget(self.sentBal)

        self.sa_btncal()
        self.bck_btn()

    #CA: enter amount function
    def ca_enter_bal(self):
        self.cEB = QLabel('Enter Amount: ')
        self.cEB.setStyleSheet("font-size: 15px")
        self.cEB.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.cEB, alignment = Qt.AlignCenter)

        self.centBal = QLineEdit()
        self.layout.addWidget(self.centBal)

        self.ca_btncal()
        self.bck_btn()

    #Check if the input amount is more than 300
    def sa_check_AmtIn(self):
        try:
            amt = int(self.sentBal.text())
            if amt < 300:
                raise ValueError
            if amt > self.sacur_bal:
                QMessageBox.critical(self, "ERROR", f"Insufficient balance. Current balance is ₱{self.sacur_bal:,.2f}")
                self.sentBal.clear()
                return None
            return amt
        except ValueError:
            click = self.invalin()
            if click == QMessageBox.Cancel:
                self.sui()
                self.goMenu.emit()
                self.sentBal.clear()
            elif click == QMessageBox.Ok:
                self.sentBal.clear()
                return None
                
    #Check if the input amount is more than 500
    def ca_check_AmtIn(self):
        try:
            amt = int(self.centBal.text())
            if amt < 500:
                raise ValueError
            if amt > self.cacur_bal:
                QMessageBox.critical(self, "ERROR", f"Insufficient balance. Current balance is ₱{self.cacur_bal:,.2f}")
                self.centBal.clear()
                return None
            return amt
        except ValueError:
            click = self.invalin()
            if click == QMessageBox.Cancel:
                self.sui()
                self.goMenu.emit()
                self.centBal.clear()
            elif click == QMessageBox.Ok:
                self.centBal.clear()
                return None

    #calculations
    def sa_calcWithdraw(self):
        amt = self.sa_check_AmtIn()
        if amt is not None:
            new_bal = self.sacur_bal - amt
            self.upd_bal(new_bal)
            self.log_transaction("Withdraw", amt, new_bal)
            self.end_msg()
    
    def ca_calcWithdraw(self):
        amt = self.ca_check_AmtIn()
        if amt is not None:
            new_bal = self.cacur_bal - amt
            self.upd_bal(new_bal)
            self.log_transaction("Withdraw", amt, new_bal)
            self.end_msg()
        
    #--BUTTONS
    def hbck(self):
        self.sui()
        self.goMenu.emit()

    def bck_btn(self):
        self.bckbtn = QPushButton(self)
        self.bckbtn.setText("BACK")
        self.bckbtn.clicked.connect(self.hbck)
        self.layout.addWidget(self.bckbtn)


    def p_btn(self):
        self.pbtn = QPushButton(self)
        self.pbtn.setText("ENTER")
        self.pbtn.clicked.connect(self.check_accn)
        self.layout.addWidget(self.pbtn,)

    #SA: button for calculation
    def sa_btncal(self):
        self.btn = QPushButton(self)
        self.btn.setText("WITHDRAW")
        self.btn.clicked.connect(self.sval_msg)
        self.layout.addWidget(self.btn)

    #CA: button for calculation
    def ca_btncal(self):
        self.btn = QPushButton(self)
        self.btn.setText("WITHDRAW")
        self.btn.clicked.connect(self.cval_msg)
        self.layout.addWidget(self.btn)
    #--END OF BUTTONS

    #--POP UP MESSAGES
    #when "Yes" is clicked, only then the calculation happen
    def sval_msg(self):
        smsg = self.msg
        smsg.setIcon(QMessageBox.Question)
        
        smsg.setWindowTitle('CONFIRMATION')
        smsg.setText("Do you want to proceed with the transaction?")
        smsg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

        click = smsg.exec_()
        if click == QMessageBox.Yes:
            self.sa_calcWithdraw()
    
    def cval_msg(self):
        cmsg = self.msg
        cmsg.setIcon(QMessageBox.Question)
        
        cmsg.setWindowTitle('CONFIRMATION')
        cmsg.setText("Do you want to proceed with the transaction?")
        cmsg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

        click = cmsg.exec_()
        if click == QMessageBox.Yes:
            self.ca_calcWithdraw()

    #When user press "Ok", the user is directed to the corresponding account type of the account
    def anumchkd(self):
        msg = self.msg
        msg.setIcon(QMessageBox.Information)
        
        msg.setWindowTitle(' ')
        msg.setText("Account Number Found!")
        msg.setStandardButtons(QMessageBox.Ok)

        click = msg.exec_()
        if click == QMessageBox.Ok:
            if self.acct == 'Savings Account':
                self.sa()
            elif self.acct == 'Current Account':
                self.ca()

    #when an error happened and if the user clicked cancel, user will go back to the menu 
    def invalin(self):
        imsg = self.msg
        imsg.setIcon(QMessageBox.Critical)

        imsg.setWindowTitle(' ')
        imsg.setWindowTitle('INVALID INPUT')
        imsg.setText("Input a valid amount or cancel the transaction")
        imsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return imsg.exec_()

    #When user press "Ok", the user is directed back to the menu 
    def end_msg(self):
        emsg = self.msg
        emsg.setIcon(QMessageBox.Information)
        
        emsg.setWindowTitle(' ')
        emsg.setText("Transaction Complete!")
        emsg.setStandardButtons(QMessageBox.Ok)

        click = emsg.exec_()
        if click == QMessageBox.Ok:
            self.goMenu.emit()
            self.sui()
    #--END OF POP UP MESSAGES