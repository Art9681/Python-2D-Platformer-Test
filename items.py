import math
import pymunk
import cocos

class Sword(object):
    global space
    def __init__(self, player_pos):
        super(Sword, self).__init__()
        #The sword image.
        self.sword_img = cocos.sprite.Sprite('sword.png')
        #self.sword_img.visible = False
        self.direction = True #True is for right, False is for left.

        #Sword physics variables.
        self.verts = [(-5, -17), (-5, 17), (5, 17), (5, -17)]
        self.mass = 10
        self.elasticity = 1
        self.moment = pymunk.moment_for_poly(self.mass, self.verts)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = player_pos
        self.shape = pymunk.Poly(self.body, self.verts)
        self.shape.group = 1
        #Make the shape a sensor so it doesnt generate collisions. Only collision callbacks.
        #self.shape.sensor = True
        self.shape.layers = 1
        self.shape.collision_type = 2

    def update(self, player_pos):
        #The sword image will follow the pymunk body.
        self.sword_img.position = self.body.position
        #Rotating code. Grab the physics body's angle and convert it to degrees, then assign that to the
        #sprite's rotation so we can see it on screen. Neat!
        self.sword_img.rotation = -math.degrees(self.body.angle)
