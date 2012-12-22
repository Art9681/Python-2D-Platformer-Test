import cocos
import pymunk
import math

class Block(object):
    def __init__(self, pos):
        super(Block, self).__init__()

        #Import the block image.
        self.block_img = cocos.sprite.Sprite('brick.png')

        #Pymunk physics variables.
        self.verts = [(-15, -15), (-15, 15), (15, 15), (15, -15)]
        self.mass = 0.1
        self.moment = pymunk.moment_for_box(self.mass, 32, 32)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = pos
        self.shape = pymunk.Poly(self.body, self.verts)
        self.shape.layers = 1
        self.shape.collision_type = 4
        self.shape.friction = 1

    def update(self):
        self.block_img.position = self.body.position

        #Rotating code. Grab the physics body's angle and convert it to degrees, then assign that to the
        #sprite's rotation so we can see it on screen. Neat!
        self.block_img.rotation = -math.degrees(self.body.angle) #Subtract the degrees so the block rolls in the direction we want it to.

