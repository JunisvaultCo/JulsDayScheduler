import math


TYPE_EQUAL = "equals"
TYPE_ENDSWITH = "ends with"
TYPE_CONTAINS = "contains"
TYPE_LIST = [TYPE_EQUAL, TYPE_ENDSWITH, TYPE_CONTAINS]

def timeRepresentation(seconds):
    minutes = math.floor(seconds / 60) % 60
    hours = math.floor(seconds / 3600)
    seconds = seconds % 60
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s" 

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
    def __init__(self, name: str, checker: Checker, level: int):
        self.name = name
        self.checker = checker
        self.subItems = []
        self.time = 0
        self.level = level

    def __init__(self, name: str, checker: str, pattern: str, level: int):
        self.name = name
        if checker == TYPE_CONTAINS:
            self.checker = FindingChecker(pattern)
        elif checker == TYPE_EQUAL:
            self.checker = EqualChecker(pattern)
        elif checker == TYPE_ENDSWITH:
            self.checker = EndingChecker(pattern)
        else:
            print("wrong type", checker)
        self.subItems = []
        self.time = 0
        self.level = level

    def addToSubItems(self, subitem):
        if type(subitem) != type(self):
            print("trying to add wrong type to addToSubItems, adding", type(subitem))
        self.subItems.append(subitem)

    def apply(self, string: str, time: int):
        result = []
        if not self.checker.applies(string):
            return result
        self.time = self.time + time
        result.append(self)
        for i in self.subItems:
            result.extend(i.apply(string, time))
        return result

    def __repr__(self):
        repr = "\t" * self.level + self.name + ": " + timeRepresentation(self.time)
        for i in self.subItems:
            repr = repr + "\n" + str(i)
        return repr

