import maya.cmds as cmds
import maya.mel as mel # 1.)
import os

def alembicExport(start, end, path, filename): # 2.)
    fullpath = os.path.join(path, filename)
    sel = cmds.ls(sl = True)
    if not len(sel) == 1: # 3.)
        return
    # 4.)
    cmd = 'AbcExport -j "-frameRange %d %d -root %s -file %s"' % (start, end, sel[0], fullpath)
    mel.eval(cmd)
    return os.path.isfile(fullpath) # 5.)