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

    def setAggregatedItem(self, parent, parentItem: SearchItem):
        items = []
        for searchItem in parentItem.subItems:
            treeItem = QTreeWidgetItem(parent, [searchItem.name, timeRepresentation(searchItem.time)])
            items.append(treeItem)
            treeItem.addChildren(self.setAggregatedItem(treeItem, searchItem))
        if parentItem.other != None:
            treeItem = QTreeWidgetItem(parent, [parentItem.other.name, timeRepresentation(parentItem.other.time)])
            treeItem.addChildren(self.setAggregatedItem(treeItem, parentItem.other))
            items.append(treeItem)
        return items

    def setAggregated(self, searchItem: SearchItem):
        self.qtw.clear()
        items = []
        treeItem = QTreeWidgetItem(self.qtw, [searchItem.name, timeRepresentation(searchItem.time)])
        items.append(treeItem)
        treeItem.addChildren(self.setAggregatedItem(items[-1], searchItem))
        self.qtw.addTopLevelItems(items)
    
    def updateAggregated(self, listSearchItem: list[SearchItem]):
        for searchItem in listSearchItem:
            items = self.qtw.findItems(searchItem.name, Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive, 0)
            for j in items:
                j.setData(1, Qt.ItemDataRole.DisplayRole, timeRepresentation(searchItem.time))