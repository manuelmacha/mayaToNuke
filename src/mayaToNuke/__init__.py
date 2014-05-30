'''
# Maya cmd:
import sys
p = '/Users/manuel/Dropbox/Private/Eclipse/workspace/mayaToNuke/src'
if not p in sys.path:
    sys.path.append(p)

from mayaToNuke import main as m2n
from mayaToNuke import constants
from mayaToNuke.utils import settings, mayaExport
from mayaToNuke.ui import baseUi
from mayaToNuke.ui import mayaUi
reload(constants)
reload(mayaExport)
reload(settings)
reload(baseUi)
reload(mayaUi)
reload(m2n)

m2n.showUi()
'''

'''
# Nuke cmd:
import sys
p = '/Users/manuel/Dropbox/Private/Eclipse/workspace/git/mayaToNuke/src'
if not p in sys.path:
    sys.path.append(p)

from mayaToNuke import main as m2n
from mayaToNuke import constants
from mayaToNuke.utils import settings, nukeImport
from mayaToNuke.ui import baseUi
from mayaToNuke.ui import nukeUi
reload(constants)
reload(nukeImport)
reload(settings)
reload(baseUi)
reload(nukeUi)
reload(m2n)

m2n.showUi()
'''
