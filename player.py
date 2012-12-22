import math
import pyglet
import pymunk
import cocos

class Player(object):
    def __init__(self):
        super(Player, self).__init__()

        #Pymunk physics variables.
        self.verts = [(-15, -15), (-15, 15), (15, 15), (15, -15)]
        self.mass = 100
        self.friction = 9
        self.elasticity = 0
        self.moment = pymunk.moment_for_poly(self.mass, self.verts)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = 150,300
        self.shape = pymunk.Poly(self.body, self.verts)
        self.shape.group = 1
        self.shape.layers = 1
        self.shape.collision_type = 1
        self.shape.friction = 0.1

        #variables for positioning the sprites or images.
        self.direction = True #True is right. False is left.
        self.player_moving_up = False
        self.player_moving_down = False
        self.player_moving_left = False
        self.player_moving_right = False
        self.on_ground = False

        #Load the player sprite sheet.
        self.player_img = pyglet.resource.image('player.png')

        #Slice the sprite sheet into a grid of specified rows and columns.
        self.sprite_sheet = pyglet.image.ImageGrid(self.player_img, 7, 3)

        #Create an image list of the elements in the Image grid by pulling them from the position on the list.
        #The player's image sequence for the front walk animation.
        self.img_seq_player_walk_front = (self.sprite_sheet[18],
                                          self.sprite_sheet[19],
                                          self.sprite_sheet[20],
                                          self.sprite_sheet[19])

        #The player's image sequence for the left walk animation.
        self.img_seq_player_walk_left = (self.sprite_sheet[15],
                                         self.sprite_sheet[16],
                                         self.sprite_sheet[17],
                                         self.sprite_sheet[16])

        #The player's image sequence for the front right animation.
        self.img_seq_player_walk_right = (self.sprite_sheet[12],
                                          self.sprite_sheet[13],
                                          self.sprite_sheet[14],
                                          self.sprite_sheet[13])

        #The player's image sequence for the rear walk animation.
        self.img_seq_player_walk_rear = (self.sprite_sheet[9],
                                         self.sprite_sheet[10],
                                         self.sprite_sheet[11],
                                         self.sprite_sheet[10])

        #Create animations from the previous lists.
        self.player_anim_front = pyglet.image.Animation.from_image_sequence(self.img_seq_player_walk_front, .25)
        self.player_anim_left = pyglet.image.Animation.from_image_sequence(self.img_seq_player_walk_left, .25)
        self.player_anim_right = pyglet.image.Animation.from_image_sequence(self.img_seq_player_walk_right, .25)
        self.player_anim_rear = pyglet.image.Animation.from_image_sequence(self.img_seq_player_walk_rear, .25)

        #Create player still images.
        self.player_front = self.sprite_sheet[19]
        self.player_left = self.sprite_sheet[16]
        self.player_right = self.sprite_sheet[13]
        self.player_rear = self.sprite_sheet[10]

        #Contains the sprite and image that is currently drawing at any given moment.
        #The image list initially contains the image the player spawns with.
        #We can add or subtract images to the list and swap them in and out of the playerSprite
        #to display the player's current texture.
        self.player_image_list = [self.player_front]
        self.player_sprite = cocos.sprite.Sprite(self.player_front, (100,200))

        #The player controls.
    #The image assigned to playerSprite will always be the last element in player_image_list.
    #The first element on the list is always the player standing still image which
    #gets dynamically replaced depending on which key is pressed.
    #The last element on the list is always the player walking animation which
    #gets dynamically replaced depending on which key is pressed.
    def walk_up(self):
        del self.player_image_list[0]
        self.player_image_list.insert(0, self.player_rear)
        self.player_image_list.append(self.player_anim_rear)
        #self.player_moving_up = True
        self.player_sprite.image = self.player_image_list[-1]
        print "The UP key was pressed"

    def walk_down(self):
        del self.player_image_list[0]
        self.player_image_list.insert(0, self.player_front)
        self.player_image_list.append(self.player_anim_front)
        #self.player_moving_down = True
        self.player_sprite.image = self.player_image_list[-1]
        print "The DOWN key was pressed"

    def walk_right(self):
        del self.player_image_list[0]
        self.player_image_list.insert(0, self.player_right)
        self.player_image_list.append(self.player_anim_right)
        #self.player_moving_right = True
        self.player_sprite.image = self.player_image_list[-1]

    def walk_left(self):
        del self.player_image_list[0]
        self.player_image_list.insert(0, self.player_left)
        self.player_image_list.append(self.player_anim_left)
        #self.player_moving_left = True
        self.player_sprite.image = self.player_image_list[-1]

    #When keys are released, the first element of player_image_list gets replaced with the
    #directional image of the player standing still and removes any animations assigned to its direction from the list.
    #If no keys are pressed, the only image remaining
    #in player_image_list will be the standing still image of the last key that was released, and thus
    #the image that gets drawn to screen.
    def stop_right(self):
        for i in self.player_image_list:
            if i == self.player_anim_right:
                self.player_image_list.remove(i)
        self.player_moving_right = False
        if self.player_image_list[0] != self.player_right:
            del self.player_image_list[0]
            self.player_image_list.insert(0, self.player_right)
        self.player_sprite.image = self.player_image_list[-1]
        print "The RIGHT key was released"

    def stop_left(self):
        for i in self.player_image_list:
            if i == self.player_anim_left:
                self.player_image_list.remove(i)
        self.player_moving_left = False
        if self.player_image_list[0] != self.player_left:
            del self.player_image_list[0]
            self.player_image_list.insert(0, self.player_left)
        self.player_sprite.image = self.player_image_list[-1]
        print "The LEFT key was released"

    def update(self):
        self.player_sprite.position = self.body.position
        if self.body.angle != 0.0:
            self.body.angle = 0.0

        #Rotating code. Grab the physics body's angle and convert it to degrees, then assign that to the
        #sprite's rotation so we can see it on screen. Neat!
        self.player_sprite.rotation = -math.degrees(self.body.angle) #Subtract the degrees so the block rolls in the direction we want it to.

