try:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)    
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
from mayaToNuke.utils import appContext, settings
from mayaToNuke import constants

class ExportsTableWidget(QtGui.QTableWidget): # 1.)
    def __init__(self, parent = None):
        super(ExportsTableWidget, self).__init__(parent)
        self.settings = settings.Settings() # 2.)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers) # 3.)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.reloadList() # 4.)
        
    def reloadList(self):
        self.clear() # 5.)
        labels = [x.capitalize() for x in constants.EXPORT_KEYS]
        self.setColumnCount(len(labels)) # 6.)
        self.setHorizontalHeaderLabels(labels)
        exports = self.settings.exports() # 7.)
        exports.reverse()
        self.setRowCount(len(exports))
        for i in range(len(exports)): # 8.)
            for k in range(len(constants.EXPORT_KEYS)): # 9.)
                value = exports[i][constants.EXPORT_KEYS[k]]
                item = QtGui.QTableWidgetItem(str(value))
                item.setData(QtCore.Qt.UserRole, exports[i]) # 10.)
                self.setItem(i, k, item)
        self.resizeColumnsToContents() # 11.)
        self.resizeRowsToContents()

class BaseUi(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(BaseUi, self).__init__(parent)
        
        self.appContext = appContext.AppContext()
        self.settings = settings.Settings()
        self.readSettings()
        
        self.exportTableWidget = ExportsTableWidget(self)
        self.setCentralWidget(self.exportTableWidget)
        
        self.mainToolbar = QtGui.QToolBar(self)
        self.addToolBar(self.mainToolbar)

        reloadIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_BrowserReload)
        reloadAction = QtGui.QAction(reloadIcon, 'Reload Exports List', self.mainToolbar)
        reloadAction.triggered.connect(self.exportTableWidget.reloadList)
        self.mainToolbar.addAction(reloadAction)  
        
        clearIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_TrashIcon)
        clearAction = QtGui.QAction(clearIcon, 'Clear Exports List (Irreversible)', self.mainToolbar)
        clearAction.triggered.connect(self.__clearExports)
        self.mainToolbar.addAction(clearAction)  
        
        self.mainToolbar.addSeparator()
        
        basePathIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_ComputerIcon)
        basePathAction = QtGui.QAction(basePathIcon, 'Set Path to Exports-Dir', self.mainToolbar)
        basePathAction.triggered.connect(self.__setBasePath)
        self.mainToolbar.addAction(basePathAction)
        
        helpIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogHelpButton)       
        helpAction = QtGui.QAction(helpIcon, 'Online Help', self.mainToolbar)
        helpAction.triggered.connect(self.__openOnlineHelp)
        self.mainToolbar.addAction(helpAction)
        
        self.__updateWindowTitle()
        
    def __updateWindowTitle(self):
        title = '%s - %s - %s' % (constants.TOOLNAME
                                  , self.appContext.toString()
                                  , self.settings.basePath())
        self.setWindowTitle(title)
        
    def __clearExports(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText('This action is irreversible');
        msgBox.setInformativeText('Do you want to proceed?')
        msgBox.setStandardButtons(msgBox.Ok | msgBox.Cancel)
        msgBox.setDefaultButton(msgBox.Cancel)
        result = msgBox.exec_()
        if result == msgBox.Ok:
            self.settings.clearExports()
            self.exportTableWidget.reloadList()
            
    def __openOnlineHelp(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(constants.HELP_URL))
        
    def __setBasePath(self):
        dialog = QtGui.QFileDialog(self, 'Set Path to Exports-Dir'
                                   , self.settings.basePath())
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        if dialog.exec_():
            newPath = dialog.directory().absolutePath()
            self.settings.setBasePath(newPath)
            self.__updateWindowTitle()
         
    def closeEvent(self, event):
        self.settings.setAppCtxAttr('geometry', self.saveGeometry())
        self.settings.setAppCtxAttr('state', self.saveState())
        return QtGui.QMainWindow.closeEvent(self, event)
    
    def readSettings(self):
        geometry = self.settings.getAppCtxAttr('geometry')
        if geometry: self.restoreGeometry(geometry)
        state = self.settings.getAppCtxAttr('state')
        if state: self.restoreState(state)