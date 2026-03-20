from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal
import pymysql.cursors
from db import getConnection


class TransactionHistoryWindow(QWidget):
    goMenu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction History")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Transaction History")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.acc_input)

        view_btn = QPushButton("View History")
        view_btn.clicked.connect(self.load_history)
        layout.addWidget(view_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Type", "Amount", "New Balance"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("btnBack")
        back_btn.clicked.connect(self.goMenu.emit)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_history(self):
        acc_no = self.acc_input.text().strip()
        if not acc_no:
            QMessageBox.warning(self, "Input Error", "Please enter an account number.")
            return

        try:
            conn = getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # verify account exists
            cursor.execute(
                "SELECT account_number FROM accounts WHERE account_number = %s", (acc_no,)
            )
            if not cursor.fetchone():
                QMessageBox.warning(self, "Error", "Account not found. Please create a new one first.")
                return

            cursor.execute(
                "SELECT transaction_date, transaction_type, amount, new_balance "
                "FROM transactions WHERE account_number = %s ORDER BY transaction_date DESC",
                (acc_no,)
            )
            rows = cursor.fetchall()

            self.table.setRowCount(0)

            if not rows:
                QMessageBox.information(self, "No Records", "No transactions found for this account.")
                return

            for row in rows:
                rowPos = self.table.rowCount()
                self.table.insertRow(rowPos)
                self.table.setItem(rowPos, 0, QTableWidgetItem(str(row['transaction_date'])))
                self.table.setItem(rowPos, 1, QTableWidgetItem(row['transaction_type']))
                self.table.setItem(rowPos, 2, QTableWidgetItem(f"₱{row['amount']:,.2f}"))
                self.table.setItem(rowPos, 3, QTableWidgetItem(f"₱{row['new_balance']:,.2f}"))

                # color code deposit vs withdraw
                color = "#0a1a0f" if row['transaction_type'] == "Deposit" else "#1a0a0a"
                for col in range(4):
                    self.table.item(rowPos, col).setBackground(
                        __import__('PyQt5.QtGui', fromlist=['QColor']).QColor(color)
                    )

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.open:
                conn.close()