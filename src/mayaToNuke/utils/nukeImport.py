import nuke
from mayaToNuke.constants import TOOLNAME

def importFromFile(name, fullpath, type_):
    
    if type_ == 'mesh':
        node = nuke.nodes.ReadGeo2(file = fullpath)
    elif type_ == 'locator':
        node = nuke.nodes.Axis2(read_from_file = True, file = fullpath)
    elif type_ == 'camera':
        node = nuke.nodes.Camera2(read_from_file = True, file = fullpath)
    else:
        nuke.message('Import for type %s not yet supported' % type_)
        return
    node.setName(name)
    
    scene = None
    sel = nuke.selectedNodes()
    if len(sel):
        if sel[0].Class() == 'Scene':
            scene = sel[0]
    else:
        scene = nuke.toNode(TOOLNAME)
    if not scene:
        scene = nuke.nodes.Scene(name = TOOLNAME)    
    
    numInputs = scene.inputs()
    scene.setInput(numInputs, node)
    return node