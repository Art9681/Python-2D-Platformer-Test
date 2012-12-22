import cocos
from pyglet.window import key

class Interface(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super( Interface, self ).__init__()

        self.dev_menu = MenuDev()
        self.add(self.dev_menu.menu)

    def on_key_press(self, symbol, modifiers):
        #Set the layer visibility if the M key is pressed. Brings up the menu and closes it.
        if symbol == key.M:
            if self.dev_menu.menu.visible == True:
                self.dev_menu.menu.visible = False
            elif self.dev_menu.menu.visible == False:
                self.dev_menu.menu.visible = True

class MenuDev(object):
    def __init__(self):
        super( MenuDev, self ).__init__()

        #Define the menu...
        self.menu = cocos.menu.Menu()
        self.menu.visible = False

        #Then add the items.
        self.item1 = cocos.menu.MenuItem('First menu item guys!', self.pmenu)

        #Now creat the menu.
        self.menu.create_menu( [ self.item1] )

    def pmenu(self):
        print "Menu item1 clicked."


    def on_toggle_callback(self, b ):
        print 'toggle item callback', b

