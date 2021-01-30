#Written by Abdulaziz Albastaki in January 2021
import sys
from panda3d.core import Vec3,PointLight, WindowProperties, CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollideMask, BitMask32
import math
from playerGUI import GUI

class Player():
    def __init__(self,camera,accept,render,loader,maxJPHeight):
        #initial variables and sounds
        self.jetPack_energy = 100
        self.maximumHeight = maxJPHeight
        self.jetPack_AUDIO = loader.loadSfx("assets/base/sounds/jetpack2.wav")
        self.jetPack_AUDIO.setLoop(True)

        #initiate GUI
        self.HUD = GUI()
        self.playerHolder = render.attachNewNode('player')

        self.character = loader.loadModel('assets/base/models/player.bam')
        self.toggleFPCam = False
        self.character.setPos(0,0,0)
        self.character.reparentTo(self.playerHolder)
        self.playerBase = self.playerHolder.attachNewNode('camParent')
        self.thirdPersonNode = self.playerBase.attachNewNode('thirdPersonCam')
        camera.reparentTo(self.thirdPersonNode)
        self.mouseSeconds = []

        #collision stuff
        self.pusher = CollisionHandlerPusher()
        self.colliderNode = CollisionNode("player")
        self.colliderNode.addSolid(CollisionSphere(0, 0, 0, 1))
        self.colliderNode.setFromCollideMask(CollideMask.bit(0))
        self.colliderNode.setIntoCollideMask(BitMask32.allOff())
        collider = self.playerHolder.attachNewNode(self.colliderNode)
        self.pusher.addCollider(collider,self.playerHolder)
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(collider,self.pusher)
        self.cTrav.show_collisions(render)
        self.setupLighting() # light
        #initial position
        self.playerHolder.setPos(64529.7, 25629.3, 2000)
        self.keyMap = {
            "left": False,
            "right": False,
            "forward": False,
            "backwards": False,
            "change_camera": False,
            "leftClick": False,
            "space": False,
            "p":False
        }

        accept("escape", sys.exit)
        accept("w", self.updateKey, ["forward", True])  #
        accept("w-up", self.updateKey, ["forward", False])

        accept("a", self.updateKey, ["left", True])
        accept("a-up", self.updateKey, ["left", False])

        accept("s", self.updateKey, ["backwards", True])
        accept("s-up", self.updateKey, ["backwards", False])

        accept("d", self.updateKey, ["right", True])
        accept("d-up", self.updateKey, ["right", False])

        accept("c",self.updateKey,["change_camera", True])

        accept("mouse1",self.updateKey,["leftClick",True])
        accept("mouse1-up",self.updateKey,["leftClick",False])

        accept("p", self.updateKey, ["p", True])
        accept("p-up", self.updateKey, ["p", False])

        accept("space",self.updateKey,["space",True])
        accept("space-up",self.updateKey,["space",False])

    def updateKey(self,key,value):
        self.keyMap[key] = value
        if key == "change_camera":
            self.changeCamera()

    def changeCamera(self):
        if self.toggleFPCam == False:
            self.toggleFPCam = True
        else:
            self.toggleFPCam = False

    def recenterMouse(self):
        base.win.movePointer(0, int(base.win.getProperties().getXSize() / 2), int(base.win.getProperties().getYSize() / 2))

    def setupLighting(self):
        plight = PointLight('plight')
        plight.setColor((0.2, 0.2, 0.2, 1))
        plnp = self.playerHolder.attachNewNode(plight)
        render.setLight(plnp)

    def playerUpdate(self,task):
        deltaTime = globalClock.getDt()
        #mouse controls
        if self.toggleFPCam: #first person camera controls
            camera.setPos(self.character.getPos())  # 0,-50,-10
            #camera.setZ(camera, 20)
            props = WindowProperties()
            props.setCursorHidden(True)
            props.setMouseMode(WindowProperties.M_relative)
            base.win.requestProperties(props)
            self.character.hide()

            if (base.mouseWatcherNode.hasMouse() == True):
                mouseposition = base.mouseWatcherNode.getMouse()
                camera.setP(mouseposition.getY() * 30)
                #self.playerBase.setH(self.playerBase.getH())
                #camera.setP(mouseposition.getY() * 30)
                self.playerBase.setH(mouseposition.getX() * -50)
                if (mouseposition.getX() < 0.1 and mouseposition.getX() > -0.1):
                    self.playerBase.setH(self.playerBase.getH())
                else:
                    #self.playerBase.setH(self.playerBase.getH() + mouseposition.getX() * -1)
                    pass

        else: #takes out of first person perspective if toggleFPS is turned off.
            props = WindowProperties()
            props.setCursorHidden(False)
            props.setMouseMode(WindowProperties.M_absolute)
            base.win.requestProperties(props)
            self.character.show()
            camera.setPos(0, -50, -4)  # 0,-50,-10
            camera.lookAt(self.character)

        self.walkConstant = 900
        self.rotateConstant = 100
        #Keyboard controls
        if self.keyMap["forward"]:
            self.playerHolder.setY(self.playerBase, (self.walkConstant*deltaTime))
            self.character.setP(self.character.getP() + (-self.rotateConstant*deltaTime*(math.cos(math.radians(self.playerBase.getH())))))
            self.character.setR(self.character.getR() - (self.rotateConstant*deltaTime*(-math.sin(math.radians(self.playerBase.getH())))))

        if self.keyMap["right"]:
            self.playerHolder.setX(self.playerBase, (self.walkConstant*deltaTime))
        if self.keyMap["p"]:
            print(self.playerHolder.getPos())
        if self.keyMap["left"]:
            self.playerHolder.setX(self.playerBase, (-self.walkConstant*deltaTime))

        if self.keyMap["backwards"]:
            self.playerHolder.setY(self.playerBase, (-self.walkConstant * deltaTime))
            self.character.setP(self.character,(self.rotateConstant*deltaTime))

        if self.keyMap["space"] and self.jetPack_energy>0:
            jetpack = 0.00001*(((self.playerHolder.getZ())-self.maximumHeight)**2)+98.1
            self.playerHolder.setZ(self.playerBase, jetpack)
            self.jetPack_energy -= 8*deltaTime
            if self.jetPack_AUDIO.status() != self.jetPack_AUDIO.PLAYING:
                self.jetPack_AUDIO.play()
        else:
            if self.jetPack_energy < 100:
                self.jetPack_energy += 10*deltaTime
            if self.jetPack_energy > 100:
                self.jetPack_energy = 100
            self.jetPack_AUDIO.stop()
        self.HUD.jetpackStatus.text = str(int(self.jetPack_energy))+"%"

        #third person camera control
        if (self.keyMap["leftClick"] == True) and (self.toggleFPCam == False): #third person camera controls
            if (base.mouseWatcherNode.hasMouse() == True):
                mouseposition = base.mouseWatcherNode.getMouse()
                self.mouseSeconds.append(mouseposition)
            if len(self.mouseSeconds) == 2:
                lookConstant = 1
                upperconstant = 40
                lowerconstant = 1
                moveX = ((self.mouseSeconds[1].getX())*upperconstant - (self.mouseSeconds[0].getX())*lowerconstant)*lookConstant
                moveY = ((self.mouseSeconds[1].getY())*upperconstant - (self.mouseSeconds[0].getY())*lowerconstant)*lookConstant
                if (moveX > 1 or moveX < -1):
                    self.playerBase.setH(self.playerBase.getH() - moveX)
                if (moveY > 1 or moveY < -1):
                    self.thirdPersonNode.setP(self.thirdPersonNode.getY()+moveY)
                self.mouseSeconds = []
        self.cTrav.traverse(render)
        self.playerHolder.setPos(self.playerHolder, Vec3(0,0,-9.81)*deltaTime) # Gravity
        return task.cont