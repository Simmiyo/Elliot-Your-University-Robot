import os

from win32api import GetFileVersionInfo, LOWORD, HIWORD


def getUipathVersionNumber(filename: str):
    try:
        info = GetFileVersionInfo(filename, "\\")       # pe asta o face api-ul windows
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except KeyError:
        return 0, 0, 0, 0


def getRobotPath():
    try:
        uiPathApp = os.environ['UIPATH_USER_SERVICE_PATH']
        # intra in environment variables (care e dict) si retine calea specificata la cheia data
        netPos = uiPathApp.find(r"\net")
        return uiPathApp[:netPos] + r"\UiRobot.exe"
    except KeyError:
        currentUser = os.environ['USERPROFILE']
        uiPath = currentUser + r"\AppData\Local\UiPath"
        version = ".".join([str(x) for x in getUipathVersionNumber(uiPath + r"\UiPath.Studio.exe")])
        if version[-1] == '0':
            version = version.rsplit(".", 1)[0]
        with os.scandir(uiPath) as dirs:
            for fold in dirs:
                if fold.name.find(version) != -1:
                    return uiPath + "\\" + fold.name + r"\UiRobot.exe"
    return None

