from pyglet.window import key, mouse
from pyglet.gl import *
import cocos
from cocos import layer, tiles
from cocos.particle import *
from cocos.particle_systems import *
import pymunk
import interface
import player
import items
import blocks
import npc

class Level(cocos.layer.ScrollableLayer):
    global scroller
    is_event_handler = True
    def __init__(self, clock):
        super( Level, self ).__init__()

        self.clock = clock
        self.dt = 1/60

        #Create the pymunk space that will simulate the physics.
        self.space = pymunk.Space()

        '''Used to reduce oscillating contacts and keep the collision
        cache warm. Defaults to 0.1. If you have poor simulation quality,
        increase this number as much as possible without allowing visible
        amounts of overlap.'''
        self.space.collision_slop = 0.3
        self.space.gravity = (0,-700)

        #The map boundaries.
        self.boundary_left = pymunk.Segment(self.space.static_body, (0, 0), (0, 500), 1)
        self.boundary_left.friction = 10
        self.boundary_left.collision_type = 4
        self.boundary_right = pymunk.Segment(self.space.static_body, (3200, 0), (3200, 500), 1)
        self.boundary_right.friction = 10

        #The platform object.
        self.platform = pymunk.Segment(self.space.static_body, (0, 64), (3200, 64), 1)
        self.platform.friction = 5
        self.platform.collision_type = 4
        self.floor = cocos.draw.Line((0,64), (3200,64), (255,255,255,255), 5)
        self.floor.visible = False

        #Create actors and other physics objects.
        self.player = player.Player()
        self.block = blocks.Block(pos = (400,300))
        self.zombie = npc.Zombie()
        self.particle = Explosion()
        self.particle.gravity = Point2(700, 0)
        self.particle.size = 5

        #self.particle.position_type = ParticleSystem.POSITION_FREE

        self.block_group = []
        self.sword_group = []
        self.vertices = []

        #Create the batch node to minimize the number of gl calls. Basically puts sprites in a group and
        #renders all of them at once or something like that.
        self.batch_node = cocos.batch.BatchNode()
        self.batch_node.add(self.player.player_sprite)
        self.batch_node.add(self.block.block_img)
        self.batch_node.add(self.zombie.enemy_img)

        self.add(self.batch_node)
        self.add(self.floor, z=1)

        #Add physics objects to our space.
        self.space.add(
                        self.boundary_left,
                        self.boundary_right,
                        self.platform,
                        self.player.body,
                        self.player.shape,
                        self.block.body,
                        self.block.shape,
                        self.zombie.body,
                        self.zombie.shape)

        #The collision handler. When the objects with the defined collision types collide,
        #The handler fires the methods defined here.
        #Collision types are as follows:
        #Ground and Walls = 4
        #Sword = 2
        #Zombie = 3
        self.space.add_collision_handler(1, 4, begin = self.player_ground, pre_solve = None, post_solve = None)
        self.space.add_collision_handler(2, 3, begin = self.zombie_dead, pre_solve = None, post_solve = None)


    def player_ground(self, space, arbiter):
        self.player.on_ground = True
        return True

    #This runs when the sword collides with the enemy.
    def zombie_dead(self, space, arbiter):
        self.add(self.particle)
        self.particle.position = self.zombie.body.position
        self.zombie.shape.layers = 0
        return True

    #I should probably move this to the Sword class...
    def remove_sword(self, dt):
        self.rsword = self.sword_group[0]
        self.space.add_post_step_callback(self.space.remove, self.rsword.body, self.rsword.shape)
        self.remove(self.rsword.sword_img)
        #self.batch_node.remove(img)
        self.sword_group.pop(0)


    #Allows us to override the layer draw so we can draw our own stuff! Useful for using Pyglet gl calls and stuffs!!
    def draw(self):
        #Blacks out the scrolling background. Useful! Use it later!
        #glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_TRIANGLES)
        glVertex2f(0, 0)
        glVertex2f(40, 0)
        glVertex2f(20, 40)
        glEnd()


    def update(self, dt):
        self.space.step(dt)
        self.player.update()
        self.block.update()
        self.zombie.update(self.player.body.position)

        for sword in self.sword_group:
            sword.update(self.player.body.position)
        for block in self.block_group:
            block.update()

    #Detects key presses and releases and fires events accordingly.
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            if self.player.on_ground == True:
                #Make the player jump!
                self.player.body.apply_impulse(pymunk.Vec2d(0, 40000), (0, 0))
                self.player.on_ground = False
        if symbol == key.D:
            self.player.direction = True
            #self.sword.direction = True
            self.player.shape.friction = 0.0
            self.player.walk_right()
            self.player.body.velocity.x = 200
        if symbol == key.A:
            self.player.direction = False
            #self.sword.direction = False
            self.player.shape.friction = 0.0
            self.player.walk_left()
            self.player.body.velocity.x = -200
            #Reverse gravity!
        if symbol == key.W:
            self.space.gravity = (0, 700)
        #This will show or hide the physics objects. A lot of work to do here.
        if symbol == key.V:
            if self.floor.visible == True:
                self.floor.visible = False
            else:
                self.floor.visible = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.player.body.apply_impulse(pymunk.Vec2d(0, -10000), (0, 0))
        if symbol == key.D:
            self.player.stop_right()
            self.player.shape.friction = 10
            self.player.body.velocity.x = 0
        if symbol == key.A:
            self.player.stop_left()
            self.player.shape.friction = 10
            self.player.body.velocity.x = 0
        if symbol == key.W:
            self.space.gravity = (0, -700)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            #When the left mouse button is clicked, the sword is created and an impulse
            #and angular velocity are applied so it is thrown.
            self.sword = items.Sword(self.player.body.position)
            self.sword_group.append(self.sword)
            self.add(self.sword.sword_img)
            #self.batch_node.add(self.sword.sword_img)
            self.space.add(self.sword.body, self.sword.shape)
            print self.sword_group

            if self.player.direction == True:
                self.sword.body.apply_impulse(pymunk.Vec2d(9000, 0), (0, 0))
                self.sword.body.angular_velocity = -40
            else:
                self.sword.body.apply_impulse(pymunk.Vec2d(-9000, 0), (0, 0))
                self.sword.body.angular_velocity = 40

            #Remove the sword physics objects after a certain interval.
            self.clock.schedule_once(self.remove_sword, 1.0)

        #Spawn a block at the location of the mouse.
        if button == mouse.RIGHT:
            if interface.MenuDev.spawn == "segment":
                if len(self.vertices)<2:
                    self.vertices.append(scroller.pixel_from_screen(x, y))
                else:
                    self.vertice_first = self.vertices[0]
                    self.vertice_second = self.vertices[1]
                    self.wall = cocos.draw.Line(self.vertice_first, self.vertice_second, (255,255,255,255), 5)
                    self.add(self.wall)
                    self.vertices.pop(1)
                    self.vertices.pop(0)

                    self.platform = pymunk.Segment(self.space.static_body, self.vertice_first, self.vertice_second, 1)
                    self.space.add(self.platform)
                print self.vertices
            if interface.MenuDev.spawn == "block":
                self.pos = scroller.pixel_from_screen(x, y)
                self.block1 = blocks.Block(pos = self.pos)
                self.block_group.append(self.block1)
                self.add(self.block1.block_img)
                self.space.add(self.block1.body, self.block1.shape)


#Handles the scrolling manager. Physics layers get added to this and this class gets added to the scene.
class Scroller(object):
    def __init__(self, clock):
        super(Scroller, self).__init__()
        global scroller

        scroller = cocos.layer.ScrollingManager()
        self.level1 = Level(clock)
        #Add the tilemap and the level to the scrolling manager
        self.resource = cocos.tiles.load('map.tmx')
        self.map = self.resource.get_resource('Tile Layer 1')
        scroller.add(self.map)
        scroller.add(self.level1)

        self.scroller = scroller

    def update(self, dt):
        self.level1.update(dt)
        scroller.set_focus(*self.level1.player.player_sprite.position)