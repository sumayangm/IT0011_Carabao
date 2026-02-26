from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class MenuWindow(QWidget):
    goMenu = pyqtSignal()
    goRegister = pyqtSignal()
    goBalanceInq = pyqtSignal()
    goDeposit = pyqtSignal()
    goWithdraw = pyqtSignal()
    goAccInfo = pyqtSignal()
    goClose = pyqtSignal()
    goExit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        layout = QVBoxLayout()

        self.label = QLabel("Carabao Banking System")
        layout.addWidget(self.label, alignment = Qt.AlignCenter)

        self.btnRegister = QPushButton("Open A New Account")
        self.btnRegister.clicked.connect(self.goRegister.emit)
        layout.addWidget(self.btnRegister)

        self.btnBalanceInq = QPushButton("Balance Inquiry")
        self.btnBalanceInq.clicked.connect(self.goBalanceInq.emit)
        layout.addWidget(self.btnBalanceInq)

        self.btnDeposit = QPushButton("Deposit")
        self.btnDeposit.clicked.connect(self.goDeposit.emit)
        layout.addWidget(self.btnDeposit)

        self.btnWithdraw = QPushButton("Withdraw")
        self.btnWithdraw.clicked.connect(self.goWithdraw.emit)
        layout.addWidget(self.btnWithdraw)

        self.btnAccInfo = QPushButton("View Account Information")
        self.btnAccInfo.clicked.connect(self.goAccInfo.emit)
        layout.addWidget(self.btnAccInfo)

        self.btnClose = QPushButton("Close Account")
        self.btnClose.clicked.connect(self.goClose.emit)
        layout.addWidget(self.btnClose)

        self.btnExit = QPushButton("Exit Program")
        self.btnExit.clicked.connect(self.goExit.emit)
        layout.addWidget(self.btnExit)

        self.setLayout(layout)
