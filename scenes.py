import pyglet
import cocos
from cocos import layer, tiles
import levels
import interface


class MyGame(cocos.scene.Scene):
    def __init__(self):
        super(MyGame, self).__init__()
        global scroller
        #Create the clock and delta time variables.
        #The clock ticks 60 times a second.
        self.clock = pyglet.clock
        dt = 1/60

        #The layers this scene has.
        self.interface = interface.Interface()
        self.level1 = levels.Level(self.clock)


        #Add the tilemap and the level to the scrolling manager
        scroller = cocos.layer.ScrollingManager()
        self.resource = cocos.tiles.load('map.tmx')#['Tile Layer 1']
        self.map = self.resource.get_resource('Tile Layer 1')
        self.tprint = self.resource.contents
        scroller.add(self.map, z=0)
        scroller.add(self.level1, z=1)

        #tprint = self.tprint.find_cells(test=True)
        print self.tprint

        #Add the layers to the scene.
        self.add(scroller, z=1)
        self.add(self.interface, z=2)

        self.clock.schedule(self.update)

    def update(self, dt):
        self.level1.update(dt)
        scroller.set_focus(*self.level1.player.player_sprite.position)