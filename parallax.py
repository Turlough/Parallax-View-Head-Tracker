from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, PointLight
from panda3d.core import LVector3

from direct.task import Task

from math import pi, atan2


import cv2


class Paralax(ShowBase):

    startX = 0.0
    startY = -50.0
    startZ = 30.0

    x = startX
    y = startY
    z = startZ

    # Trial and error found these to be acceptable scale factors
    scaleX = 1 / 20
    scaleY = 1 / 2
    scaleZ = 1 / 15

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

        # Add ambient light
        alight = AmbientLight('alight')
        alight.setColor((0.1, 0.11, 0.11, 1))
        alnp = self.render.attachNewNode(alight)
        self.scene.setLight(alnp)

        # Add point light.
        plight = PointLight('plight')
        plight.setColor((1, 1, 1, 1))
        plight.setAttenuation(LVector3(0.1, 0.02, 0))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(-27, 100, 0)
        self.scene.setLight(plnp)
        # Create a sphere to denote the light
        sphere = self.loader.loadModel("models/icosphere")
        sphere.reparentTo(plnp)

        self.taskMgr.add(self.display, 'Display')

        print("%.1f, %.1f, %.1f" % (self.x, self.y, self.z))

    def findFace(self):

        _, frame = self.cap.read()
        frame = cv2.resize(frame, (300, 300))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(gray, 1.3, 5)

        if(len(faces) > 0):

            (x, y, w, h) = faces[0]
            centerX = x + (w / 2)
            centerZ = y + (h / 2)

            self.x = self.startX - centerX * self.scaleX
            self.z = self.startZ - centerZ * self.scaleZ
            # we use the width of the face to estimate distance.
            self.y = self.startY + w * self.scaleY

            print("%.1f, %.1f, %.1f" % (self.x, self.y, self.z))

    def display(self, task):

        self.camera.setPos(self.x, self.y, self.z)
        rads = atan2(self.y, self.x)
        degs = 0
        degs = 180 * rads / pi
        degs += 100
        self.camera.setHpr(degs, 0, 0)
        self.findFace()

        return Task.cont


if __name__ == '__main__':

    app = Paralax()
    app.run()
