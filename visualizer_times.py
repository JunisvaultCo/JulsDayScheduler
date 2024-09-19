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

    def setAggregatedItem(self, item: QTreeWidgetItem, listSearchItem: SearchItem):
        items = []
        for searchItem in listSearchItem:
            treeItem = QTreeWidgetItem(item, [searchItem.name, timeRepresentation(searchItem.time)])
            items.append(treeItem)
            treeItem.addChildren(self.setAggregatedItem(treeItem, searchItem.subItems))
        return items

    def setAggregated(self, searchItem: SearchItem):
        self.qtw.clear()
        items = []
        treeItem = QTreeWidgetItem(self.qtw, [searchItem.name, timeRepresentation(searchItem.time)])
        items.append(treeItem)
        treeItem.addChildren(self.setAggregatedItem(items[-1], searchItem.subItems))
        self.qtw.addTopLevelItems(items)
    
    def updateAggregated(self, listSearchItem: list[SearchItem]):
        for searchItem in listSearchItem:
            items = self.qtw.findItems(searchItem.name, Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive, 0)
            for j in items:
                j.setData(1, Qt.ItemDataRole.DisplayRole, timeRepresentation(searchItem.time))