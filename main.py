import time
import json
import copy
import os.path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

#TODO: make linux variant.
from main_win import GetForegroundWindowTitle, getWindowTitles
from modify_options_day_scheduler import OptionsWindow
from visualizer_times import VisualizerTimes
from applications import *


def appends(s: SearchItem, i: dict, count: int):
    for j in i["others"]:
        ss = SearchItem(j["name"], j["type"], j["pattern"], count)
        s.addToSubItems(ss)
        appends(ss, j, count + 1)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.times = {}
        self.file_name = time.strftime("%d_%m_%y_times.txt")
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.times = json.load(file)
        #TODO: add more options files as options
        self.options_file_name = "options.json"

        layout = QVBoxLayout()

        self.l = QLabel(time.strftime("Today, %d %B %Y"))
        layout.addWidget(self.l)

        self.visualizer = VisualizerTimes()
        layout.addWidget(self.visualizer)

        b = QPushButton("Modify options")
        b.pressed.connect(self.open_modify_options)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.checkers = None
        self.options = {"name": "All", "others": [], "pattern": "", "type": TYPE_CONTAINS}
        if os.path.exists(self.options_file_name):
            with open(self.options_file_name, 'r') as file:
                self.options = json.load(file)
        self.updateAggregated(False, None)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.main_loop)
        self.timer.start()
        self.options_window = None
        
    def open_modify_options(self):
        if self.options_window == None or self.options_window.isHidden():
            self.options_window = OptionsWindow(self.options)
            self.options_window.save_options_sig.connect(self.setOptions)

    def updateAggregated(self, optimised: bool, lastResult):
        if not optimised:
            self.checkers = SearchItem(self.options["name"], self.options["type"], self.options["pattern"], 0)
            appends(self.checkers, self.options, 1)
            for i in self.times.keys():
                self.checkers.apply(i, self.times[i])
            self.visualizer.setAggregated(self.checkers)
        elif lastResult != None:
            applied = []
            applied.extend(self.checkers.apply(lastResult, 1))
            self.visualizer.updateAggregated(applied)

    def searchCheckers(self, searchItem: SearchItem, name: str):
        if searchItem.name == name:
            return searchItem
        for i in searchItem.subItems:
            subResult = self.searchCheckers(i, name)
            if subResult != None:
                return subResult
        if searchItem.other != None:
            return self.searchCheckers(searchItem.other, name)
        return None

    def main_loop(self):
        titles = getWindowTitles()
        result = GetForegroundWindowTitle()

        if result in self.times:
            self.times[result] += 1
        else:
            self.times[result] = 1
        self.updateAggregated(True, result)
        if self.visualizer.qtw.currentItem() == None:
            self.visualizer.qtw.setCurrentItem(self.visualizer.qtw.itemAt(0, 0))
        nameFilter = self.visualizer.qtw.currentItem().data(0, Qt.ItemDataRole.DisplayRole)
        filter = self.searchCheckers(self.checkers, nameFilter)
        if filter == None:
            print("Shouldn't have gotten here, nameFilter:", nameFilter)
        sortedList = []
        for i in filter.times.keys():
            elem = App(filter.times[i], i)
            sortedList.append(elem)
        sortedList.sort(key = lambda x : x.time, reverse=True)
        output = []
        for i in sortedList:
            output.append(str(i))
        self.visualizer.setDetailed(output)
        
        with open(self.file_name, 'w') as file:
            file.write(json.dumps(self.times))

    def setOptions(self, options):
        self.options = options
        with open(self.options_file_name, 'w') as file:
            file.write(json.dumps(self.options))
        self.updateAggregated(False, "")


app = QApplication([])
window = MainWindow(windowTitle='JulsDayScheduler')
app.exec()