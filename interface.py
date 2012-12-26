import cocos
from pyglet.window import key

#The Interface layer controls the visibility and other attributes of interface elements and menus.
#We remove the menu object when not visible so events dont register.
class Interface(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super( Interface, self ).__init__()
        self.dev_menu = MenuDev()

    def on_key_press(self, symbol, modifiers):
        #Set the layer visibility if the M key is pressed. Brings up the menu and closes it.
        if symbol == key.M:
            if self.dev_menu.menu.visible == True:
                self.dev_menu.menu.visible = False
                self.remove(self.dev_menu.menu)
                #self.dev_menu.menu.remove_all_handlers()
            elif self.dev_menu.menu.visible == False:
                self.dev_menu.menu.visible = True
                self.add(self.dev_menu.menu)

class MenuDev(object):
    #The item that will spawn based on what was selected in the menu.
    spawn = ""

    def __init__(self):
        super( MenuDev, self ).__init__()

        #Define the menu...
        self.menu = cocos.menu.Menu()
        self.menu.visible = False

        #Then add the items.
        self.block = cocos.menu.MenuItem('Create Block', self.create_block)
        self.segment = cocos.menu.MenuItem('Create Segment', self.create_segment)

        #Now create the menu.
        self.menu.create_menu([self.block, self.segment])

    def create_block(self):
        MenuDev.spawn = "block"
        print "Create block clicked!"

    def create_segment(self):
        MenuDev.spawn = "segment"
        print "Create segment clicked!"


    def on_toggle_callback(self, b ):
        print 'toggle item callback', b

