import cocos
import pyglet
import pymunk

class Zombie(object):
    def __init__(self):
        super(Zombie, self).__init__()

        #The physics variables.
        self.verts = [(-15, -15), (-15, 15), (15, 15), (15, -15)]
        self.mass = 100
        self.friction = 9
        self.elasticity = 0
        self.moment = pymunk.moment_for_poly(self.mass, self.verts)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = 500, 200
        self.shape = pymunk.Poly(self.body, self.verts)
        self.shape.layers = 1
        self.shape.collision_type = 3
        self.shape.friction = 0.1

        #Load the enemy sprite sheet.
        self.img = pyglet.resource.image('enemy.png')

        #Slice the sprite sheet into a grid of specified rows and columns.
        self.sprite_sheet = pyglet.image.ImageGrid(self.img, 7, 3)

        #Create an image list of the elements in the Image grid by pulling them from the position on the list.

        #The enemy's image sequence for the left walk animation.
        self.img_seq_enemy_walk_left = (self.sprite_sheet[15],
                                        self.sprite_sheet[16],
                                        self.sprite_sheet[17],
                                        self.sprite_sheet[16])

        #The player's image sequence for the front right animation.
        self.img_seq_enemy_walk_right = (self.sprite_sheet[12],
                                         self.sprite_sheet[13],
                                         self.sprite_sheet[14],
                                         self.sprite_sheet[13])

        #Create animations from the previous lists.
        self.enemy_anim_left = pyglet.image.Animation.from_image_sequence(self.img_seq_enemy_walk_left, .25)
        self.enemy_anim_right = pyglet.image.Animation.from_image_sequence(self.img_seq_enemy_walk_right, .25)

        #Create player still images.
        self.enemy_front = self.sprite_sheet[19]
        self.enemy_left = self.sprite_sheet[16]
        self.enemy_right = self.sprite_sheet[13]

        #Contains the sprite and image that is currently drawing at any given moment.
        #The image list initially contains the image the player spawns with.
        #We can add or subtract images to the list and swap them in and out of the playerSprite
        #to display the player's current texture.
        self.enemy_image_list = [self.enemy_front]
        self.enemy_img = cocos.sprite.Sprite(self.enemy_front, (100,200))

    #The image assigned to playerSprite will always be the last element in player_image_list.
    #The first element on the list is always the player standing still image which
    #gets dynamically replaced depending on which key is pressed.
    #The last element on the list is always the player walking animation which
    #gets dynamically replaced depending on which key is pressed.

    def walk_right(self):
        if self.enemy_img.image != self.enemy_anim_right:
            self.enemy_img.image = self.enemy_anim_right

    def walk_left(self):
        if self.enemy_img.image != self.enemy_anim_left:
            self.enemy_img.image = self.enemy_anim_left

    def update(self):
        #Bind the sprite's position to the pymunk object.
        self.enemy_img.position = self.body.position

