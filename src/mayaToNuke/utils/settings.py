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
        
        self.appCtxStr = appContext.AppContext().toString()
        if not self.basePath():
            homeDir = QtCore.QDir().homePath()
            self.setBasePath(homeDir)
        
    def setUiAttr(self, key, value):
        self.beginGroup(self.appCtxStr)
        self.setValue(key, value)
        self.endGroup()
        
    def getUiAttr(self, key):
        self.beginGroup(self.appCtxStr)
        value = self.value(key)
        self.endGroup()
        return value   
        
    def basePath(self):
        return self.value('basePath')
    
    def setBasePath(self, basePath):
        path = QtCore.QDir(basePath)
        if not path.dirName() == constants.TOOLNAME:
            path.mkdir(constants.TOOLNAME)
            basePath = os.path.join(basePath, constants.TOOLNAME)
        self.setValue('basePath', basePath)
        print basePath
        
    def clearBasePath(self):
        self.remove('basePath')
        
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
    
    def clearExports(self):
        self.remove('exports')

if __name__ == '__main__':
    s = Settings()
    #s.setBasePath('/Users/manuel/Desktop/abc')
    s.clearBasePath()
    #print s.basePath()
    #s.clearExports()
    #s.addExport('myObject', 'geo', 4, 5, 'dasd', 'asd')    
    #print s.exports()
    


    