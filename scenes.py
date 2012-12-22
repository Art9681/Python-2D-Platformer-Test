import pyglet
import cocos
import levels
import interface


class MyGame(cocos.scene.Scene):
    def __init__(self):
        super(MyGame, self).__init__()


        #Create the clock and delta time variables.
        #The clock ticks 60 times a second.
        self.clock = pyglet.clock
        dt = 1/60

        #The layers this scene has.
        self.interface = interface.Interface()
        self.scroller = levels.Scroller(self.clock)

        #Add the layers to the scene.
        self.add(self.scroller.scroller)
        self.add(self.interface)

        self.clock.schedule(self.scroller.update)

