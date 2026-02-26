from PyQt5.QtWidgets import QStackedWidget

from menuWindow import MenuWindow
from registrationWindow import RegistrationWindow
from balanceInquiryWindow import BalanceInquiryWindow
from depositWindow import DepositWindow
from withdrawWindow import WithdrawWindow
from accountInfoWindow import AccountInfoWindow
from closeAccWindow import CloseAccWindow

class Controller(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.menu = MenuWindow()
        self.register = RegistrationWindow()
        self.balanceInq = BalanceInquiryWindow()
        self.deposit = DepositWindow()
        self.withdraw = WithdrawWindow()
        self.accInfo = AccountInfoWindow()
        self.close = CloseAccWindow()
        
        self.addWidget(self.menu)
        self.addWidget(self.register)
        self.addWidget(self.balanceInq)
        self.addWidget(self.deposit)
        self.addWidget(self.withdraw)
        self.addWidget(self.accInfo)
        self.addWidget(self.close)

        self.menu.goMenu.connect(
            lambda: self.setCurrentWidget(self.menu)
        )
        self.menu.goRegister.connect(
            lambda: self.setCurrentWidget(self.register)
        )
        self.menu.goBalanceInq.connect(
            lambda: self.setCurrentWidget(self.balanceInq)
        )
        self.menu.goDeposit.connect(
            lambda: self.setCurrentWidget(self.deposit)
        )
        self.menu.goWithdraw.connect(
            lambda: self.setCurrentWidget(self.withdraw)
        )
        self.menu.goAccInfo.connect(
            lambda: self.setCurrentWidget(self.accInfo)
        )
        self.menu.goClose.connect(
            lambda: self.setCurrentWidget(self.close)
        )
