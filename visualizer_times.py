from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from applications import *

class VisualizerTimes(QWidget):
    def __init__(self, *args, **kwargs):
        super(VisualizerTimes, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.qtw = QTreeWidget(self)
        layout.addWidget(self.qtw)
        self.qtw.setColumnCount(2)
        self.qtw.setHeaderLabels(["Name", "Time"])

        self.qlw = QListWidget(self)
        layout.addWidget(self.qlw)

    def setDetailed(self, list: list):
        self.qlw.clear()
        self.qlw.addItems(list)

    def setAggregated(self, searchItem: SearchItem):
        addSearchItemToTreeWidget(self.qtw, searchItem)
    
    def updateAggregated(self, listSearchItem: list[SearchItem]):
        for searchItem in listSearchItem:
            items = self.qtw.findItems(searchItem.name, Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive, 0)
            for j in items:
                j.setData(1, Qt.ItemDataRole.DisplayRole, timeRepresentation(searchItem.time))