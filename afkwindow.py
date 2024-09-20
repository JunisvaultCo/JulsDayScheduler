from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from math import *

class AfkWindow(QMainWindow):
    option_sig = pyqtSignal(str)
    def __init__(self, screenrect: QRect, *args, **kwargs):
        super(AfkWindow, self).__init__(None, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setWindowTitle("AfkWindow JulsDayScheduler")
        self.option = ""

        layout = QVBoxLayout()
        w = QWidget(self)
        w.setLayout(layout)
        self.setCentralWidget(w)

        self.label = QLabel("You seem AFK!")
        layout.addWidget(self.label)

        self.timeLabel = QLabel()
        self.setTime("")
        layout.addWidget(self.timeLabel)
        self.timeLabel.hide()

        self.timeButton = QPushButton(w)
        self.timeButton.setText("How long have I been away for?")
        self.timeButton.pressed.connect(self.showTime)
        layout.addWidget(self.timeButton)

        self.oldOption = QPushButton("")
        self.oldOption.pressed.connect(self.chooseSameOption)
        layout.addWidget(self.oldOption)
        self.oldOption.hide()

        self.tabOther = QGroupBox(w)
        layoutOther = QHBoxLayout()
        self.tabOther.setLayout(layoutOther)
        layout.addWidget(self.tabOther)

        self.comboBox = QComboBox(self.tabOther)
        self.comboBox.setEditable(True)
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.comboBox.setMinimumContentsLength(30)
        layoutOther.addWidget(self.comboBox)
        
        self.comboButton = QPushButton(w)
        self.comboButton.setText("Register")
        self.comboButton.pressed.connect(self.chooseOptionFromComboBox)
        layoutOther.addWidget(self.comboButton)
        
        self.tabOther.hide()

        self.show()
        w.setStyleSheet("QWidget { background-color : red; color: black;}")
        self.screenrect = screenrect
        self.setLocation()

    def setLocation(self):
        locX = self.screenrect.right() - self.width()
        locY = self.screenrect.bottom() - self.height()
        self.move(locX, locY)

    def setTime(self, time: str):
        self.timeLabel.setText("You have been away for: " + time)

    def setOptions(self, current: str, otherOptions: list[str]):
        self.option = current
        self.oldOption.setText("Register as " + self.option)
        self.comboBox.clear()
        self.comboBox.addItems(otherOptions)
    
    def showTime(self):
        self.show()
        self.label.hide()
        self.timeButton.hide()
        self.timeLabel.show()
        self.oldOption.show()
        self.tabOther.show()
        self.setLocation()
    
    def showLabel(self):
        self.show()
        self.timeLabel.hide()
        self.oldOption.hide()
        self.tabOther.hide()
        self.label.show()
        self.timeButton.show()
        self.setLocation()
    
    def chooseSameOption(self):
        self.chooseOption(self.option)
    
    def chooseOptionFromComboBox(self):
        self.chooseOption(self.comboBox.currentText())

    def chooseOption(self, option: str):
        self.option_sig.emit(option)
        self.hide()