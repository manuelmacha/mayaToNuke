import nuke 
from mayaToNuke.constants import TOOLNAME 

def importFromFile(name, fullpath, type_): # 1.) 
    if type_ == 'mesh': # 2.) 
        node = nuke.nodes.ReadGeo2(file = fullpath)
    elif type_ == 'locator': # 3.)
        node = nuke.nodes.Axis2(read_from_file = True, file = fullpath)
    elif type_ == 'camera': # 4.)
        node = nuke.nodes.Camera2(read_from_file = True, file = fullpath)
    else: # 5.)
        nuke.message('Import for type %s not yet supported' % type_)
        return
    node.setName(name) # 6.)
    
    scene = None # 7.)
    sel = nuke.selectedNodes()
    if len(sel):
        if sel[0].Class() == 'Scene':
            scene = sel[0]
        else:
            scene = nuke.toNode(TOOLNAME)
    else:
        scene = nuke.toNode(TOOLNAME)
    if not scene:
        scene = nuke.nodes.Scene()
        scene.setName(TOOLNAME)  
    
    numInputs = scene.inputs()  # 8.)
    scene.setInput(numInputs, node)
    return node