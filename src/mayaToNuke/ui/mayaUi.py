try:
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

class ExportToolbarWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ExportToolbarWidget, self).__init__(parent)
        
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)
        gridLayout.addWidget(QtGui.QLabel('Name:'), 0, 0)
        self.nameLE = QtGui.QLineEdit(constants.EXPORT_DEFAULT_NAME)
        gridLayout.addWidget(self.nameLE, 0, 1)
        gridLayout.addWidget(QtGui.QLabel('Start'), 0, 2)
        self.startLE = QtGui.QLineEdit('%d' % cmds.playbackOptions(q=1, min=1))
        self.startLE.setValidator(QtGui.QIntValidator())
        gridLayout.addWidget(self.startLE, 0, 3)     
        gridLayout.addWidget(QtGui.QLabel('End'), 0, 4)
        self.endLE = QtGui.QLineEdit('%d' % cmds.playbackOptions(q=1, max=1))
        self.endLE.setValidator(QtGui.QIntValidator())
        gridLayout.addWidget(self.endLE, 0, 5)         

class MayaUi(baseUi.BaseUi):
    def __init__(self, parent = None):
        super(MayaUi, self).__init__(parent)
        
        beforeAction = self.mainToolbar.actions()[0]
        exportIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton)
        exportAction = QtGui.QAction(exportIcon, 'Export Selected Objects', self.mainToolbar)
        exportAction.triggered.connect(self.__export)
        self.mainToolbar.insertAction(beforeAction, exportAction)
        
        toolbar = QtGui.QToolBar(self)
        self.exportToolbarWidget = ExportToolbarWidget(self)
        toolbar.addWidget(self.exportToolbarWidget)
        self.addToolBar(toolbar)
        
    def __export(self):
        name = self.exportToolbarWidget.nameLE.text()
        if name == constants.EXPORT_DEFAULT_NAME and len(cmds.ls(sl=1)):
            name = cmds.ls(sl=1)[0]
        start = int(self.exportToolbarWidget.startLE.text())
        end = int(self.exportToolbarWidget.endLE.text())
        date = QtCore.QDate().currentDate().toString(format = QtCore.Qt.SystemLocaleShortDate)
        time = QtCore.QTime().currentTime().toString()
        basePath = self.settings.basePath()
        filename = '%s_%s_%s.%s' % (name.replace(' ', '')
                                    , date.replace('/', '')
                                    , time.replace(':', '')
                                    , constants.EXPORT_EXT)        
        if mayaExport.alembicExport(start, end, basePath, filename):
            shapes = cmds.listRelatives(cmds.ls(sl = True)[0])
            type_ = cmds.nodeType(shapes[0])
            self.settings.addExport(name, type_, date, time, basePath, filename)
            self.exportTableWidget.reloadList()      