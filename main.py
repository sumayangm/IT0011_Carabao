import sys
from PyQt5.QtWidgets import QApplication

# Import the QIcon class for for modifying application icons
from PyQt5.QtGui import QIcon

# Import the controller class to use the created windows
from controller import Controller
# Import the config file containing the global variables need for the app
from config import basePath, iconPath

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set Icon
    app.setWindowIcon(QIcon(iconPath))

    # Load CSS
    with open(f"{basePath}/style.qss", "r") as file:
        app.setStyleSheet(file.read())
    
    window = Controller()
    window.setWindowTitle("Carabao Banking System")
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec_())