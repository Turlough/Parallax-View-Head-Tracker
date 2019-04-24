from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, PointLight
from panda3d.core import LPoint3, LVector3

from direct.task import Task

from math import pi, atan2


import cv2


class Paralax(ShowBase):

    startX = 0.0
    startY = -30.0
    startZ = 20.0
    x = startX
    y = startY
    z = startZ

    prevX = x

    haar = "haarcascade_frontalface_default.xml"

    def __init__(self):
        ShowBase.__init__(self)

        self.cap = cv2.VideoCapture(0)
        self.classifier = cv2.CascadeClassifier(self.haar)

        self.scene = self.loader.loadModel('models/abstractroom')
        self.scene.reparentTo(self.render)

        self.scene.setPos(-10, 100, 0)

        self.shaderenable = 1
        self.scene.setShaderAuto()

        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        self.scene.setLight(alnp)

        # Add a light to the scene.
        self.lightpivot = render.attachNewNode("lightpivot")
        self.lightpivot.setPos(0, 0, 25)
        self.lightpivot.hprInterval(10, LPoint3(360, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor((1, 1, 1, 1))
        plight.setAttenuation(LVector3(0.7, 0.05, 0))
        plnp = self.lightpivot.attachNewNode(plight)
        plnp.setPos(45, 0, 0)
        self.scene.setLight(plnp)

        self.taskMgr.add(self.display, 'Display')
        (self.width, self.height) = (base.win.getXSize(), base.win.getYSize())
        print("Window: %.1f, %.1f" % (self.width, self.height))
        print("%.1f, %.1f, %.1f" % (self.x, self.y, self.z))


    def rotateLight(self, offset):
        self.lightpivot.setH(self.lightpivot.getH() + offset * 20)

    def findFace(self):

        _, frame = self.cap.read()
        frame = cv2.resize(frame, (300, 300))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(gray, 1.3, 5)

        if(len(faces) > 0):

            (self.width, self.height) = (base.win.getXSize(), base.win.getYSize())
            # print("Window: %.1f, %.1f" % (self.width, self.height))

            (x, y, w, h) = faces[0]
            centerX = x + (w / 2)
            centerZ = y + (h / 2)

            self.x = self.startX - centerX / 20
            # self.z = self.startZ - centerZ / 50


            # self.y = self.startY - center / 15
            # self.y = 40 - w / 15
            print("%.1f, %.1f, %.1f" % (self.x, self.y, self.z))

    def display(self, task):

        self.camera.setPos(self.x, self.y, self.z)
        rads = atan2(self.y , self.x)
        degs = 0
        degs = 180 * rads / pi
        degs += 100
        self.camera.setHpr(degs, 0, 0)
        self.findFace()

        return Task.cont


if __name__ == '__main__':

    app = Paralax()
    app.run()
