try:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)    
    from PyQt4 import QtCore
except ImportError:
    from PySide import QtCore
    
from mayaToNuke import constants
from mayaToNuke.utils import appContext
import os
    
class Settings(QtCore.QSettings):
    def __init__(self):
        super(Settings, self).__init__(constants.TOOLNAME)
        self.appCtxStr = appContext.AppContext().toString() # 1.)
        if not self.basePath(): # 2.)
            homeDir = QtCore.QDir().homePath()
            self.setBasePath(homeDir)
                
    def setBasePath(self, basePath): # 3.)
        path = QtCore.QDir(basePath)
        if not path.dirName() == constants.TOOLNAME: # 4.)
            path.mkdir(constants.TOOLNAME)
            basePath = os.path.join(basePath, constants.TOOLNAME)
        self.setValue('basePath', basePath) # 5.)
        
    def basePath(self): # 6.)
        return self.value('basePath')        
        
    def setUiAttr(self, key, value): # 7.)
        self.beginGroup(self.appCtxStr)
        self.setValue(key, value)
        self.endGroup()
        
    def getUiAttr(self, key): # 8.)
        self.beginGroup(self.appCtxStr)
        value = self.value(key)
        self.endGroup()
        return value       
    
    # 9.)
    def addExport(self, name, type_, date, time, path, filename):
        numExports = self.beginReadArray('exports')
        self.endArray()
        self.beginWriteArray('exports')
        self.setArrayIndex(numExports)
        self.setValue('name', name)
        self.setValue('type', type_)
        self.setValue('date', date)
        self.setValue('time', time)
        self.setValue('path', path)
        self.setValue('filename', filename)
        self.endArray()
        return self.basePath(), filename
    
    # 10.)
    def exports(self):
        exports = []
        numExports = self.beginReadArray('exports')
        for i in range(numExports):
            export = {}
            self.setArrayIndex(i)
            for key in constants.EXPORT_KEYS:
                export[key] = self.value(key)
            exports.append(export)
        self.endArray()
        return exports