
# PyQt/PySide imports
try:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
    
from mayaToNuke.utils.appContext import AppContext
from mayaToNuke.constants import TOOLNAME

# Logging
import logging
logger = logging.getLogger(__name__)
    
UI = None

def getUi():
    global UI
    appCtx = AppContext()
    if not UI:
        if appCtx.isMaya():
            from mayaToNuke.ui import mayaUi
            UI = mayaUi.MayaUi()            
        elif appCtx.isNuke():
            from mayaToNuke.ui import nukeUi
            UI = nukeUi.NukeUi()
        elif appCtx.isStandalone():
            from mayaToNuke.ui import baseUi
            UI = baseUi.BaseUi()
    logger.info('Starting %s in %s mode' % (TOOLNAME, appCtx.toString()))            
    return UI

def showUi():
    ui = getUi()
    ui.show()
    ui.raise_()
    
def deleteUi():
    global UI
    if UI:
        UI.close()
        UI.setParent(None)
        UI = None
        
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    showUi()
    sys.exit(app.exec_())    