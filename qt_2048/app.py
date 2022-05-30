import sys
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication


from game_field import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.setWindowTitle("2048")
    # Icon
    # window.setWindowIcon(QtGui.QIcon())

    window.show()

    app.exec()


