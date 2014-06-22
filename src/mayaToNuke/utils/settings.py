try: # 1.)
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)    
    from PyQt4 import QtCore
except ImportError:
    from PySide import QtCore
    
from mayaToNuke import constants
from mayaToNuke.utils import appContext
import os
    
class Settings(QtCore.QSettings): # 2.)
    def __init__(self):
        super(Settings, self).__init__(constants.TOOLNAME) # 3.)
        self.appCtxStr = appContext.AppContext().toString() # 4.)
        if not self.basePath(): # 5.)
            homeDir = QtCore.QDir().homePath() # 6.)
            self.setBasePath(homeDir)
                
    def setBasePath(self, basePath): # 7.)
        path = QtCore.QDir(basePath)  # 8.)
        if not path.dirName() == constants.TOOLNAME: # 9.)
            path.mkdir(constants.TOOLNAME)
            basePath = os.path.join(basePath, constants.TOOLNAME)
        self.setValue('basePath', basePath) # 10.)
        
    def basePath(self): # 11.)
        return self.value('basePath')        
        
    def setAppCtxAttr(self, key, value): # 12.)
        self.beginGroup(self.appCtxStr) # 13.)
        self.setValue(key, value)
        self.endGroup()
        
    def getAppCtxAttr(self, key): # 14.)
        self.beginGroup(self.appCtxStr)
        value = self.value(key)
        self.endGroup()
        return value       
    
    def addExport(self, *args): # 15.)
        numExports = self.beginReadArray('exports') # 16.)
        self.endArray()
        self.beginWriteArray('exports') # 17.)
        self.setArrayIndex(numExports)
        for i in range(len(args)): # 18.)
            self.setValue(constants.EXPORT_KEYS[i], args[i])
        self.endArray()
        return self.basePath(), self.value('filename')
    
    def exports(self): # 19.)
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