from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from applications import *
import re

def getUnit(text: str, mark: str):
    pattern = re.compile("([0-9])+" + mark)
    matches = pattern.findall(text)
    if len(matches) > 1:
        return -1
    if len(matches) == 1:
        return int(matches[0])
    return 0

class WorkWindow(QMainWindow):
    options_sig = pyqtSignal(list, int)
    def __init__(self, checkers: SearchItem, *args, **kwargs):
        super(WorkWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Work Mode Window JulsDayScheduler")

        layout = QGridLayout()
        w = QWidget(self)
        w.setLayout(layout)
        self.setCentralWidget(w)
        
        l = QLabel("Initial Apps:")
        layout.addWidget(l, 0, 0, 1, 1)

        self.initialList = QTreeWidget(w)
        self.initialList.setHeaderLabel("Name")
        self.addChecker(checkers)
        layout.addWidget(self.initialList, 1, 0, 7, 2)
        
        labelTimeBad = QLabel("Time allowed in bad apps:")
        layout.addWidget(labelTimeBad, 8, 0, 1, 1)
        
        self.boxTimeBad = QLineEdit("0h 5m 0s")
        layout.addWidget(self.boxTimeBad, 8, 1, 1, 1)

        addDesired = QPushButton("add")
        addDesired.pressed.connect(self.addDesired)
        layout.addWidget(addDesired, 1, 2, 1, 1)
        
        remDesired = QPushButton("remove")
        remDesired.pressed.connect(self.removeDesired)
        layout.addWidget(remDesired, 2, 2, 1, 1)

        l = QLabel("Desired apps:")
        layout.addWidget(l, 0, 3, 1, 2)

        self.desiredList = QListWidget(w)
        layout.addWidget(self.desiredList, 1, 3, 3, 2)

        startWorkButton = QPushButton("Start Work Mode")
        startWorkButton.pressed.connect(self.startWork)
        layout.addWidget(startWorkButton, 8, 3, 1, 2)

        self.show()
    
    def addChecker(self, checker: SearchItem):
        addSearchItemToTreeWidget(self.initialList, checker, True)

    def addDesired(self):
        toAdd = self.initialList.currentItem()
        if toAdd == None:
            return
        name = toAdd.data(0, Qt.ItemDataRole.DisplayRole)
        for i in self.desiredList.findItems("", Qt.MatchFlag.MatchContains):
            if i.data(Qt.ItemDataRole.DisplayRole) == name:
                return None
        self.desiredList.addItem(name)
    
    def removeDesired(self):
        toRem = self.desiredList.currentRow()
        self.desiredList.takeItem(toRem)
    
    def getTextEditToSeconds(self):
        text = self.boxTimeBad.text()
        h = getUnit(text, "h")
        m = getUnit(text, "m")
        s = getUnit(text, "s")
        if h == -1 or m == -1 or s == -1:
            return -1
        result = h * 60 * 60 + m * 60 + s
        return result

    def startWork(self):
        secondsAllowedBad = self.getTextEditToSeconds()
        if secondsAllowedBad == -1:
            return
        self.hide()
        rowCount = self.desiredList.model().rowCount()
        options = []
        for i in range(rowCount):
            options.append(self.desiredList.item(i).data(Qt.ItemDataRole.DisplayRole))
        self.options_sig.emit(options, secondsAllowedBad)