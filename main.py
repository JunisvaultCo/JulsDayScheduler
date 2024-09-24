import time
import json
import os.path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

#TODO: make linux variant.
from main_win import GetForegroundWindowTitle, getWindowTitles, CheckAnyActivitySinceLastTime
from modify_options_day_scheduler import OptionsWindow
from visualizer_times import VisualizerTimes
from applications import *
from afkwindow import AfkWindow
from workwindow import WorkWindow
from window_warning import WindowWarning

DEFAULT_MAX_AFK = 30
app = QApplication([])

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

        goodTimesGroup = QGroupBox()
        layoutGood = QHBoxLayout()
        goodTimesGroup.setLayout(layoutGood)
        self.totalGoodTimeLabel = QLabel()
        self.currentGoodTimeLabel = QLabel()
        layoutGood.addWidget(self.currentGoodTimeLabel)
        layoutGood.addWidget(self.totalGoodTimeLabel)
        layout.addWidget(goodTimesGroup)

        b = QPushButton("Modify options")
        b.pressed.connect(self.open_modify_options)
        layout.addWidget(b)

        self.modeButton = QPushButton()
        layout.addWidget(self.modeButton)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)


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
        self.timeWithoutMods = 0
        self.afkTime = DEFAULT_MAX_AFK
        self.afkWindow = None
        self.isAFK = False
        self.workWindow = None
        self.workMode = False
        self.allowedCheckers = []
        self.maxAllowedBadTime = 0
        self.currentBadTime = 0
        self.totalBadTime = 0
        self.currentGoodTime = 0
        self.totalGoodTime = 0
        self.setModeButton(False)
        self.window_warning = None
        self.show()
        
    def open_modify_options(self):
        if self.options_window == None or self.options_window.isHidden():
            self.options_window = OptionsWindow(self.options)
            self.options_window.save_options_sig.connect(self.setOptions)

    def updateAggregated(self, optimised: bool, lastResult: str, time = 1):
        if not optimised:
            self.checkers = SearchItem(self.options["name"], self.options["type"], self.options["pattern"], 0)
            appends(self.checkers, self.options, time)
            for i in self.times.keys():
                self.checkers.apply(i, self.times[i])
            self.visualizer.setAggregated(self.checkers)
        elif lastResult != None:
            applied = []
            applied.extend(self.checkers.apply(lastResult, time))
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
        if CheckAnyActivitySinceLastTime() and not self.isAFK:
            self.timeWithoutMods = 0
        else:
            self.timeWithoutMods += 1
            if self.timeWithoutMods == self.afkTime:
                self.isAFK = True
                if self.afkWindow == None:
                    screenrect = app.primaryScreen().availableGeometry()
                    self.afkWindow = AfkWindow(screenrect)
                    self.afkWindow.option_sig.connect(self.returnFromAfk)
                else:
                    self.afkWindow.showLabel()
                self.afkWindow.setOptions(result, self.times.keys())
            if self.timeWithoutMods >= self.afkTime:
                self.afkWindow.setTime(timeRepresentation(self.timeWithoutMods))

        if not self.isAFK:
            self.updateResult(result, 1)
        else:
            self.updateResult(result, 0)

    def returnFromAfk(self, option):
        self.updateResult(option, self.timeWithoutMods)
        self.updateResult(self.afkWindow.option, - self.afkTime)
        self.timeWithoutMods = 0
        self.isAFK = False
        self.afkWindow.showLabel()

    def updateResult(self, result: str, time: int):
        if result in self.times:
            self.times[result] += time
        else:
            self.times[result] = time
        self.updateAggregated(True, result, time)
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
        if self.workMode:
            ok = False
            for i in self.allowedCheckers:
                if i.checker.applies(result):
                    ok = True
                    self.currentGoodTime += 1
                    self.totalGoodTime += 1

            if not ok:
                self.currentBadTime += 1
                self.totalBadTime += 1
                if self.currentBadTime == self.maxAllowedBadTime + 1:
                    screenrect = app.primaryScreen().availableGeometry()
                    self.window_warning = WindowWarning(timeRepresentation(self.totalBadTime), screenrect)
                    self.window_warning.end_sig.connect(self.returnFromBad)
            self.currentGoodTimeLabel.setText("Current time spent well: " + timeRepresentation(self.currentGoodTime))
        else:
            self.currentGoodTimeLabel.setText("Work mode not currently on!")
        self.totalGoodTimeLabel.setText("Total time spent well: " + timeRepresentation(self.totalGoodTime))

    def setOptions(self, options):
        self.options = options
        with open(self.options_file_name, 'w') as file:
            file.write(json.dumps(self.options))
        self.updateAggregated(False, "")
    
    def setModeButton(self, setBefore: bool):
        if not self.workMode:
            self.modeButton.setText("Start Work Mode")
            self.modeButton.pressed.connect(self.popWorkWindow)
            if setBefore:
                self.modeButton.pressed.disconnect(self.stopWorkMode)
        else:
            self.modeButton.setText("Stop Work Mode")
            if setBefore:
                self.modeButton.pressed.disconnect(self.popWorkWindow)
            self.modeButton.pressed.connect(self.stopWorkMode)

    def popWorkWindow(self):
        if self.workWindow == None:
            self.workWindow = WorkWindow(self.checkers)
            self.workWindow.options_sig.connect(self.startWorkMode)
        else:
            self.workWindow.show()

    def startWorkMode(self, options_sig: list[str], maxBadTime: int):
        self.currentGoodTime = 0
        self.allowedCheckers = []
        for i in options_sig:
            self.allowedCheckers.append(self.checkers.find(i))
        self.maxAllowedBadTime = maxBadTime
        self.workMode = True
        self.setModeButton(True)

    def stopWorkMode(self):
        self.workMode = False
        self.setModeButton(True)
    def returnFromBad(self):
        self.currentBadTime = 0


window = MainWindow(windowTitle='JulsDayScheduler')
app.exec()