import sys # 4.)
class AppContext(object):
    _instance = None # 1.)
    def __init__(self): # 4.)
        self.__insideMaya  = 'maya.app.startup.basic' in sys.modules
        self.__insideNuke = 'nuke' in sys.modules
        self.__standalone = not (self.__insideMaya or self.__insideNuke)
        
    def __new__(cls, *args, **kwargs): # 2.)
        if not cls._instance: # 3.)
            cls._instance = super(AppContext, cls).__new__(cls, *args, **kwargs)
        return cls._instance    
        
    def isMaya(self): # 5.)
        return self.__insideMaya
    
    def isNuke(self): # 5.)
        return self.__insideNuke
    
    def isStandalone(self): # 5.)
        return self.__standalone
    
    def toString(self): # 6.)
        if self.isMaya(): return 'Maya'
        elif self.isNuke(): return 'Nuke'
        return 'Standalone'