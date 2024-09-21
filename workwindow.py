from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from applications import *

class WorkWindow(QMainWindow):
    option_sig = pyqtSignal(str)
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
        
        boxTimeBad = QLineEdit("0h 5m 0s")
        layout.addWidget(boxTimeBad, 8, 1, 1, 1)

        addDesired = QPushButton("add")
        addDesired.pressed.connect(self.addDesired)
        layout.addWidget(addDesired, 1, 2, 1, 1)
        
        remDesired = QPushButton("remove")
        remDesired.pressed.connect(self.removeDesired)
        layout.addWidget(remDesired, 2, 2, 1, 1)

        addBad = QPushButton("add")
        layout.addWidget(addBad, 5, 2, 1, 1)
        
        remBad = QPushButton("remove")
        layout.addWidget(remBad, 6, 2, 1, 1)

        l = QLabel("Desired apps:")
        layout.addWidget(l, 0, 3, 1, 2)

        self.desiredList = QListWidget(w)
        layout.addWidget(self.desiredList, 1, 3, 3, 2)
        
        l = QLabel("Bad apps:")
        layout.addWidget(l, 4, 3, 1, 2)
        
        self.badList = QListWidget(w)
        layout.addWidget(self.badList, 5, 3, 3, 2)

        startWorkButton = QPushButton("Start Work Mode")
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