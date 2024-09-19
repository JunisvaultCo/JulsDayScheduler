import ctypes
import math
import ctypes.wintypes


EnumWindows = ctypes.windll.user32.EnumWindows
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
IsWindowEnabled = ctypes.windll.user32.IsWindowEnabled
IsIconic = ctypes.windll.user32.IsIconic
GetWindowRect = ctypes.windll.user32.GetWindowRect
GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow

windows = []

screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

divI = 20

sectionsX = math.ceil(screen_width / divI)
sectionsY = math.ceil(screen_height / divI - 1)
sections = [[-1] * sectionsX for _ in range(sectionsY)]

def winEnumHandler(hwnd, ctx):
    global sections
    global windows
    # Variables
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer("", length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)

    rect = ctypes.wintypes.RECT()
    GetWindowRect(hwnd, ctypes.pointer(rect))
    # DWM
    isCloacked = ctypes.c_int(0)
    ctypes.WinDLL("dwmapi").DwmGetWindowAttribute(hwnd, 14, ctypes.byref(isCloacked), ctypes.sizeof(isCloacked))


    # Append HWND to list
    if IsWindowVisible(hwnd) and IsWindowEnabled(hwnd) and length != 0 and not IsIconic(hwnd) and isCloacked.value == 0:
        windows.append({"title": buf.value,
                    "left": rect.left, "right": rect.right, "top": rect.top, "bottom": rect.bottom})
        maxY = min(math.ceil(rect.bottom / divI), sectionsY - 1)
        minY = max(0, math.ceil(rect.top / divI))
        maxX = min(math.ceil(rect.right / divI), sectionsX - 1)
        minX = max(0, math.ceil(rect.left / divI))
      #  print(buf.value, rect.bottom, rect.top, rect.right, rect.left)
        for i in range(minX, maxX + 1, 1):
            for j in range(minY, maxY + 1, 1):
                if sections[j][i] == -1:
                    sections[j][i] = len(windows) - 1
    return True

a = ctypes.WINFUNCTYPE(ctypes.c_bool,
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int))(winEnumHandler)

#returns a dictionary of visible titles + 0 - 1 how much of the visual area is covered by the.
def getWindowTitles():
    global sections
    windows.clear()
    sections = [[-1] * sectionsX for _ in range(sectionsY)]
    EnumWindows(a, None)
    titles = {}

    for i in windows:
        titles[i["title"]] = 0
    for i in sections:
        for j in i:
            if j != -1:
                titles[windows[j]["title"]] += 1
    deletes = []
    for i in titles.keys():
        if titles[i] == 0:
            deletes.append(i)
    for j in deletes:
        titles.pop(j)
    for j in titles:
        titles[j] = titles[j] / (sectionsX * sectionsY)
    print(titles)
    return titles

def GetForegroundWindowTitle():
    hwnd = GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer("", length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value