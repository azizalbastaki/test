#Written by Abdulaziz Albastaki in January 2021
from panda3d.core import BitMask32, AmbientLight
from buildings import dock
from water import water
class environment():
    def __init__(self,render,loader):
        self.loader = loader
        def make(x):
            self.fakeWorld = loader.loadModel('assets/environment/nature/world.bam')
            self.fakeWorld.reparentTo(render)
            self.fakeWorld.setScale(100)
            self.fakeWorld.setSz(10000)
            self.fakeWorld.setZ(-1010)
            self.fakeWorld.setY(x)
            self.fakeWorld.flattenStrong()
        make(0)
        make(90000)
        make(-100000)
        self.river = water(render, loader, (36728.9, 31409.8, -150), 34000, 300000)  # 200,200
        self.world = loader.loadModel('assets/environment/nature/world.bam')
        self.maximumHeight = 4000  # 24693
        self.world.reparentTo(render)
        self.world.setScale(100)
        self.world.setSz(10000)
        self.world.setZ(-1010)
        self.world.setY(0)
        self.world.setCollideMask(BitMask32.bit(0))
        self.world.hide()
        self.town()
        self.setupLights()

    def setupLights(self):
        ambiet = AmbientLight('ambient')
        ambiet.setColor((0.2,0.2,0.2,1))
        alight = render.attachNewNode(ambiet)
        render.setLight(alight)
    def town(self):
        port = dock(self.loader,(45150, 42978.6, -38.4))
