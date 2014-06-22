try: # 1.)
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)    
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
    
from mayaToNuke.ui import baseUi
from mayaToNuke.utils import mayaExport
from mayaToNuke import constants
import maya.cmds as cmds

class ExportToolbarWidget(QtGui.QWidget): # 2.)
    def __init__(self, parent = None):
        super(ExportToolbarWidget, self).__init__(parent)
        
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)
        gridLayout.addWidget(QtGui.QLabel('Name:'), 0, 0)
        self.nameLE = QtGui.QLineEdit(constants.EXPORT_DEFAULT_NAME) # 3.)
        gridLayout.addWidget(self.nameLE, 0, 1)
        gridLayout.addWidget(QtGui.QLabel('Start'), 0, 2) # 4.)
        self.startLE = QtGui.QLineEdit('%d' % cmds.playbackOptions(q=1, min=1))
        self.startLE.setValidator(QtGui.QIntValidator()) 
        gridLayout.addWidget(self.startLE, 0, 3)     
        gridLayout.addWidget(QtGui.QLabel('End'), 0, 4)
        self.endLE = QtGui.QLineEdit('%d' % cmds.playbackOptions(q=1, max=1))
        self.endLE.setValidator(QtGui.QIntValidator())
        gridLayout.addWidget(self.endLE, 0, 5)         

class MayaUi(baseUi.BaseUi): # 5.)
    def __init__(self, parent = None):
        super(MayaUi, self).__init__(parent)
        
        beforeAction = self.mainToolbar.actions()[0] # 6.)
        exportIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton)
        exportAction = QtGui.QAction(exportIcon, 'Export Selected Objects', self.mainToolbar)
        exportAction.triggered.connect(self.__export) # 7.)
        self.mainToolbar.insertAction(beforeAction, exportAction)
        
        toolbar = QtGui.QToolBar(self) # 8.)
        self.exportToolbarWidget = ExportToolbarWidget(self)
        toolbar.addWidget(self.exportToolbarWidget)
        self.addToolBar(toolbar)
        
    def __export(self): # 9.)
        name = self.exportToolbarWidget.nameLE.text()
        if name == constants.EXPORT_DEFAULT_NAME and len(cmds.ls(sl=1)): # 10.)
            name = cmds.ls(sl=1)[0]
        start = int(self.exportToolbarWidget.startLE.text()) # 11.)
        end = int(self.exportToolbarWidget.endLE.text())
        date = QtCore.QDate().currentDate().toString(format = QtCore.Qt.SystemLocaleShortDate)
        time = QtCore.QTime().currentTime().toString()
        basePath = self.settings.basePath()
        # 12.)
        filename = '%s_%s_%s.%s' % (name.replace(' ', '')
                                    , date.replace('/', '')
                                    , time.replace(':', '')
                                    , constants.EXPORT_EXT)    
        if mayaExport.alembicExport(start, end, basePath, filename): # 13.) 
            shapes = cmds.listRelatives(cmds.ls(sl = True)[0]) # 14.)
            type_ = cmds.nodeType(shapes[0])
            self.settings.addExport(name, type_, date, time, basePath, filename) # 15.)
            self.exportTableWidget.reloadList() # 16.)  