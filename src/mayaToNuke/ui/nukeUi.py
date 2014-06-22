try:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)    
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
    
from mayaToNuke.ui import baseUi
from mayaToNuke.utils import nukeImport
import os

class NukeUi(baseUi.BaseUi):
    def __init__(self, parent = None):
        super(NukeUi, self).__init__(parent)
        
        # 1.)
        beforeAction = self.mainToolbar.actions()[0]
        importIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton)
        importAction = QtGui.QAction(importIcon, 'Import Selected', self.mainToolbar)
        importAction.triggered.connect(self.__import)
        self.mainToolbar.insertAction(beforeAction, importAction)
        
    def __import(self):
        item = self.exportTableWidget.currentItem() # 2.)
        if item:
            exportData = item.data(QtCore.Qt.UserRole)
            fullpath = os.path.join(exportData['path'], exportData['filename']) # 3.)
            if not os.path.isfile(fullpath): # 4.)
                msgBox = QtGui.QMessageBox()
                msgBox.setText('Cannot locate file:');
                msgBox.setInformativeText(fullpath)
                msgBox.setStandardButtons(msgBox.Cancel)
                msgBox.setDefaultButton(msgBox.Cancel)
                msgBox.exec_()
                return
            name = exportData['name']
            type_ = exportData['type']
            result = nukeImport.importFromFile(name, fullpath, type_) # 5.)          
        