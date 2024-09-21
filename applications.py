import math


TYPE_EQUAL = "equals"
TYPE_ENDSWITH = "ends with"
TYPE_CONTAINS = "contains"
TYPE_LIST = [TYPE_EQUAL, TYPE_ENDSWITH, TYPE_CONTAINS]

def timeRepresentation(seconds):
    minutes = math.floor(seconds / 60) % 60
    hours = math.floor(seconds / 3600)
    seconds = seconds % 60
    if hours != 0:
        return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"
    if minutes != 0:
        return str(minutes) + "m " + str(seconds) + "s"
    return str(seconds) + "s"

class App():
    def __init__(self, time, title):
        self.time = time
        self.title = title

    def __repr__(self):
        representation = timeRepresentation(self.time)
        return representation + " " + self.title

#we have entire apps and subtabs inside an app to track

class Checker():
    def __init__(self, stringToSearch: str):
        self.stringToSearch = stringToSearch

    def applies(self, string: str):
        return True

class FindingChecker(Checker):
    def __init__(self, stringToSearch: str):
        super().__init__(stringToSearch)

    def applies(self, string: str):
        return string.find(self.stringToSearch) != -1

class EndingChecker(Checker):
    def __init__(self, stringToSearch: str):
        super().__init__(stringToSearch)

    def applies(self, string: str):
        return string.endswith(self.stringToSearch)
    
class EqualChecker(Checker):
    def __init__(self, stringToSearch: str):
        super().__init__(stringToSearch)

    def applies(self, string: str):
        return string == self.stringToSearch

class SearchItem():
    
    def otherInit(self, name: str, level:int):
        self.name = name
        self.subItems = []
        self.time = 0
        self.level = level
        self.other = None
        self.times = {}

    def __init__(self, name: str, checker: Checker, level: int):
        self.checker = checker
        self.otherInit(name, level)

    def __init__(self, name: str, checker: str, pattern: str, level: int):
        self.otherInit(name, level)
        if checker == TYPE_CONTAINS:
            self.checker = FindingChecker(pattern)
        elif checker == TYPE_EQUAL:
            self.checker = EqualChecker(pattern)
        elif checker == TYPE_ENDSWITH:
            self.checker = EndingChecker(pattern)
        else:
            print("wrong type", checker)

    def addToSubItems(self, subitem):
        if self.other == None:
            self.other = SearchItem("Misc " + self.name, TYPE_CONTAINS, "", self.level + 1)

        if type(subitem) != type(self):
            print("trying to add wrong type to addToSubItems, adding", type(subitem))
        self.subItems.append(subitem)

    def apply(self, string: str, time: int):
        result = []
        if not self.checker.applies(string):
            return result
        self.time = self.time + time
        if string in self.times.keys():
            self.times[string] += time
        else:
            self.times[string] = time
        result.append(self)
        for i in self.subItems:
            result.extend(i.apply(string, time))
        if len(self.subItems) != 0 and len(result) == 1:
            result.extend(self.other.apply(string, time))
        return result

    def __repr__(self):
        repr = "\t" * self.level + self.name + ": " + timeRepresentation(self.time)
        for i in self.subItems:
            repr = repr + "\n" + str(i)
        return repr

