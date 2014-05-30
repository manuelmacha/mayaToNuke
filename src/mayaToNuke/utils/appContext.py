import sys

class AppContext(object):
    _instance = None
    def __init__(self):
        self.__insideMaya  = 'maya.app.startup.basic' in sys.modules
        self.__insideNuke = 'nuke' in sys.modules
        self.__standalone = not (self.__insideMaya or self.__insideNuke)
        
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppContext, cls).__new__(cls, *args, **kwargs)
        return cls._instance        
        
    def isMaya(self):
        return self.__insideMaya
    
    def isNuke(self):
        return self.__insideNuke
    
    def isStandalone(self):
        return self.__standalone
    
    def toString(self):
        if self.isMaya(): return 'Maya'
        elif self.isNuke(): return 'Nuke'
        return 'Standalone'