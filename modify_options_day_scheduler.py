import time
import json
import os.path
from applications import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class OptionsLine(QWidget):
    def __init__(self, definingOption, *args, **kwargs):
        super(OptionsLine, self).__init__(*args, **kwargs)
        self.storedState = definingOption
        self.updateFromState()

    def updateFromState(self):
        self.layoutOut = QVBoxLayout()
        self.setLayout(self.layoutOut)
        pane = QGroupBox()
        self.layoutIn = QHBoxLayout()
        pane.setLayout(self.layoutIn)
        self.layoutOut.addWidget(pane)

        others = self.storedState["others"]
        type = self.storedState["type"]
        name = self.storedState["name"]
        pattern = self.storedState["pattern"]

        self.nameL = QLineEdit(self)
        self.nameL.setText(name)
        self.layoutIn.addWidget(self.nameL)

        self.typeL = QComboBox(self)
        self.typeL.insertItems(0, TYPE_LIST)
        for (jn, jt) in enumerate(TYPE_LIST):
            if jt == type:
                self.typeL.setCurrentIndex(jn)
        self.layoutIn.addWidget(self.typeL)

        self.patternL = QLineEdit(self)
        self.patternL.setText(pattern)
        self.layoutIn.addWidget(self.patternL)

        b = QPushButton("+")
        b.pressed.connect(self.add_option)

        self.layoutIn.addWidget(b)

        r = QPushButton("-")
        r.pressed.connect(self.remove_option)

        self.layoutIn.addWidget(r)

        self.children = []
        for i in others:
            newI = OptionsLine(i)
            self.children.append(newI)
            self.layoutOut.addWidget(newI)

    def add_option(self):
        newChild = OptionsLine({"type": TYPE_EQUAL, "name": "", "others": [], "pattern": ""})
        self.children.append(newChild)
        self.layoutOut.addWidget(newChild)

    #TODO: come back to this lmao
    def remove_option(self):
        pass
    
    def getState(self):
        self.storedState = {"type": self.typeL.currentText(), "name": self.nameL.text(), "pattern": self.patternL.text(), "others": []}
        for i in self.children:
            self.storedState["others"].append(i.getState())
        return self.storedState

class OptionsWindow(QMainWindow):
    save_options_sig = pyqtSignal(dict)
    def __init__(self, options, *args, **kwargs):
        super(OptionsWindow, self).__init__(*args, **kwargs)
        self.options = options
        self.setWindowTitle("Options JulsDayScheduler")

        layout = QVBoxLayout()

        self.l = QLabel("Modify options regarding parsing")
        save = QPushButton("Save Options")
        save.pressed.connect(self.save_options)

        group = QGroupBox(self)
        self.layoutGroup = QVBoxLayout()
        group.setLayout(self.layoutGroup)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumSize(300, 300)
        scroll.setWidget(group)

        layout.addWidget(self.l)
        layout.addWidget(scroll)
        layout.addWidget(save)

        w = QWidget()
        w.setLayout(layout)

        self.child = None
        self.setCentralWidget(w)
        
        self.draw_options()
        self.show()
    def draw_options(self):
        self.child = OptionsLine(self.options)
        self.layoutGroup.addWidget(self.child)

    def save_options(self):
        self.options = self.child.getState()
        self.save_options_sig.emit(self.options)