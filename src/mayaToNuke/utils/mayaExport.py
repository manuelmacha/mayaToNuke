import maya.cmds as cmds
import maya.mel as mel
import os

def alembicExport(start, end, path, filename):
    fullpath = os.path.join(path, filename)
    sel = cmds.ls(sl = True)
    if not len(sel) == 1: 
        return
    cmd = 'AbcExport -j "-frameRange %d %d -root %s -file %s"' % (start, end, sel[0], fullpath)
    mel.eval(cmd)
    return os.path.isfile(fullpath)