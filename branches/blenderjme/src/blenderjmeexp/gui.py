__version__ = '$Revision$'
__date__ = '$Date$'
__author__ = 'Blaine Simpson, blaine (dot) simpson (at) admc (dot) com'
__url__ = 'http://www.jmonkeyengine.com'

import Blender
from Blender import Draw
from Blender import BGL
from bpy import data
import exporter
from os import path

defaultFilePath = path.abspath("default-jme.xml")
saveAll = False
xmlFile = None
BTNID_SAVEALL = 1
BTNID_SAVE = 2
BTNID_CANCEL = 3

def exitModule():
    global guiBox
    guiBox.free()
    Draw.Exit()
    print "Exiting exporter"

def exportableCounts():
    """Returns counts of all exportable objects, and all selected exportable
    objects"""
    # TODO:  Narrow to EXPORTABLEs.  We can't export most Blender object types.
    return [len(data.objects), len(data.scenes.active.objects.selected)]

def btnHandler(btnId):
    global saveAll, xmlFile, defaultFilePath
    if btnId == BTNID_SAVEALL:
        saveAll = not saveAll
        return
    if btnId == BTNID_SAVE:
        try:
            xmlFile = exporter.gen(saveAll)
        except Exception as e:
            if 1 == Draw.PupMenu(str(e) + "%t|Abort|Try other settings"):
                exitModule()
            return
        Blender.Window.FileSelector(saveFile, "Write XML file", defaultFilePath)
        # TODO:  Upon successful save, store file path to Blender registry
        # so that we can use it as default the next time.
        return
    if btnId == BTNID_CANCEL:
        exitModule()
        return

def inputHandler(eventNum, press): # press is set for mouse movements. ?
    if not press: return
    if eventNum == Draw.ESCKEY:
        print "Got ESC"
        exitModule()

class GuiBox(object):
    __slots__ = ['x', 'y', 'w', 'h', '__imgs', '__imgpaths']

    def __init__(self, w, h, imgpaths):
        object.__init__(self)
        self.w = w
        self.h = h
        availableW, availableH = Blender.Window.GetAreaSize()
        if (w > availableW) or (h > availableH):
            raise Exception("Current Window not large enough for our Gui")
        self.x = (availableW - self.w) / 2
        self.y = (availableH - self.h) / 2
        self.__imgpaths = imgpaths
        self.__loadImages()

    def __loadImages(self):
        self.__imgs = []
        for path in self.__imgpaths:
            self.__imgs.append(Blender.Image.Load(path))
        for img in self.__imgs: img.glLoad()

    def free(self):
        for img in self.__imgs: img.glFree()
        self.__imgs = None

    def drawBg(self):
        if not self.__imgs: self.__loadImages()
        BGL.glColor3f(.95,.54,.24)
        BGL.glRectf(self.x, self.y, self.x + self.w, self.y + self.h)
        BGL.glColor3f(1, 1, 1)
        BGL.glRectf(self.x + 5, self.y + 5, \
                self.x + self.w - 5, self.y + self.h - 5)

        imgDim = self.__imgs[0].getSize()[0]; # Unfortunately [0] == [1]
        imgY = self.y + self.h - imgDim   # Img starts at top of gui box
        imgX = self.x + (self.w - len(self.__imgs) * imgDim) / 2
          # Centered horizontally in gui box
        for img in self.__imgs:
            BGL.glEnable(BGL.GL_TEXTURE_2D)
            BGL.glBindTexture(BGL.GL_TEXTURE_2D, img.getBindCode())
            BGL.glBegin(BGL.GL_POLYGON)
            BGL.glTexCoord2f(0.0,0.0) 
            BGL.glColor3f(1.0,1.0,1.0)
            BGL.glVertex3f(float(imgX),float(imgY),0.0)
            BGL.glTexCoord2f(1.0,0.0)
            BGL.glColor3f(1.0,1.0,1.0)
            BGL.glVertex3f(float(imgX + imgDim),float(imgY),0.0)
            BGL.glTexCoord2f(1.0,1.0)
            BGL.glColor3f(1.0,1.0,1.0)
            BGL.glVertex3f(float(imgX+imgDim),float(imgY+imgDim),0.0)
            BGL.glTexCoord2f(0.0,1.0)	
            BGL.glColor3f(1.0,1.0,1.0)
            BGL.glVertex3f(float(imgX),float(imgY+imgDim),0.0 )
            imgX += imgDim
            BGL.glEnd() 
            BGL.glDisable(BGL.GL_TEXTURE_2D)

        # Anything done after the image writing writes with BLACK
        #BGL.glColor3f(1., 0., 0.)
        #BGL.glRectf(self.x, y, self.x + self.w, self.y + self.h -  self.imgH)


guiBox = GuiBox(330, 300, ['/home/blaine/.blender/scripts/bj1.png', \
    '/home/blaine/.blender/scripts/bj2.png', \
    '/home/blaine/.blender/scripts/bj3.png', \
    '/home/blaine/.blender/scripts/bj4.png', \
    '/home/blaine/.blender/scripts/bj5.png'])

def saveFile(filepath):
    # Can only get here when our Gui is present, but completely overwritten
    # by the FileSelector window.
    global defaultFilePath

    try:
        if filepath.endswith(".blend"):
            raise Exception( \
            "You should only save Blender native files with extension '.blend'")
        print "Attempting to save file '" + filepath + "'"
        xmlFile.writeFile(filepath)
        print "Saved file '" + filepath + "'"
        defaultFilePath = filepath
        exitModule()
    except Exception as e:
        if 1 == Draw.PupMenu(str(e) + "%t|Abort|Try other settings"):
            exitModule()
        print "Will retry"

def drawer():
    global saveAll, BTNID_SAVEALL, BTNID_SAVE, BTNID_CANCEL, guiBox

    BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
    guiBox.drawBg()
    Draw.PushButton("Cancel", BTNID_CANCEL, \
            guiBox.x + 10, guiBox.y + 10, 100, 20, "Abort export")
    allCount, selCount = exportableCounts()
    if selCount < 1:  # TEMPORARY.  Enable following once impl. saveAll.
    #if allCount < 0:
        Draw.Label("Your scenes contain no",
                guiBox.x + 10, guiBox.y + 200,200,20)
        Draw.Label("export-supported objects",
                guiBox.x + 10, guiBox.y + 170,200,20)
        return
    Draw.Toggle("All Scene Objects",
            BTNID_SAVEALL, guiBox.x + 10, guiBox.y + 200,100,20, saveAll,
            "Save all savable items from scene, as opposed to selected items")
    Draw.PushButton("Export", BTNID_SAVE, \
            guiBox.x + 10, guiBox.y + 50, 100, 20, "Select file to save to")
