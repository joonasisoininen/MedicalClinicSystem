import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!



def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

#Use QTableView to display lists of patients.
#Use QPlainTextEdit for viewing and editing notes.
#Ensure all GUI code resides in the clinic/gui/ directory.