from game_engine import GameEngine

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class PopupSignals(QtCore.QObject):
    CLOSE = QtCore.Signal()


class PopupWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PopupWidget, self).__init__(parent)
        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setStyleSheet("background:red;")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.central_widget = QWidget()
        # self.central_widget.resize(300, 120)
        self.central_widget.setFixedWidth(300)
        self.central_widget.setFixedHeight(120)


        self.central_widget.setStyleSheet("background:red;")

        self.layout.addWidget(self.central_widget, QtCore.Qt.AlignCenter)

        self.central_widget_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.central_widget_layout)
        # self.central_widget.resize(300, 120)
        self.close_btn = QtWidgets.QPushButton(self.central_widget)
        self.close_btn.setText("x")

        self.close_btn.setStyleSheet("background-color: rgb(0, 0, 0, 0)")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self._onclose)

        # self.close_btn.setAlignment(QtCore.Qt.Right)


        self.central_widget_layout.addWidget(self.close_btn, alignment=QtCore.Qt.AlignRight)

        self.SIGNALS = PopupSignals()

        self.result = 0

        # self.label = QLabel("Game over!", self)
        self.label = QLabel("", self.central_widget)
        self.label.setAlignment(QtCore.Qt.AlignVCenter)

        self.central_widget_layout.addWidget(self.label)

    # def resizeEvent(self, event):
    #     s = self.size()
    #     popup_width = 300
    #     popup_height = 120
    #     ow = int(s.width() / 2 - popup_width / 2)
    #     oh = int(s.height() / 2 - popup_height / 2)
    #     self.close_btn.move(ow + 265, oh + 5)

    def paintEvent(self, event):
        s = self.size()

        self.label.setText(f"Game over! Your result is {self.result}")
        self.label.setStyleSheet(f"font-size: 16px;"
                                f"font-weight: bold;"
                                f"color: black;")
        # label = QLabel(f"Game over! Your result is {self.result}")
        # self.add_widget(label)
        # self.fillColor = QtGui.QColor(30, 30, 30, 120)
        # self.penColor = QtGui.QColor("#333333")
        #
        # self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        # self.popup_penColor = QtGui.QColor(200, 200, 200, 255)


        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(QtGui.QColor("#333333"))
        qp.setBrush(QtGui.QColor(30, 30, 30, 120))
        qp.drawRect(0, 0, s.width(), s.height())

        qp.setPen(QtGui.QColor(240, 240, 240, 255))
        qp.setBrush(QtGui.QColor(200, 200, 200, 255))
        popup_width = 300
        popup_height = 120
        ox = int(s.width() / 2 - popup_width / 2)
        oy = int(s.height() / 2 - popup_height / 2)
        qp.drawRoundedRect(ox, oy, popup_width, popup_height, 5, 5)

        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(QtGui.QColor(70, 70, 70))
        tolw, tolh = 80, -5
        # qp.drawText(ow + int(popup_width / 2) - tolw,
        #             oh + int(popup_height / 2) - tolh,
        #             f"Game over! Your result is {self.result}")

        qp.end()

    def _onclose(self):
        self.SIGNALS.CLOSE.emit()

    def set_result(self, result):
        self.result = result


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = GameEngine()
        self.field = self.engine.get_field()
        self.layout = QtWidgets.QGridLayout()

        self.resize(500, 500)

        self.cells = list()

        self.create_grid()

        self.shortcut_left = QtGui.QShortcut(QKeySequence('left'), self)
        self.shortcut_left.activated.connect(self.on_key_press('left'))
        self.shortcut_right = QtGui.QShortcut(QKeySequence('right'), self)
        self.shortcut_right.activated.connect(self.on_key_press('right'))
        self.shortcut_up = QtGui.QShortcut(QKeySequence('up'), self)
        self.shortcut_up.activated.connect(self.on_key_press('up'))
        self.shortcut_down = QtGui.QShortcut(QKeySequence('down'), self)
        self.shortcut_down.activated.connect(self.on_key_press('down'))

        self._popup = None
        self._is_popup_on = False
        self._is_game_over = False

    def on_key_press(self, action):
        def process_action():
            if self._is_game_over:
                return

            self.field = self.engine.process_action(action)
            self.rerender()
            if self.engine.get_is_game_over():
                self._is_game_over = True
                self._on_game_end_popup()

        return process_action

    def rerender(self):
        field_as_row = []
        for i in range(self.field.shape[1]):
            for j in range(self.field.shape[0]):
                field_as_row.append(self.field[i][j])

        for i in range(len(self.cells)):
            value = field_as_row[i]
            cell_value = value if value > 0 else ""
            self.cells[i].setText(str(cell_value))
            # self.cells[i].setStyleSheet(f"background-color: {self._get_color_by_value(value)}")

            self.cells[i].setStyleSheet(f"background-color: {self._get_color_by_value(value)};"
                                        f"font-size: 32px;"
                                        f"font-weight: bold;"
                                        f"color: white;")

    def create_grid(self):

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)

        for i in range(self.field.shape[1]):
            for j in range(self.field.shape[0]):
                value = self.field[i][j]
                cell_value = value if value > 0 else ""
                label = QLabel(str(cell_value))
                label.setAlignment(QtCore.Qt.AlignCenter)

                label.setStyleSheet(f"background-color: {self._get_color_by_value(value)};"
                                    f"font-size: 32px;"
                                    f"font-weight: bold;"
                                    f"color: white;")
                self.cells.append(label)
                self.layout.addWidget(label, j, i)

    def resizeEvent(self, event):
        if self._is_popup_on:
            self._popup.move(0, 0)
            self._popup.resize(self.width(), self.height())

    def _on_game_end_popup(self):
        result = self.engine.calculate_result()

        self._popup = PopupWidget(self)
        self._popup.set_result(result)
        self._popup.move(0, 0)
        self._popup.resize(self.width(), self.height())
        self._popup.SIGNALS.CLOSE.connect(self._close_popup)
        self._is_popup_on = True
        self._popup.show()

    def _close_popup(self):
        self._popup.close()
        self._is_popup_on = False

    @staticmethod
    def _get_color_by_value(value):
        colors = {
            0: 'grey',
            2: 'pink',
            4: 'purple',
            8: 'darkblue',
            16: 'aquamarine',
            32: 'green',
            64: 'darkgreen',
            128: 'yellow',
            256: 'orange',
            512: 'magenta',
            1024: 'firebrick',
            2048: 'red'
        }

        return colors[value]
