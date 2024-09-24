from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from math import *

class WindowWarning(QMainWindow):
    end_sig = pyqtSignal()
    def __init__(self, time: str, screenrect: QRect, *args, **kwargs):
        super(WindowWarning, self).__init__(None, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setWindowTitle("WindowWarning JulsDayScheduler")
        self.option = ""

        layout = QVBoxLayout()
        w = QWidget(self)
        w.setLayout(layout)
        self.setCentralWidget(w)
        
        label = QLabel("Get your ass back to work! You spent " + time + " on bad apps!")
        layout.addWidget(label)

        endButton = QPushButton("Understood!")
        endButton.pressed.connect(self.endIt)
        layout.addWidget(endButton)
        
        self.showMaximized()
        w.setStyleSheet("QWidget { background-color : gray; color: black;}")
        left = max(floor(screenrect.right() / 2) - 200, 0)
        top = max(floor(screenrect.bottom() / 2) - 50, 0)
        right = max(floor(screenrect.right() / 2) - 200, 0)
        bottom = max(floor(screenrect.bottom() / 2) - 50, 0)

        layout.setContentsMargins(left, top, right, bottom)
    
    def endIt(self):
        self.hide()
        self.end_sig.emit()