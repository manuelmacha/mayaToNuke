try:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
from mayaToNuke.utils.appContext import AppContext
from mayaToNuke.constants import TOOLNAME
    
UI = None # 1.) 
def getUi():
    global UI # 2.)
    appCtx = AppContext() # 3.)
    if not UI: # 4.)
        if appCtx.isMaya():
            from mayaToNuke.ui import mayaUi
            UI = mayaUi.MayaUi()            
        elif appCtx.isNuke():
            from mayaToNuke.ui import nukeUi
            UI = nukeUi.NukeUi()
        elif appCtx.isStandalone():
            from mayaToNuke.ui import baseUi
            UI = baseUi.BaseUi()          
    return UI # 5.)

def showUi(): # 6.)
    ui = getUi()
    ui.show()
#    ui.raise_()
#    
#def deleteUi():
#    global UI
#    if UI:
#        UI.close()
#        UI.setParent(None)
#        UI = None  